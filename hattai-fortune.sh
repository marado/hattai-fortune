rm -f publicoRSS && wget http://feeds.feedburner.com/publicoRSS -o /dev/null

# if wget isn't successful, we're fsck'd up, better quit!
RETVAL=$?
[ $RETVAL -ne 0 ] && exit $RETVAL

# if title is empty or does not exist, initialize it
if [[ -s title ]] ; then
echo -n "";
else
echo "Público" > title
fi;

cat publicoRSS|grep title|sed 's/\ *<title>//g'|sed 's/<\/title>//g'|grep -v -i blico|grep -v "$(cat title)"|grep -v -i psilon|grep -v -i benfic|grep -v -i assinant|grep -v -i sporting|grep -v -i Chelsea|grep -v -i arsenal|grep -v derby|grep -v -i golo|grep -v -i sporting|grep -v Djokovic|grep -v -i jogo|grep -v ^$|grep -v "lt;"|grep -v \"|grep -v -i ronaldo|head -1 > title
grep "$(cat title|sed 's/\r//g')" publicoRSS -A2|grep link|sed 's/\ *<link>//g'|sed 's/<\/link>//g' > link
cat title
