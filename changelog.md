# Changelog

### v1.1.1 (jon8rfc) 2023-10-19
#### FIX
* v1.0.0 http status 200 from disallowing a failure state to report
* Android 13 and prior fix for disappearing NFC setting and eventual screen off dysfunction
#### ADD
* Android 14 support
* custom HTTP status response code 535 if a known incompatibility exists
  * since I can't yet figure out textual responses from within a failed upload process
#### CHANGE
* 
#### UPDATE
* apktool to v2.9.0
* dex2jar to v74
#### NOTES

---
### v1.1.0 (jon8rfc) 2023-09-06
#### ADD
* pre-patch verify: server connectivity (no upload waiting if down)
* custom HTTP status response codes 545 & 555 (server.py & NFCScreenOff Magisk module v2.0.0+ customize.sh)
  * distinction between patching failure and anything else (server.py & customize.sh)
  * optional textual messages with abort/resume functionality within module (server.py & customize.sh)
* optional saving of failed-to-patch zip file for custom HTTP status codes failures (server.py)
* build.prop version/sdk and module version, for troubleshooting
* simple landing/home page
#### CHANGE
* save client-side UNIX date as "DATE_ID" in stats.csv, replacing/unifying server-side UNIX date instead of "timestamp"
  * improves troubleshooting when someone shares info with their DATE_ID
* Android SDK tools to standalone build tools (for zipalign & apksigner)
* dex2jar from pxb1988 repo to ThexXTURBOXx repo
* smali & baksmali from JesusFreke repo to Google repo
* dockerfile update/refactor/rearrange
  * comments/notes for update URLs
#### UPDATE
* smali folders to include smali_classes4 through smali_classes9
* Android build tools from rev 26.0.1 (Jul 2017) to rev 34.0.0 rc4 (May 2023)
* apktool from v2.6.2 (2022-12-09) to v2.8.1 (2023-07-22)
* dex2jar from pxb1988 v2.0 (2015-06-09) to ThexXTURBOXx v72 (2023-09-04)
* smali & baksmali from v2.5.2 (2021-03-03) to v3.0.3 (2023-04-27)
#### NOTES

---
### v1.0.0 (lapwat)  2022-12-09
