pyt="python3 compile.py"
res=0
$pyt captcha2.js xhr.js i18n.js sendMsgToMe.js
res=$(($res|$?))
$pyt -t salt.js element.js xhr.js wplink.js
res=$(($res|$?))
$pyt xhr.js instaVerify.js
res=$(($res|$?))
exit $res
