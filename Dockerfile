FROM anapsix/alpine-java:8

RUN apk add --no-cache curl zip py-pip python3 && \
mkdir -p /dedroid/lib/ /dedroid/lib64/ /lib64/ && \
curl -sL https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool > /dedroid/apktool && \
# get below new URL versions from:
# https://androidsdkmanager.azurewebsites.net/Buildtools
# https://github.com/iBotPeaches/Apktool/releases/
# https://github.com/ThexXTURBOXx/dex2jar/releases/
curl -sL https://dl.google.com/android/repository/build-tools_r34-rc4-linux.zip -o buildtools.zip && \
curl -sL https://github.com/iBotPeaches/Apktool/releases/download/v2.8.1/apktool_2.8.1.jar -o /dedroid/apktool.jar && \
#curl -k --digest -sL http://127.0.0.1/androidtools/apktool-cli-all.jar -o /dedroid/apktool.jar && \
curl -sL https://github.com/ThexXTURBOXx/dex2jar/releases/download/v72/dex-tools-2.1-SNAPSHOT.zip -o dextools.zip && \
unzip -q dextools.zip -d /dextools/ && \
unzip -q buildtools.zip -d /buildtools/ && \
rm /dextools/*/*.bat && \
cp -a /dextools/*/* /buildtools/*/apksigner /buildtools/*/zipalign /dedroid/ && \
cp -a /buildtools/*/lib/apksigner.jar /dedroid/lib/ && \
cp -a /buildtools/*/lib64/libc++.so /dedroid/lib64/ && \
cp -a /buildtools/*/lib64/libc++.so /lib64/ && \
chmod a+x /dedroid/d2j*.sh /dedroid/apktool && \
rm -r /dextools/ /buildtools/ dextools.zip buildtools.zip
ENV PATH=/dedroid/:$PATH

WORKDIR /app/

ADD requirements.txt server.py patcher.py disassemble.sh assemble.sh disassemble_odex.sh assemble_odex.sh free-space.sh ./
# get below new URL versions from:
# https://maven.google.com/web/index.html#com.android.tools.smali
RUN pip3 install -r requirements.txt && \
wget -O baksmali.jar https://dl.google.com/android/maven2/com/android/tools/smali/smali-baksmali/3.0.3/smali-baksmali-3.0.3.jar && \
wget -O smali.jar https://dl.google.com/android/maven2/com/android/tools/smali/smali/3.0.3/smali-3.0.3.jar

EXPOSE 8000
CMD ["python3", "server.py"]
