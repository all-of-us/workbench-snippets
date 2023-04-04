library(httr)
library(jsonlite)
library(rprojroot)
library(glue)
library(stringr)

# Check for the CROMWELL app
check_for_app <- function(env) {
  list_apps_url <- glue("{env$leonardo_url}/api/google/v1/apps/{env$google_project}")

  res <- GET(
    url = list_apps_url,
    query = list(includeDeleted = "false"),
    add_headers(Authorization = paste("Bearer", env$token))
  )
  stop_for_status(res)

  for (potential_app in content(res, as = "parsed")) {
    if (potential_app$appType == "CROMWELL" &&
        (toString(potential_app$auditInfo$creator) == env$owner_email ||
         toString(potential_app$auditInfo$creator) == env$user_email)) {
      potential_app_name <- potential_app$appName
      potential_app_status <- potential_app$status

      # We found a CROMWELL app in the correct google project and owned by the user. Now just check the workspace:
      app_details <- get_app_details(env, potential_app_name)
      workspace_namespace <- app_details[[2]]
      proxy_url <- app_details[[3]]
      if (workspace_namespace == env$workspace_namespace) {
        return(list(potential_app_name, potential_app_status, proxy_url))
      }
    }
  }
  return(list(NULL, NULL, NULL))
}

# Get the details of the specified app
get_app_details <- function(env, app_name) {
  get_app_url <- glue("{env$leonardo_url}/api/google/v1/apps/{env$google_project}/{app_name}")

  res <- GET(
    url = get_app_url,
    query = list(includeDeleted = "true", role = "creator"),
    add_headers(Authorization = paste("Bearer", env$token))
  )
  if (status_code(res) == 404) {
    return(list("DELETED", NULL, NULL))
  } else {
    stop_for_status(res)
  }

  result_json <- content(res, as = "parsed")
  custom_environment_variables <- result_json$customEnvironmentVariables

  list(result_json$status, custom_environment_variables$WORKSPACE_NAMESPACE, result_json$proxyUrls)
}

# Check if cromshell is installed
validate_cromshell <- function() {
  cat('Scanning for correct cromshell version...\n')
  tryCatch({
    validate_cromshell_beta()
  }, error = function(e) {
    validate_cromshell_alpha()
  })
  return
}

validate_cromshell_alpha <- function() {
  cat('Scanning for cromshell 2 alpha..')
  tryCatch({
    system2('cromshell-alpha', args = 'version', stdout = TRUE, stderr = TRUE)
    cat('cromshell-alpha found\n')
  }, error = function(e) {
    cat('cromshell-alpha not found\n')
      stop(e)
  })

  return
}

validate_cromshell_beta <- function() {
  cat('Scanning for cromshell 2 beta...\n')
  tryCatch({
    system2('cromshell-beta', args = 'version', stdout = TRUE, stderr = TRUE)
    cat('cromshell-beta found')
  }, error = function(e) {
    stop(e)
  })
}

# Configure Cromwell
configure_cromwell <- function(env, proxy_url) {
  cat("Updating cromwell config\n")
  file_path <- file.path(path.expand("~"), ".cromshell", "cromshell_config.json")
  configuration <- list(
    cromwell_server = ifelse(!is.null(proxy_url), proxy_url, ""),
    requests_timeout = 5,
    gcloud_token_email = env$user_email,
    referer_header_url = env$leonardo_url
  )
  write(toJSON(configuration, auto_unbox = TRUE, pretty = TRUE), file_path)
}

# Find the status of the app
find_app_status <- function(env) {
  cat('Checking status for CROMWELL app\n')
  app_info <- check_for_app(env)
  app_name <- app_info[[1]]
  app_status <- app_info[[2]]
  proxy_url <- app_info[[3]]

  configure_cromwell(env, proxy_url)

  if (is.null(app_name)) {
    message('CROMWELL app does not exist. Please create cromwell server from workbench\n')
  } else {
    cat(sprintf('app_name=%s; app_status=%s\n', app_name, app_status))
    message(sprintf('Existing CROMWELL app found (app_name=%s; app_status=%s).\n', app_name, app_status))
    quit(save = "no", status = 1, runLast = FALSE)
  }
}

main <- function() {
  # Iteration 1: these ENV reads will throw errors if not set.
  env <- list(
    workspace_namespace = Sys.getenv('WORKSPACE_NAMESPACE'),
    workspace_bucket = Sys.getenv('WORKSPACE_BUCKET'),
    user_email = ifelse(is.null(Sys.getenv('PET_SA_EMAIL')), Sys.getenv('OWNER_EMAIL'), Sys.getenv('PET_SA_EMAIL')),
    owner_email = Sys.getenv('OWNER_EMAIL'),
    google_project = Sys.getenv('GOOGLE_PROJECT'),
    leonardo_url = Sys.getenv('LEONARDO_BASE_URL')
  )

  # Before going any further, check that cromshell2 is installed:
  validate_cromshell()

  # Fetch the token:
  token <- system2('gcloud', args = c("auth", "print-access-token"), stdout = TRUE)

  env['token'] <- token

  find_app_status(env)
}

 main()

