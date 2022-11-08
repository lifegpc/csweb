@echo off
SETLOCAL
set py=python
set pyt=%py% compile.py -W *
%pyt% -t sendMsgToMe.js captcha2.js
%pyt% -t wplink.js -t salt.js
%pyt% -t instaVerify.js
%pyt% -o about.js -t wplink.js
%pyt% -t tools/clearBlankLines.js
%pyt% -t tools/md_to_html.js
%pyt% -t proxy/manage.js
%pyt% -t pixiv/pixivgen.js
%pyt% -t genshinExportWishUrl.js
COPY /Y js(origin)\*.wasm js\
ENDLOCAL
