cd /d c:\fetch_tweets

python gettweets_api.py -hg زندگی -c 2000
python gettweets_api.py -hg تاریخ -c 2000
python gettweets_api.py -hg فرهنگ -c 2000

rem set /P lastId= < last_tweet_id
del life.csv
python gettweets_api.py -x life.csv -hg زندگی -xc last

rem echo %lastId% > last_tweet_id
del history.csv
python gettweets_api.py -x history.csv -hg تاریخ -xc last

rem echo %lastId% > last_tweet_id
del culture.csv
python gettweets_api.py -x culture.csv -hg فرهنگ -xc last
