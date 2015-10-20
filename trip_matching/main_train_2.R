library(dtw)
library(rjson)

for (trip in 0:319){
    # Trip id
    print("####")
    print(trip)
    trip_id = trip

    # Read request index
    setwd(".\\output_1")
    request_line_original = scan(paste("trip_",trip_id,".csv",sep=""))

    request_line = sort(request_line_original)
    request_line_backup = request_line
    gc()

    # Read Train
    setwd("..\\..\\input")
    con  <- file("train.csv", open = "r")
    k=-1
    j=1
    similar_line_location=list()
    while (length(oneLine <- readLines(con, n = 1, warn = FALSE)) > 0) {
        if (k==-1){
            k=k+1
            next
        }

        if (length(request_line)==0){
            break
        }

        if (k==request_line[1]){
            line_location = unlist(strsplit(oneLine, "[\"]"))
            line_location = line_location[length(line_location)]
            request_line = request_line[-1]
            similar_line_location[[j]] = matrix(unlist(fromJSON(line_location)),nc=2,byrow = TRUE)
            j=j+1
        }


        if ((k%%100000)==0){
            print(k)
        }
        k=k+1
    }
    close(con)
    gc()

    # Read test
    target_line_location = NULL
    con  <- file("test.csv", open = "r")
    k=-1
    while (length(oneLine <- readLines(con, n = 1, warn = FALSE)) > 0) {
        if (k==-1){
            k=k+1
            next
        }
        if (k==trip_id){
            line_location = unlist(strsplit(oneLine, "[\"]"))
            line_location = line_location[length(line_location)]
            target_line_location = matrix(unlist(fromJSON(line_location)),nc=2,byrow = TRUE)
            break
        }
        k=k+1
    }
    close(con)
    gc()

    # Find the closest dynamic time wraping distance
    k=0
    dtw_dist = NULL
    target_snapshot = dim(target_line_location)[1]
    if (target_snapshot==1){
        print("One snapshot only")
    }else{
        for (i in 1:length(similar_line_location)) {
            temp_similar_line_location = similar_line_location[[i]]

            if (dim(temp_similar_line_location)[1]<target_snapshot){
                dtw_dist = c(dtw_dist,999)
            }
            else {
                # Compute multidimensiional dynamic time warping
                cxdist <-dist(target_line_location,temp_similar_line_location[1:target_snapshot,],method="euclidean")
                dtw_dist = c(dtw_dist,dtw(cxdist,distance.only=T)$distance)
            }

            if ((k%%1000)==0){
                print(k)
            }
            k=k+1
        }
    }
    if (target_snapshot==1){
        save_index = as.integer(request_line_original[1:100])
        save_index_2 = as.integer(request_line_original[1:100])
        save_index_3 = as.integer(request_line_original[1:100])
        save_index_4 = as.integer(request_line_original[1:100])
        save_index_5 = as.integer(request_line_original[1:100])
    }else{
        dtw_index = dtw_dist %in% sort(dtw_dist)[1:25][sort(dtw_dist)[1:25]<999]
        save_index = as.integer(request_line_backup[dtw_index])
        dtw_index = dtw_dist %in% sort(dtw_dist)[1:50][sort(dtw_dist)[1:50]<999]
        save_index_2 = as.integer(request_line_backup[dtw_index])
        dtw_index = dtw_dist %in% sort(dtw_dist)[1:75][sort(dtw_dist)[1:75]<999]
        save_index_3 = as.integer(request_line_backup[dtw_index])
        dtw_index = dtw_dist %in% sort(dtw_dist)[1:100][sort(dtw_dist)[1:100]<999]
        save_index_4 = as.integer(request_line_backup[dtw_index])
    }

    #setwd("/Users/achm/documents/digitcube_self/kaggle/taxi_ii")
    setwd("..\\trip_matching\\output_2")
    con  <- file(paste("trip_",trip_id,"_dtw_25.csv",sep=""), open = "w")
    write.table(file=con, save_index, row.names = FALSE, col.names=FALSE)
    close(con)
    con  <- file(paste("trip_",trip_id,"_dtw_50.csv",sep=""), open = "w")
    write.table(file=con, save_index_2, row.names = FALSE, col.names=FALSE)
    close(con)

    con  <- file(paste("trip_",trip_id,"_dtw_75.csv",sep=""), open = "w")
    write.table(file=con, save_index_3, row.names = FALSE, col.names=FALSE)
    close(con)

    con  <- file(paste("trip_",trip_id,"_dtw_100.csv",sep=""), open = "w")
    write.table(file=con, save_index_4, row.names = FALSE, col.names=FALSE)
    close(con)

}
