#!/bin/bash -e
# Checks out RDR code from git in the current directory; by default, uses the same version of the
# app that is currently running in the staging environment.
# After a Y/N confirmation, upgrades the database, installs the latest config, deploys the code
# and crons, or just the cron+queue config. By default, does all of the above.

# Run this in the rest-api dir of the git repo with no uncommitted changes. You will need to
# check out whatever branch you want to work in after it's done.

. tools/set_path.sh

TARGET="all"

while true; do
  case "$1" in
    --account) ACCOUNT=$2; shift 2;;
    --project) PROJECT=$2; shift 2;;
    --version) VERSION=$2; shift 2;;
    --deploy_as_version) DEPLOY_AS_VERSION=$2; shift 2;;
    --target) TARGET=$2; shift 2;;
    --use_prod_yaml) USE_PROD_YAML='true'; shift 1;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done

function usage {
  echo "Usage: deploy_app.sh --project all-of-us-rdr-stable --account $USER@pmi-ops.org \\"
  echo "    [--target app|db|config|cron|all] [--version GIT_REF] [--deploy_as_version APPENGINE_VERSION]"
  exit 1
}

if [ -z "${PROJECT}" ]
then
  echo "Missing required --project flag."
  usage
fi

if [[ $(git status --porcelain) ]]; then
  # Changes
  echo "git status must be clean"
  EXIT 1
fi

UPDATE_TRACKER=tools/update_release_tracker.py
if [ "${PROJECT}" == "all-of-us-rdr-prod" ]
then
  CONFIG="config/config_prod.json"
elif [ "${PROJECT}" == "all-of-us-rdr-stable" ]
then
  CONFIG="config/config_stable.json"
elif [ "${PROJECT}" == "all-of-us-rdr-staging" ]
then
  CONFIG="config/config_staging.json"
elif [ "${PROJECT}" == "pmi-drc-api-test" ]
then
  CONFIG="config/config_test.json"
  echo "Skipping JIRA tracker updates for Test."
  UPDATE_TRACKER=echo

elif [ "${PROJECT}" == "all-of-us-rdr-sandbox" ]
then
  CONFIG="config/config_sandbox.json"
  echo "Skipping JIRA tracker updates for Sandbox."
  UPDATE_TRACKER=echo
elif [ "${PROJECT}" == "all-of-us-rdr-ptsc-1-test" ]
then
  CONFIG="config/config_test_ptsc_1.json"
  echo "Skipping JIRA tracker updates for PTSC Test 1."
  UPDATE_TRACKER=echo
elif [ "${PROJECT}" == "all-of-us-rdr-ptsc-2-test" ]
then
  CONFIG="config/config_test_ptsc_2.json"
  echo "Skipping JIRA tracker updates for PTSC Test 2."
  UPDATE_TRACKER=echo
elif [ "${PROJECT}" == "all-of-us-rdr-ptsc-3-test" ]
then
  CONFIG="config/config_test_ptsc_3.json"
  echo "Skipping JIRA tracker updates for PTSC Test 3."
  UPDATE_TRACKER=echo
elif [ "${PROJECT}" == "all-of-us-rdr-careevo-test" ]
then
  CONFIG="config/config_test_careevo.json"
  echo "Skipping JIRA tracker updates for Care Evolution Test."
  UPDATE_TRACKER=echo
else
  echo "Unsupported project: ${PROJECT}; exiting."
  usage
fi

if [ -z "${ACCOUNT}" ]
then
  echo "Missing required --account flag."
  usage
fi

if [ "$TARGET" != "all" ] && [ "$TARGET" != "app" ] && [ $TARGET != "db" ] && [ $TARGET != "config" ] && [ "$TARGET" != "cron" ]
then
  echo "Target must be one of: all, app, db, config, cron. Exiting."
  usage
fi

gcloud auth login $ACCOUNT
if [ -z "${VERSION}" ]
then
  VERSION=`gcloud app versions --project all-of-us-rdr-staging list | grep default | grep " 1.00" | tr -s ' ' | cut -f2 -d" "`
  if [ -z "${VERSION}" ]
  then
    echo "App version for $PROJECT could not be determined; exiting."
    usage
  fi
fi
if [ -z ${DEPLOY_AS_VERSION} ]
then
  DEPLOY_AS_VERSION="$VERSION"
fi

BOLD=$(tput bold)
NONE=$(tput sgr0)

echo "Project: ${BOLD}$PROJECT${NONE}"
echo "Source Version: ${BOLD}$VERSION${NONE}"
echo "Target Version: ${BOLD}$DEPLOY_AS_VERSION${NONE}"
echo "Target: ${BOLD}$TARGET${NONE}"
read -p "Are you sure? (Y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
  echo "Exiting."
  exit 1
