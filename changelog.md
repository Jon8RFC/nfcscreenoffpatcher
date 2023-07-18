# Changelog

### v1.1.0 (jon8rfc) 2023-07-xx
#### ADD
* pre-patch verify: server connectivity (no upload waiting if down)
  * uses root index.html
* custom HTTP status response codes 545 & 555
  * CLEAR distinction between a possible patching failure and anything else, client-side
  * some textual feedback, client-side
* optional saving of failed-to-patch zip file for custom HTTP status codes failures (server.py)
* build.prop version/sdk for troubleshooting
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
* apktool from v2.6.2 (2022-12-09) to v2.8.0 (2023-07-17)
* dex2jar from pxb1988 v2.0 (2015-06-09) to ThexXTURBOXx v63 (2023-04-15)
* smali & baksmali from 2.5.2 (2021-03-03) to 3.0.3 (2023-04-27)
#### NOTES

---
### v1.0.0 (lapwat)  2022-12-09