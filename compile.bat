@echo off
SETLOCAL
set py=python
set pyt=%py% compile.py
%pyt% captcha2.js xhr.js i18n.js sendMsgToMe.js
%pyt% -t salt.js element.js xhr.js wplink.js i18n.js
%pyt% xhr.js instaVerify.js
%pyt% -o about.js xhr.js wplink.js
%pyt% tools/clearBlankLines.js
copy /Y node_modules\clipboard\dist\clipboard.min.js js\
copy /Y node_modules\js-sha512\build\sha512.min.js js\
ENDLOCAL
