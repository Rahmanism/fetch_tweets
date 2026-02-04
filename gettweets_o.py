# Gets some tweets with the given hashtag (crawling method!)

import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import gettweets_help
# from db import DB

if '-h' in sys.argv or '--help' in sys.argv:
    gettweets_help.show_help()
    sys.exit(0)

if len(sys.argv) > 1:
    hashtag = sys.argv[1]
else:
    hashtag = input('What\'s the hashtag you looking for? ')

if '-top' in sys.argv:
    url = f'https://x.com/hashtag/{hashtag}?lang=fa&src=hashtag_click'
else:
    url = f'https://x.com/hashtag/{hashtag}?lang=fa&src=hashtag_click&f=live'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        #            'AppleWebKit/537.36 (KHTML, like Gecko) '
        #            'Chrome/72.0.3626.119 Safari/537.36'),
    'Accept-Encoding': 'utf-8'
}

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def load_cookies(driver, cookies_file):
    driver.get(url)  # Navigate to the domain of the cookies
    with open(cookies_file, "r") as file:
        for line in file:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.strip().split("\t")
            cookie = {
                "domain": parts[0],
                "name": parts[5],
                "value": parts[6],
                "path": parts[2],
                "secure": parts[3] == "TRUE",
                "expiry": int(parts[4]) if parts[4] != "0" else None,
            }
            driver.add_cookie(cookie)
    driver.refresh()  # Refresh to apply cookies

def crawl_hashtag(url, timeout=10):
    opts = Options()
    opts.headless = True
    service = Service(executable_path='/Users/mostafa/bin/chromedriver-mac-arm64/chromedriver')
    # maybe set user-agent, disable images, etc., for speed
    driver = webdriver.Chrome(service=service, options=opts)
    load_cookies(driver, '/Users/mostafa/Documents/xcookies.txt')
    try:
        driver.get(url)
        time.sleep(5)
        # wait for tweets/posts to load; adjust CSS/XPath to select one post
        wait = WebDriverWait(driver, timeout)
        # Example: wait until at least one tweet is present
        wait.until(EC.presence_of_element_located((By.XPATH, "//article"))) 
        # get page source
        html = driver.page_source
        # you can parse html with BeautifulSoup or use driver.find_elements(...) to extract structured data
        return html
    finally:
        driver.quit()



print(url)
page = crawl_hashtag(url)
# do something with page, e.g. BeautifulSoup(page)
print(page[:1000])  # just preview
sys.exit()

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')
# print(soup)
tweets = soup.find_all('div', {'class': 'tweet'})

print(f"Number of tweets fetched: {len(tweets)}.")

# saving the html of tweets in a temp file!
f = open('t.htm', 'w', encoding='utf-8')
f.write(str(tweets))
f.close()

inserted_tweets_count = 0
for tweet in tweets:
    tweet_timestamp_tag = tweet.find('a', {'class': 'tweet-timestamp'})
    tweet_id = tweet_timestamp_tag.get('data-conversation-id')
    if tdb.check_if_exists(tweet_id):
        continue
    tweet_timestamp = int(tweet_timestamp_tag.find(
        'span', {'class': '_timestamp'}).get('data-time'))
    tweet_time = datetime.fromtimestamp(tweet_timestamp)
    user = tweet.find('span', {'class': 'username'}).find('b').text
    tweet_content = tweet.find(
        'div', {'class': 'js-tweet-text-container'}).text
    reply = tweet.find('div', {'class': 'ReplyingToContextBelowAuthor'})
    tweet_type = 0 if reply == None else 1
    tweet_profile = tweet.find(
        'div', {'class': 'ProfileTweet-actionCountList'})
    replys = (tweet_profile.find(
        'span', {'class': 'ProfileTweet-action--reply'})
        .find('span', {'class': 'ProfileTweet-actionCount'})
        .get("data-tweet-stat-count"))
    retweets = (tweet_profile.find(
        'span', {'class': 'ProfileTweet-action--retweet'})
        .find('span', {'class': 'ProfileTweet-actionCount'})
        .get("data-tweet-stat-count"))
    likes = (tweet_profile.find(
        'span', {'class': 'ProfileTweet-action--favorite'})
        .find('span', {'class': 'ProfileTweet-actionCount'})
        .get("data-tweet-stat-count"))

    tweet_data = {
        'tweet_id': tweet_id,
        'user': user,
        'tweet': tweet_content,
        'tweet_type': tweet_type,
        'hashtag': hashtag,
        'timestamp_seconds': tweet_timestamp,
        'tweet_time': tweet_time,
        'likes': likes,
        'retweets': retweets,
        'replys': replys
    }
    print(tweet_data)
    inserted_tweets_count += 1

print(f"Number of tweets inserted in DB: {inserted_tweets_count}.")
