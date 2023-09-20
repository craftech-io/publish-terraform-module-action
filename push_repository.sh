#!/bin/bash

set -e 

AUTH='Authorization: Bearer '$API_KEY
DATA=./modules.zip

function log_error {
        local -ra message=("$@")
        echo "ERROR: ${message[@]}"
}

function log_info {
        local -ra message=("$@")
        echo "INFO: ${message[@]}"
}

function check_if_empty {
        if [ -z "$1" ]; then
                log_error "The '$2' cannot be empty"
        fi
}

check_if_empty $HOSTNAME "hostname"

if [[ ! "$HOSTNAME" =~ ^https://.*[^/]$ ]]; then
        log_error "The hostname '$HOSTNAME' is invalid."
fi

check_if_empty $API_KEY "API Key"
check_if_empty $NAMESPACE "namespace"
check_if_empty $NAME "name"
check_if_empty $VERSION "version"

if [ ! -d "$MODULES_PATH" ]; then
    log_error "The directory '$MODULES_PATH' does not exists."
fi

zip -r modules.zip $MODULE_PATH -x .git\* -x push_repository.sh
echo ''"$HOSTNAME"'/'"$NAMESPACE"'/'"$NAME"'/'"$SYSTEM"'/'"$VERSION"'/upload'
wget --no-check-certificate -v --method POST --timeout=0 --header "$AUTH" --header 'Content-Type: application/zip' \
        --body-file="$DATA" ''"$HOSTNAME"'/'"$NAMESPACE"'/'"$NAME"'/'"$SYSTEM"'/'"$VERSION"'/upload'
