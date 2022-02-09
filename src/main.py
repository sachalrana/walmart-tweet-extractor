import os
import tweepy
import json
import pandas as pd
import sqlite3
import logging
import credentials

logger = logging.getLogger(__name__)  
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('logs/tweet_processing.log')
formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def save_tweets(tweet_list, db_conn, tbl):

    sql_insert = '''INSERT INTO {table_name} (tweet_id,tweet_text,tweet_createdat,tweet_userid) 
                    VALUES (?,?,?,?)'''.format(table_name=tbl)
    
    try:
        print(len(tweet_list))
        db_conn.executemany(sql_insert,tweet_list)
        db_conn.commit()

    except sqlite3.Error as err:
        logger.error(err)

def create_sql_conn():
    conn = None
    try:
        db_file_path = os.path.join(os.getcwd(),'data',credentials.DB_FILE)
        conn = sqlite3.connect(db_file_path)
    except sqlite3.Error as e:
        logger.error(e)
    finally:
        if conn:
            return conn

def create_tbl(tbl,db_conn):

    cur = db_conn.cursor()
    sql_createtbl = '''DROP TABLE IF EXISTS {table_name}; 
                        CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    tweet_id TEXT NOT NULL, tweet_userid TEXT, 
                                    tweet_createdat TEXT, tweet_text TEXT)'''.format(table_name = tbl)
    
    cur.executescript(sql_createtbl)
    return



if __name__ == '__main__':

    auth = tweepy.OAuthHandler(credentials.TWITTER_API_KEY, credentials.TWITTER_API_KEY_SECRET)
    auth.set_access_token(credentials.TWITTER_ACCESS_TOKEN, credentials.TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth,wait_on_rate_limit=True)

    try:
        tweets = tweepy.Cursor(api.search_tweets,q="justin beiber",lang="en").items(credentials.MAX_RESULTS)
    except tweepy.TweepyException as te:
        logger.error(te)
    
    lst_tweets = []
    for tweet in tweets:
        obj_tweet = tweet._json
        tuple_tweet = (obj_tweet['id_str'],obj_tweet['text'],obj_tweet['created_at'],json.dumps((obj_tweet['user']['id'])))
        lst_tweets.append(tuple_tweet)
    
    conn = create_sql_conn()
    create_tbl('tbl_tweets',conn)
    
    df = pd.DataFrame(lst_tweets,columns=['id','text','created_at','user_id'])
    
    count_rows_initial = df.shape[0]
    print("Tweets consumed: " ,count_rows_initial)
    logger.info("Tweets consumed: " + str(count_rows_initial))

    #filter out tweets about music (not an exhaustive list, based on some preliminary analysis)
    drop_words = ['music', 'album', 'songs', 'song', 'tour', 'concert', 
                    'justinbieberlive','justintour','#JusticeWorldTour','Justice World Tour']
    
    df = df[~df['text'].isin(drop_words)]

    print("Tweets Remaining: ", df.shape[0])
    logger.info("Tweets consumed: " + str(count_rows_initial))

    df = df.drop_duplicates(subset=['text'])
    count_rows_after = df.shape[0]
    
    print("Duplicates removed: ", count_rows_initial - count_rows_after)
    logger.info("Duplicates removed: " + str(count_rows_initial - count_rows_after))
    
    print("Unique Tweets: ",count_rows_after)
    logger.info("Tweets consumed: " + str(count_rows_after))
    
    all_tweets = df.to_records(index=False)
    filtered_tweets = list(all_tweets)
    save_tweets(filtered_tweets,conn,'tbl_tweets')

    conn.close()

