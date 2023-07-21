#!/bin/sh
EXTRACT_DIR=$1
APK_NAME=$2

cd "$EXTRACT_DIR/"
unzip "$APK_NAME.apk" -d "$APK_NAME"
java -jar /app/baksmali.jar x -c arm64/boot.oat -d arm64 "$APK_NAME.odex" -o smali_classes
