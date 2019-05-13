
descriptive_stats <- function(data, rem_na = NULL) {
    # data is a dataframe
    # rem_na = 'TRUE' or 'FALSE'. The default is "TRUE"
    
    # basic stats
    if(is.null(rem_na)) {
        cat(blue("Missing values have been removed to calculate stats."))
        sts<- psych::describe(data, na.rm = TRUE)
    } else if(rem_na == TRUE) {
        cat(blue("Missing values have been removed to calculate stats."))
        sts<- psych::describe(data, na.rm = TRUE)
        } else {
        cat(blue("Missing values have NOT been removed to calculate stats."))
        sts<- psych::describe(data, na.rm = FALSE)
        }
    
    # mode: Function to get the mode: https://www.tutorialspoint.com/r/r_mean_median_mode.htm
    Mode <- function(v) {
       uniqv <- unique(v)
       uniqv[which.max(tabulate(match(v, uniqv)))]
    }
    mode<- t(as.data.frame(lapply(data, Mode)))
    
    # coefficient of variation
    
    coeff_of_variation<- t(as.data.frame(lapply(data, raster::cv)))
    
    #Pearson’s correlation coefficient 
    pearson_corr <- cor(as.matrix(data), method = c('pearson'))
    
    for (n in 1:ncol(pearson_corr)) {
        col_num = n
        colnames(pearson_corr)[col_num] <- paste("corr_", colnames(pearson_corr)[col_num])
    }
    
    ## Final stats summary table
        
     sts<- sts[, -6]
    
     colnames(sts)[2] <- "count"
     colnames(sts)[4] <- "std_dev"
     colnames(sts)[6] <- "median absolute deviation"
     colnames(sts)[12]<- "standard error"
    
     final_stats <- cbind(pearson_corr, sts, mode, coeff_of_variation)
    
     final_stats

}

