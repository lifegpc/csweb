@echo off
SETLOCAL
set py=python
set pyt=%py% compile.py
%pyt% captcha2.js xhr.js i18n.js sendMsgToMe.js
%pyt% -W undefinedVars -t salt.js xhr.js wplink.js
ENDLOCAL
