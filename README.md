# fetch_tweets
A simple python code for fetching tweets from twitter.com  
  
Using example:  

```bash
python gettweets_api.py -hg hashtag_to_search -c number_of_tweets -l language  
python gettweets_api.py -x filename.csv -xc int_of_how_many_tweets_to_export | last
```

Using `last` for `-xc` means the tweets from last export. If there was not any export before,
or the `last_tweet_id` file wasn't there, or the content of it was unreadable, it'll return all tweets.
  
  
<sub><sup>(We use MySQL for saving tweets.)</sup></sub>
