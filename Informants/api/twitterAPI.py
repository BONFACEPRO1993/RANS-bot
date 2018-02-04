# INTERNAL LIBRARIES
from Informants.methods import json, sql, time_conversion

# DEFAULT LIBRARIES
import sys
import time

# EXTERNAL LIBRARIES
from tweepy import AppAuthHandler, OAuthHandler, API, TweepError

# Twitter App Authentication
def twitter_auth(filename):
    # Call json
    credentials_data = json.load_from_file(filename)

    # Extract info to access twitter app
    cons_key = credentials_data['consumer_key']
    cons_secret = credentials_data['consumer_secret']


    auth = AppAuthHandler(consumer_key=cons_key, consumer_secret=cons_secret)


    api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


    if (not api):
        print("Can't Authenticate!!")
        sys.exit(-1)

    return api

# Twitter App Authentication
def twitter_oauth(filename):
    # Call json
    credentials_data = json.load_from_file(filename)

    # Extract info to access twitter app
    cons_key = credentials_data['consumer_key']
    cons_secret = credentials_data['consumer_secret']
    acc_token = credentials_data['access_token']
    acc_token_secret = credentials_data['access_token_secret']


    auth = OAuthHandler(cons_key, cons_secret)
    auth.set_access_token(acc_token, acc_token_secret)

    api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


    if (not api):
        print("Can't Authenticate!!")
        sys.exit(-1)

    return api

# Search historic tweets
def twitter_search(search_term, json_file):
    auth_api = twitter_auth(json_file)

    # Variables
    query = search_term
    maxTweets = 100000      #Abitrary figure
    tweetsPerQuery = 100    #Max tweets that can be searched at a time
    sinceId = None
    max_id = -1
    tweetCount = 0
    tweet_list = []

    print("Downloading max {0} tweets".format(maxTweets))

    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = auth_api.search(q=query, count=tweetsPerQuery, )

                else:
                    new_tweets = auth_api.search(q=query, count=tweetsPerQuery, since_id=sinceId)

            else:
                if (not sinceId):
                    new_tweets = auth_api.search(q=query, count=tweetsPerQuery,
                                            max_id=str(max_id - 1))

                else:
                    new_tweets = auth_api.search(q=query, count=tweetsPerQuery,
                                            max_id=str(max_id - 1), since_id=sinceId)

            if not new_tweets:
                print("No more tweets found")
                break

            for tweet in new_tweets:
                tweet = json.load_from_variable2(tweet)
                tweet_list.append(tweet)


            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id

        except TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

    print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, "database"))
    return tweet_list

# Posts tweet to a particular handle
def post_dm(twitter_file, sql_file, sql_query):
    # Variables
    send_to = "@BonbonTest"

    # Get authentication
    auth_api = twitter_oauth(twitter_file)

    # Obtain data from database
    db_data = sql.extract_from_db(sql_file, sql_query)


    for data in db_data:
        try:
            # Get current time
            posted_time = str(time_conversion.get_current_time())

            # Draft tweet
            tweet = data[1] + " " + posted_time

            if len(tweet) <= 140 and data[1] != "No text captured!!":
                # Post tweet after 10 sec
                auth_api.send_direct_message(user=send_to, text=tweet)
                print("DM sent to RANS")
                time.sleep(40)


        except TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            pass