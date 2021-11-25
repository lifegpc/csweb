pyt="python3 compile.py -W '*'"
res=0
$pyt -t sendMsgToMe.js captcha2.js
res=$(($res|$?))
$pyt -t wplink.js -t salt.js
res=$(($res|$?))
$pyt -t instaVerify.js
res=$(($res|$?))
$pyt -o about.js -t wplink.js
res=$(($res|$?))
$pyt -t tools/clearBlankLines.js
res=$(($res|$?))
$pyt -t tools/md_to_html.js
res=$(($res|$?))
cp -v js\(origin\)/*.wasm js/
res=$(($res|$?))
exit $res
