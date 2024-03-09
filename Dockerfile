FROM anapsix/alpine-java:8

RUN apk add --no-cache curl zip py-pip python3 && \
mkdir -p /dedroid/lib/ /dedroid/lib64/ /lib64/ /app/ && \
# get below new URL versions from:
# https://androidsdkoffline.blogspot.com/p/android-sdk-build-tools.html
# https://maven.google.com/web/index.html#com.android.tools.smali
# https://github.com/iBotPeaches/Apktool/releases/
# https://github.com/ThexXTURBOXx/dex2jar/releases/
curl -sL https://dl.google.com/android/repository/build-tools_r34-linux.zip -o buildtools.zip && \
curl -sL https://dl.google.com/android/maven2/com/android/tools/smali/smali-baksmali/3.0.3/smali-baksmali-3.0.3.jar -o /app/baksmali.jar && \
curl -sL https://dl.google.com/android/maven2/com/android/tools/smali/smali/3.0.3/smali-3.0.3.jar -o /app/smali.jar && \
curl -sL https://github.com/iBotPeaches/Apktool/releases/download/v2.8.1/apktool_2.8.1.jar -o /dedroid/apktool_android13.jar && \
curl -sL https://github.com/iBotPeaches/Apktool/releases/download/v2.9.2/apktool_2.9.2.jar -o /dedroid/apktool_android14.jar && \
curl -sL https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool > /dedroid/apktool && \
curl -sL https://github.com/ThexXTURBOXx/dex2jar/releases/download/2.4.15/dex-tools-2.4.15.zip -o dextools.zip && \
cp /dedroid/apktool /dedroid/apktool_android13 && \
python3 -c "lines = [line.replace('apktool.jar', 'apktool_android13.jar') for line in open('/dedroid/apktool_android13').readlines()]; open('/dedroid/apktool_android13', 'w').writelines(lines)" && \
cp /dedroid/apktool /dedroid/apktool_android14 && \
python3 -c "lines = [line.replace('apktool.jar', 'apktool_android14.jar') for line in open('/dedroid/apktool_android14').readlines()]; open('/dedroid/apktool_android14', 'w').writelines(lines)" && \
unzip -q dextools.zip -d /dextools/ && \
unzip -q buildtools.zip -d /buildtools/ && \
rm /dextools/*/*.bat /dextools/*/*/*.bat /dextools/*/*.txt /dedroid/apktool && \
cp -a /dextools/*/* /buildtools/*/apksigner /buildtools/*/zipalign /dedroid/ && \
cp -a /buildtools/*/lib/apksigner.jar /dedroid/lib/ && \
cp -a /buildtools/*/lib64/libc++.so /dedroid/lib64/ && \
cp -a /buildtools/*/lib64/libc++.so /lib64/ && \
chmod a+x /dedroid/d2j*.sh /dedroid/apktool* /app/*smali.jar && \
rm -r /dextools/ /buildtools/ dextools.zip buildtools.zip
ENV PYTHONUNBUFFERED=1
ENV PATH=/dedroid/:$PATH

WORKDIR /app/
ADD requirements.txt server.py patcher.py disassemble.sh assemble.sh disassemble_odex.sh assemble_odex.sh free-space.sh ./
RUN pip3 install -r requirements.txt

EXPOSE 8000
CMD ["python3", "server.py"]