fi

echo "${BOLD}Checking out code...${NONE}"
git checkout $VERSION

if [[ $(git status --porcelain) ]]; then
  # Changes
  echo "git status must be clean"
  EXIT 1
fi

if [ "$TARGET" == "all" ] || [ "$TARGET" == "db" ]
then
  echo "${BOLD}Upgrading database...${NONE}"
  $UPDATE_TRACKER --version $VERSION --comment "Upgrading database for ${PROJECT}."
  tools/upgrade_database.sh --project $PROJECT --account $ACCOUNT
  $UPDATE_TRACKER --version $VERSION --comment "Database for ${PROJECT} upgraded."

  echo "Updating BigQuery rdr_ops_data_view dataset..."
  if [ -z "${SERVICE_ACCOUNT}" ]
  then
    case "${PROJECT}" in
        "pmi-drc-api-test" | "all-of-us-rdr-staging")
            SERVICE_ACCOUNT="circle-deploy@all-of-us-rdr-staging.iam.gserviceaccount.com"
            ;;
        *)
            SERVICE_ACCOUNT="configurator@${PROJECT}.iam.gserviceaccount.com"
            ;;
    esac
  fi
#  python -m tools migrate-bq --project ${PROJECT} --service-account ${SERVICE_ACCOUNT}
#  $UPDATE_TRACKER --version $VERSION --comment "BigQuery dataset rdr_ops_data_view for ${PROJECT} upgraded."
fi

if [ "$TARGET" == "all" ] || [ "$TARGET" == "config" ]
then
  echo "${BOLD}Updating configuration...${NONE}"
  $UPDATE_TRACKER --version $VERSION --comment "Updating config for ${PROJECT}."
  tools/install_config.sh --project $PROJECT --account $ACCOUNT --config $CONFIG --update
  $UPDATE_TRACKER --version $VERSION --comment "Config for ${PROJECT} updated."
fi

if [ "$TARGET" == "all" ] || [ "$TARGET" == "app" ] || [ "$TARGET" == "cron" ]
then

  if [[ $(git status --porcelain) ]]; then
    # Changes
    echo "git status must be clean"
    EXIT 1
  fi

  declare -a yamls
  declare -a tmp_files

  # Deploy cron/queue in all cases.
  tools/build_cron_yaml.py --project ${PROJECT} > ../cron.yaml
  cd ..
  cp rdr_service/queue.yaml .
  cp rdr_service/offline.yaml .
  cp rdr_service/index.yaml .
  yamls+=( cron.yaml queue.yaml )
  tmp_files+=( cron.yaml queue.yaml offline.yaml index.yaml)
  before_comment="Updating cron/queue configuration in ${PROJECT}."
  after_comment="cron/queue configuration updated in ${PROJECT}."

  if [ "$TARGET" == "app" ] || [ "$TARGET" == "all" ]
  then
    if [ "${PROJECT}" = "all-of-us-rdr-prod" ] || [ "${USE_PROD_YAML}" = "true" ]
    then
      echo "Using ${BOLD}prod${NONE} app.yaml for project $PROJECT."
      APP_YAML=rdr_service/app_prod.yaml
    elif [ "${PROJECT}" = "all-of-us-rdr-stable" ]
    then
      echo "Using ${BOLD}stable${NONE} app.yaml for project $PROJECT."
      APP_YAML=rdr_service/app_stable.yaml
    else
      APP_YAML=rdr_service/app_nonprod.yaml
    fi
    cat rdr_service/app_base.yaml $APP_YAML > app.yaml

    yamls+=( app.yaml index.yaml offline.yaml )
    tmp_files+=( app.yaml cron.yaml)
    before_comment="Deploying app to ${PROJECT}."
    after_comment="App deployed to ${PROJECT}."
  fi

  echo "${BOLD}Deploying application...${NONE}"
  $UPDATE_TRACKER --version $VERSION --comment "${before_comment}"
  gcloud app deploy "${yamls[@]}" \
      --quiet --project "$PROJECT" --version "$DEPLOY_AS_VERSION"
  $UPDATE_TRACKER --version $VERSION --comment "${after_comment}"
  rm "${tmp_files[@]}"
fi

test_request=$(curl -s https://${PROJECT}.appspot.com/rdr/v1/ | grep version_id)
if [[ -z "$test_request" ]];
then
  echo "${BOLD}Test request failed to return the expected response, something may be wrong with
       the deployment${NONE}"
  $UPDATE_TRACKER --version $VERSION --comment "!!!!!!REQUEST FAILURE!!!!!! Test request failed to return a valid response."
else
  echo "Test request succeeded !"
  $UPDATE_TRACKER --version $VERSION --comment "Test request received a valid response."
fi
echo "${BOLD}Done!${NONE}"
