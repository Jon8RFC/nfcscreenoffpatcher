#!/bin/sh
EXTRACT_DIR=$1
APK_NAME=$2
SMALI_PATH="$APK_NAME/smali/com/android/nfc/NfcService.smali"

cd "$EXTRACT_DIR/"

# decompile
apktool if framework-res.apk
apktool d -f "$APK_NAME.apk" -o "$APK_NAME/"

# mod
sed -e '/.*if-lt.*/s/^/#/g' -i "$SMALI_PATH"
grep -n -A4 -B4 if-lt "$SMALI_PATH" | tail -9 | sed -e 's/[^0-9].*$//' -e 's/$/s|^|#|/' | sed -i -f- "$SMALI_PATH"
sed 's/SCREEN_OFF/SCREEN_OFF_DISABLED/' -i "$SMALI_PATH"
sed 's/SCREEN_ON/SCREEN_ON_DISABLED/' -i "$SMALI_PATH"
sed 's/USER_PRESENT/USER_PRESENT_DISABLED/' -i "$SMALI_PATH"
sed 's/USER_SWITCHED/USER_SWITCHED_DISABLED/' -i "$SMALI_PATH"

# build
apktool b -f "$APK_NAME/" -o "${APK_NAME}_mod.apk"
# keytool -genkey -v -keystore ~/.android/debug.keystore -storepass android -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000
# jarsigner -verbose -sigalg MD5withRSA -digestalg SHA1 -keystore ~/.android/debug.keystore -storepass android "${APK_NAME}_mod.apk" androiddebugkey
zipalign -v 4 "${APK_NAME}_mod.apk" "${APK_NAME}_align.apk"

# clean
#ls | grep -v "${APK_NAME}_align.apk" | xargs rm -r