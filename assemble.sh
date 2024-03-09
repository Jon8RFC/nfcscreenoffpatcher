#!/bin/sh
EXTRACT_DIR=$1
APK_NAME=$2

cd "$EXTRACT_DIR/"
SDK=$(grep '^SDK=' .env | cut -d'=' -f2)
if [ "$SDK" -gt 33 ]; then
	apktool_android14 b -f "$APK_NAME/" -o "${APK_NAME}_mod.apk"
else
	apktool_android13 b -f "$APK_NAME/" -o "${APK_NAME}_mod.apk"
fi
zipalign -v 4 "${APK_NAME}_mod.apk" "${APK_NAME}_align.apk"
