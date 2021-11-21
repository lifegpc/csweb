@echo off
SETLOCAL
set py=python
set pyt=%py% compile.py -W *
%pyt% captcha2.js xhr.js i18n.js sendMsgToMe.js
%pyt% -t salt.js xhr.js wplink.js i18n.js
%pyt% xhr.js instaVerify.js
%pyt% -o about.js xhr.js wplink.js
%pyt% tools/clearBlankLines.js
%pyt% -t tools/md_to_html.js
copy /Y node_modules\clipboard\dist\clipboard.min.js js\
COPY /Y js(origin)\*.wasm js\
ENDLOCAL
