# Glimpse of data and missing value check
understand_data<- function(data) {
    glimpse(data)
    
    check_missing = levels(factor(is.na(data)))
    if(length(check_missing) <= 1 && check_missing != TRUE) {
        cat(blue("There are no missing values in your dataset."))
        } else {
        cat(blue(paste("There are", count(data[is.na(data),]), "missing values in your dataset.")))
        cat(blue(paste(" There are", (count(data)+count(data[is.na(data),])), "values in total in your dataset.
")))
        cat(blue(paste("The missing values account for ", 
                    count(data[is.na(data),])/(count(data)+count(data[is.na(data),])),
              "% of your data.", sep = "")))
        }

   print(skim(data))

    }
