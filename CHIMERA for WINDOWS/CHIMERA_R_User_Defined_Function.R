##################
# Common arguments
##################
args <- commandArgs(trailingOnly = TRUE)
function_to_call <- args[1]
atlas_user_name <- args[3]
atlas_password <- args[4]
 
#########################################################
# Additional arguments based on the function to be called
#########################################################
if (function_to_call == "postConceptSet") {
  dataframe_csv_file <- args[2]
  output_directory <- args[5]
  base_url <- args[6]
} else if (function_to_call == "checkConceptSet") {
  concept_set_name <- args[2]
  base_url <- args[5]
} else if (function_to_call == "conceptSetMetadata") {
  flag_metadata <- args[2]
  base_url <- args[5]
} else if (function_to_call == "deleteConceptSet") {
  conceptSetId <- args[2]
  base_url <- args[5]
} else if (function_to_call == "authorize_web_api") {
  base_url <- args[2]
}
 
#########################
# Load required libraries
#########################
library(httr)
library(remotes)
library(ROhdsiWebApi)
library(jsonlite)
library(Capr)
library(dplyr)
library(stringr)

#######################
# Authorize the Web API
#######################
authorize_web_api <- function(base_url, username, password) {
  httr::set_config(config(ssl_verifypeer = 0L))
  tryCatch({
    ROhdsiWebApi::authorizeWebApi(
      baseUrl = base_url,
      authMethod = "windows",
      webApiUsername = username,
      webApiPassword = password
    )
  }, error = function(e) {
    cat("Error in authorizing WebAPI:", e$message, "\n")
    stop("Authorization failed")
  })
}
 
###########################
# Generate concept set name
###########################
generate_concept_set_name <- function(username, group_identifier) {
  prefix <- "CHI"
  first_two_letters <- substr(username, 1, 2)
  last_two_letters <- substr(username, nchar(username) - 1, nchar(username))
  concept_set_name <- paste(prefix, first_two_letters, last_two_letters, group_identifier, sep = "_")
  return(concept_set_name)
}
 
##################################################
# Check if a given concept set name already exists
##################################################
checkConceptSet <- function(concept_set_name, atlasUsername, atlasPassword, base_url) {
  
  authorize_web_api(base_url, atlasUsername, atlasPassword)
  tryCatch({
    #WebAPI
    result <- ROhdsiWebApi::existsConceptSetName(
      conceptSetName = concept_set_name, 
      baseUrl = base_url
      )
    resultdataframe <- as.data.frame(result)
    result_string <- paste(capture.output(write.csv(resultdataframe, row.names = FALSE)), collapse = "\n")
    cat(result_string)
  }, error = function(e) {
    cat("Error:", e$message, "\n")
    stop("Issue occured while calling the API. Try Again!")
  })
}
 
####################
# Create Concept Set
####################
postConceptSet <- function(data, atlasUsername, atlasPassword, output_directory, base_url) {
  
  # Inclusion list for Final_flag == 1
  inclusion_list <- data %>%
    filter(Final_Flag == 1) %>%
    pull(concept_id) %>%
    paste(collapse = ",")
  
  # Descendants list for Final_flag == 2
  descendants_list <- data %>%
    filter(Final_Flag == 2) %>%
    pull(concept_id) %>%
    paste(collapse = ",")
  
  # Exclusion list for Final_flag == 3
  exclusion_list <- data %>%
    filter(Final_Flag == 3) %>%
    pull(concept_id) %>%
    paste(collapse = ",")
  
  # Concept Id List
  concept_id_list <- cs(as.numeric(unlist(strsplit(inclusion_list, ","))), exclude(as.numeric(unlist(strsplit(exclusion_list, ",")))), descendants(as.numeric(unlist(strsplit(descendants_list, ",")))), name = "concept_id_list")
  
  # Define name of the concept set
  group_identifier <- data$sheet_name[1]
  concept_set_name <- generate_concept_set_name(atlasUsername, group_identifier)
  
  # File path to store the json file of concept set
  filename <- paste(concept_set_name, ".json", sep = "")
  filepath <- file.path(output_directory, filename)
  rExpression <- writeConceptSet(concept_id_list, filepath)
  
  # Load the JSON file
  res <- fromJSON(filepath)
  
  # Connecting to ATLAS
  authorize_web_api(base_url, atlasUsername, atlasPassword)
  
  # Ensure all rows and columns are printed
  options(tibble.width = Inf)
  options(dplyr.print_min = Inf)
  
  # Post Concept Set Definition
  tryCatch({
    #WebAPI
    result <- ROhdsiWebApi::postConceptSetDefinition(
      name = concept_set_name,
      conceptSetDefinition = res,
      baseUrl = base_url
    )
    
    resultdataframe <- as.data.frame(result)
    result_string <- paste(capture.output(write.csv(resultdataframe, row.names = FALSE)), collapse = "\n")
    cat(result_string)
  }, error = function(e) {
    cat("Error posting Concept Set Definition:", e$message, "\n")
    stop("Post Concept Set Definition failed")
  })
}

