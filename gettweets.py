# Gets some tweets with the given hashtag

# 1. We are going to collect tweets with special hashtags for building a good enough data set for a linguistics project.
# 2. We use the data set for machine learning mechanism, both with supervised and unsupervised methods.
# 3. Conceptual metaphor analyses may use the results of our project to come up with how people understand and talk about different things.
# App use description: We will search tweets with special hashtags to create data sets that will be used for machine learning in the field of cognitive linguistics.

import sys
import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
from gettweets_secret_keys import *

try:
    cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    else:
        print(err)
    sys.exit()
except:
    print("An error happend connecting to DB.")
    sys.exit()

cur = cnx.cursor()

# IF THERE IS NO DATABASE BEFORE
query = ("create database if not exists tweets "
         "character set utf8 collate utf8_general_ci")
cur.execute(query)
cur.execute('use tweets')
query = """\
create table if not exists tweets (
    id int unsigned auto_increment primary key,
    user varchar(255),
    tweet varchar(280),
    hashtag varchar(255),
    time datetime,
    likes int,
    retweets int,
    replys int
) character set utf8 collate utf8_general_ci
"""
cur.execute(query)
# end of creating DB and table

if len(sys.argv) > 1:
    hashtag = sys.argv[1]
else:
    hashtag = input('What\'s the hashtag you looking for? ')
url = 'https://twitter.com/hashtag/%s?lang=fa' % hashtag
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    'Accept-Encoding':'utf-8'
}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')
tweets = soup.find_all('div', {'class': 'tweet'})
f = open('t.htm', 'w', encoding='utf-8')
f.write(str(soup.contents))
f.close()
print(len(tweets))
i = 0
for tweet in tweets:
    tweet_content = tweet.findChildren('div',{'class':'js-tweet-text-container'})
    i += 1
    print(i)
    print(u"%s" % tweet_content[0].text)
