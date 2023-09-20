#!/bin/bash

AUTH='Authorization: Bearer '$API_KEY
DATA=./modules.zip

function log_error {
        local -ra message=("$@")
        log "ERROR" "${message[@]}"
}

function log_info {
        local -ra message=("$@")
        log "INFO" "${message[@]}"
}

function chef_if_empty {
        if [ -z "$1" ]; then
                log_error "The '$2' cannot be empty"
        fi
}

check_if_empty $HOSTNAME "hostname"

if [[ "$HOSTNAME" =~ ^https://.*[^/]$ ]]; then
        log_info "The hostname '$HOSTNAME' is valid."
else
        log_error "The hostname '$HOSTNAME' is invalid."
fi

chef_if_empty $API_KEY "API Key"
chef_if_empty $NAMESPACE "namespace"
chef_if_empty $NAME "name"
chef_if_empty $VERSION "version"

if [ ! -d "$MODULES_PATH" ]; then
    log_error "The directory '$MODULES_PATH' does not exists."
fi

zip -r modules.zip $MODULE_PATH -x .git\* -x push_repository.sh
echo ''"$HOSTNAME"'/'"$NAMESPACE"'/'"$NAME"'/'"$SYSTEM"'/'"$VERSION"'/upload'
wget --no-check-certificate -v --method POST --timeout=0 --header "$AUTH" --header 'Content-Type: application/zip' \
        --body-file="$DATA" ''"$HOSTNAME"'/'"$NAMESPACE"'/'"$NAME"'/'"$SYSTEM"'/'"$VERSION"'/upload'
