rename_columns <- function(data, list_names) {
    #list_name should be in the format list("name1", "name2", "etc")
    # list of names should be in the exact order of current column names
     
    for (n in 1:ncol(data)) {
        n_data <- data
        col_num = n
        new_name = list_names[n]
        colnames(n_data)[col_num] <- new_name
    }
    
    cat(blue("New column names"))
    head(n_data, 1)

}
