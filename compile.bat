@echo off
SETLOCAL
set py=python
set pyt=%py% compile.py -W *
%pyt% -t sendMsgToMe.js captcha2.js xhr.js
%pyt% -t salt.js xhr.js wplink.js
%pyt% xhr.js instaVerify.js
%pyt% -o about.js xhr.js wplink.js
%pyt% tools/clearBlankLines.js
%pyt% -t tools/md_to_html.js
copy /Y node_modules\clipboard\dist\clipboard.min.js js\
COPY /Y js(origin)\*.wasm js\
ENDLOCAL
