pyt="python3 compile.py"
res=0
$pyt captcha2.js xhr.js i18n.js sendMsgToMe.js
res=$(($res|$?))
$pyt -t salt.js element.js xhr.js wplink.js
res=$(($res|$?))
$pyt xhr.js instaVerify.js
res=$(($res|$?))
$pyt -o about.js xhr.js wplink.js
res=$(($res|$?))
cp -v node_modules/clipboard/dist/clipboard.min.js js/
res=$(($res|$?))
cp -v node_modules/js-sha512/build/sha512.min.js js/
res=$(($res|$?))
exit $res
