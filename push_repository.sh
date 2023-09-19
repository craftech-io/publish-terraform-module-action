AUTH='Authorization: Bearer '$API_KEY
DATA=`PWD`/module.zip
zip -r module.zip $PATH -x .git\* -x push_repository.sh
echo ''"$HOSTNAME"'/'"$NAMESPACE"'/'"$NAME"'/'"$SYSTEM"'/'"$VERSION"'/upload'
wget --no-check-certificate -v --method POST --timeout=0 --header "$AUTH" --header 'Content-Type: application/zip' \
        --body-file="$DATA" ''"$HOSTNAME"'/'"$NAMESPACE"'/'"$NAME"'/'"$SYSTEM"'/'"$VERSION"'/upload'
