
# Tweet Extractor
***Task for Walmart DE Application***
***by Sachal Abbas***

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
- `tweet_text`: Text of the tweet
- `tweet_createdat`: Timestamp of when the tweet was published

#### More features:
There were tons of more features available from the Twitter Streaming API such as like count, retweet count, geo location data which can be utilized for deeper analysis 

# 3. Deployment
1. Before we run the program, we need to input the access keys and bearer token that the user has available from Twitter's Dev Account (https://developer.twitter.com/en/portal/dashboard). 
2. Modify the `credentials.py` file available in the `config` folder and modify the appropriate attributes accordingly. For now my credentials are already there (**I know it's bad practice**)
3. Modify the number of tweets that you want to extract from Twitter by updating the `MAX_RESULTS` parameter in the file
4. You can specify the name of the database file by modifying the `DB_FILE` parameter in the file

This Python program can be run from the command line when in the main folder assuming all the necessary libraries have been installed in your python3 environment

    python3 main.py
The appropriate log files will be generated in the `logs` folder

Once the application stops running, we can explore the data by opening the `{db_name}.db` file generated in the data folder using any SQLite3 browser.
The answers to unique counts plus the number of tweets consumed are going to be printed in the log and the terminal window as well where you run the python program.

Recommended Database Browser: (Supports Windows and macOS): https://sqlitebrowser.org/dl/

# 4. Project Structure

```
|   requirements.txt
├── src
│   	├── main.py         <- main app
	├── credentials.py  <- contains credentials + config.
|
├── logs	<- Contains the logs generated.
|
├── data	<- Contains the .db file to explore.
```

# 5. Further Questions

**Q1. What are the risks involved in building such a pipeline?**
 - Personal information of users is also available in each tweet's metadata such as geolocation plus name of the users. We have to maintain data integrity.
 - Data governance is really important. We have to keep in mind data regulations such as GDPR when storing and processing such data. 
 - There would be a lot of profanity that needs to be filtered
 - Make sure that the pipeline is running in a secured manner i.e. proper access controls are implemented in terms of getting access to the data produced

 **Q2. How would you roll out the pipeline going from proof-of-concept to a production-ready solution?**
 - We would first test the pipeline in a dev environment that will be have limited resources. Once the pipeline performs as expected, we will deploy it on a UAT environment which will have resources similar to that of a production level instance. Once all the testing is complete on all phases, we can roll out the pipeline onto the production instance. 
 - We will need to ensure that data is of good quality when the pipeline has been rolled out into a UAT instance.
 - Make sure we have a big enough scope at the proof of concept phase so that we don't run into issues when in Production

**Q3. What would a production-ready solution entail that a POC wouldn't?**
- A production ready solution should be **scalable**.
	- The pipeline should follow the concept of containerization i.e. if there is change in the volume/traffic of tweets, it should be able to easily scale up or down the number of containers. Each container here is used to distribute the load and execute the processes in parallel.
	- There should be a contingency plan in place if one server goes down, then the traffic should automatically switch over to the other server without any latency. For example, in AWS, if the us-east-1 availability zone goes down, traffic should be re-routed to us-west-2.
- A production ready solution should be **portable**.
	- If we are using docker containers, we should be able to run them on any platform; for example Elastic Container Service (ECS), Elastic Kubernetes Service (EKS) etc.  
	- The image that has been created for the pipeline should be able to run on any cloud or on-prem service.
 - A production ready solution should have good **interoperability**
	 - The pipeline should be able to communicate with other services and run on any platform

**Q4. What is the level of effort required to deliver each phase of the solution?**
- *Requirement Gathering*:  LOE is **high** because this involves scoping the project and planning what features are required keeping in mind the end goal of the solution.
- *Software Design and Development*: LOE is **high** because this is the time where the engineers actually design the solution architecture plus write the code. 
- *Testing and Integration*: LOE is **high**. We have to make sure that the solution passes all quality and performance standard in place. 
- *Deployment*: LOE is **medium**. During all the previous phases, we have a good understanding of all the requirements for running the solution and letting the DevOps team know about the requirements for provisioning should be straightforward. 
- *Operationalization And Maintenance*: LOE is **high**. In this phase, the solution is running and now we have to make sure that data integrity is maintained plus the proper data governance controls are in place.  

**Q5. What is your estimated timeline for delivery for a production-ready solution?**

Every organization has its way of deploying a production-ready solution. Most of the time, sprints are done in spans of 2 weeks. Requirement Gathering can take approximately a week and then we can have 2 week sprints; coding, testing, deployment to UAT and Prod + testing. So in total we can assume the solution from start to finish can take anytime between 2-3 sprints (1.5 - 2 months).

# 6. Conclusion
There were various way of interpreting and finalizing a solution for getting tweets regarding a particular topic. Twitter had recently released a v2 of their API with more robust features and endpoints for deeper analysis however it is still in development and hasn't been fully completed.
I had come up with a solution initially utilizing the v2 version of the app which allowed me to remove certain types of tweets from being streamed using rules, however, the API was too slow to stream the tweets which forced me to look into their v1 API which was quite decent as well. 
Moreover, the way the v2 API endpoint for streaming tweets was designed, we could only interrupt the stream with a KeyboardInterrupt which wasn't feasible in our use case where we have to perform certain queries on the resultant dataset hence another reason to look into the v1 version of Twitter's API. 
