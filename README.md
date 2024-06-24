# Start Jon8RFC's readme portion
## Docker setup on Windows
I use this batch file I made to keep things simple and quick:
https://github.com/Jon8RFC/nfcscreenoffpatcher/blob/master/container_setup.bat
You can do steps 1-2, then use the batch file.

1. Install Docker, update WSL if instructed
   * 🟥 **do _NOT_** click on restart when Docker prompts--close applications and use the start menu to restart! 🟥
2. Download and unzip this repo
3. Run in cmd ```docker build --no-cache "C:\nfcscreenoffpatcher-master" -t patcher/patcher:latest``` _(builds, names, tags the image)_
4. Run in cmd ```docker run -p 8000:8000 --name patcher patcher/patcher``` _(binds the port, creates & starts the container)_
5. Stop the container in Docker _(unsure if it gracefully closes from cmd)_
6. Run in cmd ```docker builder prune``` _(cleans up remnants/junk from any vestigial or failed builds)_
7. Start the container in Docker whenever you want it
   * (optional) Run in cmd ```docker update --restart always patcher``` _(starts the container when you run docker)_  

File locations of WSL and Docker configs:  
```"C:\Users\%USERNAME%\.wslconfig"```  
```"C:\Users\%USERNAME%\AppData\Roaming\Docker\settings.json"```  
You'd create .wslconfig yourself, maybe with:  
```
[wsl2]
memory=4GB
processors=8
#swap=0 #swap memory max, defaults to 25% of memory size on Windows rounded up to the nearest GB
```
### NFCScreenOff magisk module
Edit the customize.sh file's PATCH_URL to your computer's IP running the Docker patcher, such as: ```http://192.168.1.30:8000```

### Manual apk viewing
I like apktool and notepad++, but you can use dex2jar and something like [JD-GUI](http://java-decompiler.github.io/) ([github](https://github.com/java-decompiler/jd-gui)) for a different and conglomerated viewing of the decompiled apk.  
* Run in cmd ```apktool d NfcNci.apk```, then edit files in text viewer  
* Run in cmd ```d2j-dex2jar.bat -f -o NfcNci.jar NfcNci.apk```, then open in JD-GUI  

⠀⠀
⠀⠀
⠀⠀
# Start [Lapwat's NfcScreenOffPie readme](https://github.com/lapwat/NfcScreenOffPie/) from 2019-11-15:
# Tools
- adb
- apktool
- smali / baksmali v2.3+
- zip / unzip
- zipalign
- jarsigner

Enable ADB on phone in developper options.

# Decompile process

```sh
# copy original sources
$ adb pull /system/app/NfcNci/NfcNci.apk
$ adb pull /system/framework/framework-res.apk

# create a backup for recovery
$ cp NfcNci.apk NfcNci_bak.apk

# decompile
$ apktool d -f NfcNci.apk -o NfcNci/
```
# Modding

This is the part where you reverse engineer the source code of the app by modifying smali files.

For NfcNci, apply [those changes](https://github.com/lapwat/NfcScreenOffPie/commit/42df7a757535490f6219ded761f42e0120031033).

Files to edit are located at:
- NfcNci/smali/com/android/nfc/NfcService.smali
- NfcNci/smali/com/android/nfc/ScreenStateHelper.smali


# Compile process

```sh
# load framework
$ apktool if framework-res.apk

# compile
$ apktool b -f NfcNci/ -o NfcNci_mod.apk

# sign
$ keytool -genkey -v -keystore ~/.android/debug.keystore -storepass android -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000
$ jarsigner -verbose -sigalg MD5withRSA -digestalg SHA1 -keystore ~/.android/debug.keystore -storepass android NfcNci_mod.apk androiddebugkey

# align
zipalign -v 4 NfcNci_mod.apk NfcNci_align.apk
```

# Load modded APK on your phone

```sh
adb push NfcNci_align.apk /sdcard/
adb shell

# android shell
su
cd /system/app/NfcNci
busybox mount -o remount,rw $PWD
cp /sdcard/NfcNci_align.apk NfcNci.apk
chmod 644 NfcNci.apk
```

# Something went wrong?

You can restore the original APK file at any time with those commands.

```sh
adb push NfcNci_bak.apk /sdcard/
adb shell

# android shell
su
cd /system/app/NfcNci
busybox mount -o remount,rw $PWD
cp /sdcard/NfcNci_bak.apk NfcNci.apk
chmod 644 NfcNci.apk
```

# Sources

Java versions of smali files for reverse engineering

https://android.googlesource.com/platform/packages/apps/Nfc/+/refs/tags/android-9.0.0_r48/src/com/android/nfc/

Big up to Lasse Hyldahl Jensen for his version for Android N

https://lasse-it.dk/2017/01/how-to-modifying-nfcnci-apk-to-run-when-screen-is-turned-off-on-android-nougat/

Understanding the signing process

https://reverseengineering.stackexchange.com/a/9185
