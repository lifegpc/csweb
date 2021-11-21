pyt="python3 compile.py -W *"
res=0
$pyt captcha2.js xhr.js i18n.js sendMsgToMe.js
res=$(($res|$?))
$pyt -t salt.js xhr.js wplink.js i18n.js
res=$(($res|$?))
$pyt xhr.js instaVerify.js
res=$(($res|$?))
$pyt -o about.js xhr.js wplink.js
res=$(($res|$?))
$pyt tools/clearBlankLines.js
res=$(($res|$?))
$pyt -t tools/md_to_html.js
res=$(($res|$?))
cp -v node_modules/clipboard/dist/clipboard.min.js js/
res=$(($res|$?))
cp -v js\(origin\)/*.wasm js/
res=$(($res|$?))
exit $res
