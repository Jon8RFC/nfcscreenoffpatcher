FROM anapsix/alpine-java:8 as sdkbuilder

RUN apk add --no-cache curl
RUN curl -sL https://dl.google.com/android/repository/sdk-tools-linux-3859397.zip -o /sdktools.zip
RUN mkdir -p /sdk/licenses
WORKDIR /sdk
RUN unzip -q /sdktools.zip
RUN echo 8933bad161af4178b1185d1a37fbf41ea5269c55 > /sdk/licenses/android-sdk-license
RUN yes | /sdk/tools/bin/sdkmanager --licenses
RUN /sdk/tools/bin/sdkmanager "build-tools;26.0.1"
WORKDIR /
RUN curl -sLO https://github.com/pxb1988/dex2jar/releases/download/2.0/dex-tools-2.0.zip
RUN unzip -q dex-tools-2.0.zip
RUN rm dex2jar-2.0/*.bat
RUN mkdir -p /export/lib/
#RUN curl -sL https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.6.1.jar > /export/apktool.jar
COPY apktool-2.6.2-9db742.jar /export/apktool.jar
RUN curl -sL https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool > /export/apktool
RUN cp -a /sdk/build-tools/26.0.1/apksigner /sdk/build-tools/26.0.1/zipalign /dex2jar-2.0/* /export/
RUN cp -a /sdk/build-tools/26.0.1/lib/apksigner.jar /export/lib/
RUN chmod a+x /export/d2j*.sh

FROM anapsix/alpine-java:8
RUN apk add --no-cache zip py-pip python3

RUN mkdir /dedroid/
COPY --from=sdkbuilder /export /dedroid/
COPY --from=sdkbuilder /sdk/build-tools/26.0.1/lib64/libc++.so /lib64/
RUN chmod a+x /dedroid/apktool
ENV PATH=/dedroid/:$PATH

WORKDIR /app/

ADD requirements.txt . 
RUN pip3 install -r requirements.txt

RUN wget -O baksmali.jar https://bitbucket.org/JesusFreke/smali/downloads/baksmali-2.5.2.jar
RUN wget -O smali.jar https://bitbucket.org/JesusFreke/smali/downloads/smali-2.5.2.jar
ADD server.py patcher.py disassemble.sh assemble.sh disassemble_odex.sh assemble_odex.sh free-space.sh ./

EXPOSE 8000
CMD ["python3", "server.py"]
