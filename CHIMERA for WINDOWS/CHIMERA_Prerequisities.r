options(repos = c(CRAN = "https://cloud.r-project.org/"))

cran_packages <- c("dplyr", "httr", "jsonlite", "stringr", "remotes")

for (pkg in cran_packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg)
    print(paste(pkg, "has been successfully installed."))
  } else {
    print(paste(pkg, "is already available."))
  }
}

library(remotes)

if (!requireNamespace("ROhdsiWebApi", quietly = TRUE)) {
  remotes::install_github("OHDSI/ROhdsiWebApi", force = TRUE)
  print("ROhdsiWebApi has been successfully installed from GitHub.")
} else {
  print("ROhdsiWebApi is already available.")
}

if (!requireNamespace("Capr", quietly = TRUE)) {
  remotes::install_github("OHDSI/Capr", force = TRUE)
  print("Capr has been successfully installed from GitHub.")
} else {
  print("Capr is already available.")
}