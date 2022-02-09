
# Tweet Extractor
***Task for Walmart DE Application***

# 1. Requirements

-   Implement a data pipeline, using your programming language of choice, that outputs a machine-learning ready dataset.
-   Connect to the Twitter streaming API and do a keyword search on Justin Bieber
-   Filter out all tweets having to do with music
-   Store the tweets into a database of your choosing
-   Avoid duplicates
-   Produce a count of all tweets consumed
-   Produce a count of unique tweets

# 2. Data
We utilized the Tweepy library to download **X** number of tweets about **Justin Bieber**

According to the requirements, we only needed to store the bare minimum attributes for now

Features:
- `id`: (primary key, auto increment) - Unique identifier for each record.
- `tweet_id`: Unique identifier from Twitter for each tweet.
- `tweet_userid`: Unique identifier of the User who tweeted
- `tweet_text`: The tweet itself
- `tweet_createdat`: Timestamp of when the tweet was published

#### More features:
There were tons of more features available from the Twitter Streaming API such as like count, retweet count, geo location data which can be utilized for deeper analysis 

# 3. Deployment
1. Before we run the program, we need to input the access keys and bearer token that the user has available from Twitter's Dev Account (https://developer.twitter.com/en/portal/dashboard). 
2. Modify the `credentials.py` file available in the `config` folder and modify the appropriate attributes accordingly.
3. Modify the number of tweets that you want to extract from Twitter by updating the `MAX_RESULTS` parameter in the file
4. You can specify the name of the database file by modifying the `DB_FILE` parameter in the file

This Python program can be run from the command line when in the main folder

    python3 main.py
The appropriate log files will be generated in the `logs` folder

Once the application stops running, we can explore the `.db` file generated in the data folder using any SQLite3 browser
Recommended (Supports Windows and macOS): https://sqlitebrowser.org/dl/

# 4. -  Further Questions

1. What are the risks involved in building such a pipeline?
2. How would you roll out the pipeline going from proof-of-concept to a production-ready solution?
3. What would a production-ready solution entail that a POC wouldn't?
4. What is the level of effort required to deliver each phase of the solution?
5. What is your estimated timeline for delivery for a production-ready solution?

# 5. Project Structure

```
|   requirements.txt
|   setup.py
├── src
│   ├── main.py         <- main app.
	├── credentials.py  <- contains credentials + config.
│
├── logs          		<- Logs folder.
|
├── data                <- DB file.
```
