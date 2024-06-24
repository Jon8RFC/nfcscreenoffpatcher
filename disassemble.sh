#!/bin/sh
EXTRACT_DIR=$1
APK_NAME=$2

cd "$EXTRACT_DIR/" || exit 1
echo ""
echo ""
cat .env
echo ""
echo ""
SDK=$(grep '^SDK=' .env | cut -d'=' -f2)
if [ "$SDK" -gt 33 ]; then
	apktool_android14 if framework-res.apk
	apktool_android14 d -f "${APK_NAME}.apk" -o "${APK_NAME}/"
else
	apktool_android13 if framework-res.apk
	apktool_android13 d -f "${APK_NAME}.apk" -o "${APK_NAME}/"
fi
