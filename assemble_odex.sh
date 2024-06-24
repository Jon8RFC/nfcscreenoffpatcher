#!/bin/sh
EXTRACT_DIR=$1
APK_NAME=$2

cd "$EXTRACT_DIR/" || exit 1
java -jar /app/smali.jar a smali_classes -o "$APK_NAME/classes.dex"
cd "$APK_NAME" || exit 1
zip -r "../${APK_NAME}_mod.apk" *
cd .. || exit 1
zipalign -v 4 "${APK_NAME}_mod.apk" "${APK_NAME}_align.apk"
