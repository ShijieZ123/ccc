from http.client import IncompleteRead

import tweepy
import couchdb
import time
import json
import logging
import datetime as DT
import tw_cdb_credentials
import sys

#twitter auth
consumer_key = tw_cdb_credentials.consumer_key
consumer_secret = tw_cdb_credentials.consumer_secret
access_token = tw_cdb_credentials.access_token
access_token_secret = tw_cdb_credentials.access_token_secret




# == couchdb ==
couch = couchdb.Server(tw_cdb_credentials.url)
try:
    couch.create('twitter_adelaide')
    db = couch['twitter_adelaide']
except:
    db = couch['twitter_adelaide']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)
#1:adelaide, 2:sydney, 3:melbourne, 4:perth, 5:brisbane
citycode = 1
city_id = {
    "adelaide": "01e8a1a140ccdc5c",
    "sydney":"0073b76548e5984f",
    "brisbane": "004ec16c62325149",
    "melbourne":"01864a8a64df9dc4",
    "perth": "0118c71c0ed41109",
    "canberra": "01e4b0c84959d430"
}

todaytweets = api.search_tweets(q="place:%s" % city_id['adelaide'], count=100,until=DT.date.today().strftime("%Y-%m-%d"))
current_tweet_id = ""
begin_tweet_id = ""

for todaytweet in todaytweets:
    tweetstr = json.dumps(todaytweet._json)
    json_load = json.loads(tweetstr)
    current_tweet_id = json_load['id_str']
    begin_tweet_id = json_load['id_str']

logfile = DT.datetime.today().strftime("%d-%b-%Y(%H-%M-%S.%f)") + ".log"

logging.basicConfig(filename=logfile, level=logging.INFO)


def create_db(db_name):
    try:
        couch.create(db_name)
    except:
        logging.warning("db exist")

def get_tweets_query(city,page,datetweet, current_id):
          
    # Authorization to consumer key and consumer secret
    # Calling api
    api = tweepy.API(auth)
    last_tweet_id = current_id
    search_tweets_inserted = 0
    timeline_tweets_inserted = 0
  
    try:
        pages = tweepy.Cursor(api.search_tweets, q="place:%s" % city_id[city], count=100, max_id=current_id, until=datetweet).pages(page)

    except IncompleteRead:
        logging.warning("Incomplete Read")

    for tweets in pages:
        for tweet in tweets:
            tweetstr = json.dumps(tweet._json)
            json_load = json.loads(tweetstr)
            user = {'id_str': json_load['user']['id_str'],
                    'screen_name': json_load['user']['screen_name'],
                    'location': json_load['user']['location'],
                    'verified': json_load['user']['verified'],
                    'followers_count': json_load['user']['followers_count'],
                    'friends_count': json_load['user']['friends_count'],}
            text = {'_id': json_load['id_str'],
                    'created_at': json_load['created_at'],
                    'text': json_load['text'],
                    'source': json_load['source'],
                    'user': user,
                    'geo': json_load['geo'],
                    'coordinates': json_load['coordinates'],
                    'place': json_load['place'],
                    #'quote_count': json_load['quote_count'],
                    #'reply_count': json_load['reply_count'],
                    'retweet_count': json_load['retweet_count'],
                    'favorite_count': json_load['favorite_count'],
                    'entities': json_load['entities'],
                    'lang': json_load['lang'],
                    }
            last_tweet_id = tweet.id_str
            try:
                db.save(json.loads(json.dumps(text)))
                search_tweets_inserted = search_tweets_inserted + 1
                logging.info("save search tweet successful " + last_tweet_id)
                #go through user timeline of the tweet from search query result
                tweets_user = api.user_timeline(id=json_load['user']['id_str'],count=15,max_id=json_load['id_str'])
                for tweet_user in tweets_user:
                    tweetstr = json.dumps(tweet_user._json)
                    json_load = json.loads(tweetstr)
                    user = {'id_str': json_load['user']['id_str'],
                            'screen_name': json_load['user']['screen_name'],
                            'location': json_load['user']['location'],
                            'verified': json_load['user']['verified'],
                            'followers_count': json_load['user']['followers_count'],
                            'friends_count': json_load['user']['friends_count'],}
                    text = {'_id': json_load['id_str'],
                            'created_at': json_load['created_at'],
                            'text': json_load['text'],
                            'source': json_load['source'],
                            'user': user,
                            'geo': json_load['geo'],
                            'coordinates': json_load['coordinates'],
                            'place': json_load['place'],
                            'retweet_count': json_load['retweet_count'],
                            'favorite_count': json_load['favorite_count'],
                            'entities': json_load['entities'],
                            'lang': json_load['lang'],
                            }
                    try:
                        db.save(json.loads(json.dumps(text)))
                        logging.info("save user timeline tweet")
                        timeline_tweets_inserted = timeline_tweets_inserted + 1
                    except couchdb.http.ResourceConflict:
                        logging.info("duplicate user timeline tweet")

            except couchdb.http.ResourceConflict:
                logging.info("duplicate search tweet")
                logging.info(last_tweet_id)
                #sys.exit(1)
            #current_tweet_id = tweet.id_str
        logging.info('searching paused')
        logging.info("Search tweets:" + str(search_tweets_inserted) + " timeline tweets:" + str(timeline_tweets_inserted))
    return (last_tweet_id,search_tweets_inserted)

if __name__ == "__main__":

    for city in ['twitter_adelaide', 'twitter_sydney', 'twitter_melbourne', 'twitter_perth', 'twitter_brisbane']:
        create_db(city)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #Adelaide
    city = "adelaide"
    logging.info("ADELAIDE")
    page = 100 # maximum pages we can get within 15min
    datetweet = (DT.date.today() - DT.timedelta(days=7)).strftime("%Y-%m-%d")
    timer = 900
    
    # run for 999 times just in case you forgot to close it
    for i in range(0, 999):
        timer = 900
        
        logging.info('time to abstract from ' + datetweet + '. With tweets earlier than: ' + current_tweet_id)
        result = get_tweets_query(city,page,datetweet, current_tweet_id)
        current_tweet_id = result[0]
        logging.info(current_tweet_id)

        if(result[1]==0):
            citycode = citycode + 1
            if(citycode == 2):
                db = couch['twitter_sydney']
                city = "sydney"
                current_tweet_id = begin_tweet_id
                logging.info("SYDNEY")
            elif(citycode == 3):
                db = couch['twitter_melbourne']
                city = "melbourne"
                current_tweet_id = begin_tweet_id
                logging.info("MELBOURNE")
            elif(citycode == 4):
                db = couch['twitter_perth']
                city = "perth"
                current_tweet_id = begin_tweet_id
                logging.info("PERTH")
            elif(citycode == 5):
                db = couch['twitter_brisbane']
                city = "brisbane"
                current_tweet_id = begin_tweet_id
                logging.info("BRISBANE")
            else:
                sys.exit()

        # make call after 15min
        while timer >= 0:
            time.sleep(1)
            timer -= 1
    logging.info('searching finished')
