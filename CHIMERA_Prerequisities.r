options(repos = c(CRAN = "https://cloud.r-project.org/"))

install.packages(c("dplyr", "httr", "jsonlite", "stringr", "remotes"))

# Load the remotes package
library(remotes)

# Install GitHub packages
remotes::install_github("OHDSI/ROhdsiWebApi", force= TRUE)
remotes::install_github("OHDSI/Capr", force = TRUE)

