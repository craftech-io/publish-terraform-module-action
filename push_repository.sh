#!/bin/bash

set -e 

AUTH='Authorization: Bearer '$API_KEY
DATA=./modules.zip

function log_error {
        echo "ERROR: $1"
        exit 1
}

if [[ ! "$HOSTNAME" =~ ^https://.*[^/]$ ]]; then
        log_error "The hostname '$HOSTNAME' is invalid."
fi

if [ -z "$HOSTNAME" ]; then
        log_error "The hostname cannot be empty"
fi

if [ -z "$API_KEY" ]; then
        log_error "The API Key cannot be empty"
fi

if [ -z "$NAMESPACE" ]; then
        log_error "The namespace cannot be empty"
fi

if [ -z "$NAME" ]; then
        log_error "The name cannot be empty"
fi

if [ -z "$VERSION" ]; then
        log_error "The version cannot be empty"
fi

if [ ! -d "$MODULES_PATH" ]; then
        log_error "The directory '$MODULES_PATH' does not exists."
fi

if [ -n "$LOWER_TERRAFORM_VERSION" ] && [ -n "$HIGHER_TERRAFORM_VERSION"]; then
python3 /terraform_required_versions.py
fi

echo 'The terraform required versions are compliant with the desired version range.'

zip -r modules.zip $MODULES_PATH -x .git\* -x push_repository.sh -x terraform_required_versions.py
# echo ''"$HOSTNAME"'/'"$NAMESPACE"'/'"$NAME"'/'"$SYSTEM"'/'"$VERSION"'/upload'
# wget --no-check-certificate -v --method POST --timeout=0 --header "$AUTH" --header 'Content-Type: application/zip' \
#         --body-file="$DATA" ''"$HOSTNAME"'/'"$NAMESPACE"'/'"$NAME"'/'"$SYSTEM"'/'"$VERSION"'/upload'
