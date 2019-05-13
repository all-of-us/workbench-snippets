install_and_load_all <- function() {
    # 1.Define list of packages (add more if needed)

    r_pkgs <- c("skimr", "qwraps2", "viridis", "ggthemes", "ggplot2", "pheatmap", "reticulate",
        "crayon", "RColorBrewer", "scales", "plyr", "dplyr", "tidyr", "lubridate", "raster",
        "reshape2", "formatR", "bigrquery", "psych")

    py_pkgs <- c("pandas", "google.cloud.storage")

    # 2.Install R packages, if not already installed
    install_if_missing <- function(packages) {
        if (length(setdiff(packages, rownames(installed.packages()))) > 0) {
            install.packages(setdiff(packages, rownames(installed.packages())))
        }
    }
    install_if_missing(packages = r_pkgs)

    # 3.Load all packages
        # '<<-' ensures the modules aliases can be used outside of the function
    lapply(r_pkgs, library, character.only = TRUE)
    storage <<- reticulate::import("google.cloud.storage")
    pd <<- reticulate::import("pandas")
      # If error message for google.cloud storage, run: system('pip3 install google.cloud.storage', intern = TRUE) in a R notebook; 
      # if error persists run: !pip3 install --upgrade google.cloud.storage, in a PY notebook and restart R notebook.

}  