##########################
# Metadata of Concept Sets
##########################
conceptSetMetadata <- function(atlasUsername, atlasPassword, base_url) {

  authorize_web_api(base_url, atlasUsername, atlasPassword)

  tryCatch({
    metadata_data <- ROhdsiWebApi::getConceptSetDefinitionsMetaData(baseUrl = base_url)
    metadata_dataframe <- as.data.frame(metadata_data) %>% 
                          mutate(author_createdBy = sapply(createdBy, function(x) x$name),
                          author_modifiedBy = sapply(modifiedBy, function(x) x$name)) %>% 
                          select(id, name, author_createdBy, createdDate, author_modifiedBy, modifiedDate, description, hasWriteAccess, hasReadAccess) %>% 
                          distinct()
    metadata_string <- paste(capture.output(write.csv(metadata_dataframe, row.names = FALSE)), collapse = "\n")
    cat(metadata_string)  
  }, error = function(e) {
    cat("Error in extracting metadata of Concept-Sets:", e$message, "\n")
    stop("Metadata extraction failed")
  })

}

#####################
# Delete Concept Sets
#####################
deleteConceptSet <- function(conceptSetId, atlasUsername, atlasPassword, base_url) {

  authorize_web_api(base_url, atlasUsername, atlasPassword)
  
  tryCatch({
    conceptSetId <- as.integer(conceptSetId)
    delete <- ROhdsiWebApi::deleteConceptSetDefinition(
      conceptSetId= conceptSetId, 
      baseUrl = base_url
      ) 
    deletedataframe <- as.data.frame(delete)
    delete_string <- paste(capture.output(write.csv(deletedataframe, row.names = FALSE)), collapse = "\n")
    cat(delete_string)
  }, error = function(e) {
    cat("Error in deleting Concept-Set Definition (ID:", conceptSetId, "):", e$message, "\n")
    stop("Delete Concept Set Definition failed")
  })
}


###########################
# Call appropriate function
###########################
if (function_to_call == "postConceptSet") {
  
  if (file.exists(dataframe_csv_file)) {
    data <- read.csv(dataframe_csv_file)
    if (nrow(data) == 0) {
      stop("Error: The specified CSV file is empty.")
    }
    postConceptSet(data, atlas_user_name, atlas_password, output_directory, base_url)
  } else {
    stop("Error: The specified CSV file does not exist.")
  }
  
} else if (function_to_call == "checkConceptSet") {
  
  checkConceptSet(concept_set_name, atlas_user_name, atlas_password, base_url)
  
} else if (function_to_call == "conceptSetMetadata") {
  
  conceptSetMetadata(atlas_user_name, atlas_password, base_url)
  
} else if (function_to_call == "deleteConceptSet") {
  
  deleteConceptSet(conceptSetId, atlas_user_name, atlas_password, base_url)
  
} else if (function_to_call == "authorize_web_api") {

  authorize_web_api(base_url, atlas_user_name, atlas_password)

}
else {
  
  stop("Invalid function name provided")
  
}

