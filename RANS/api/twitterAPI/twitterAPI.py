from tweepy import OAuthHandler, API, Stream, TweepError

from RANS.methods import json, sql, text_validation, time_conversion
from RANS.api.twitterAPI import twitterStream

import time


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

    return auth

# Twitter Streaming module
def twitter_stream(twitter_file):

    # Get authentication
    auth_api = twitter_oauth(twitter_file)

    try:
        stream = Stream(auth_api, twitterStream.customStreamListener())

        stream.userstream()

    except BaseException as e:
        print("Error in streaming: ", str(e))
        time.sleep(5)


# Module that sends message from RANS
def auto_reply(twitter_file, send_to, tweet):
    # Get authentication
    auth_api = twitter_oauth(twitter_file)

    api = API(auth_api, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Send confirmation text to informant
    api.send_direct_message(user=send_to, text=tweet)
    print("Confirmation sent to informant " + send_to)

#   Modules sends message to ERSP.
def send_ERSP(twitter_file, send_inputs):
    # Get authentication
    auth_api = twitter_oauth(twitter_file)

    api = API(auth_api, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Check if previous tweet was replied to
    query = "SELECT replied_status from rans_informant_rec WHERE message_id= '" + str(send_inputs[0]) + "'"

    query_results = sql.extract_from_db(query)

    # If message was not replied, return tuple result
    if(query_results[0] == 0):
        final_result = text_validation.tweet_comparison(send_inputs)

        if final_result[2] == 0:
            send_to = '@ServicesTraffic'
            tweet = final_result[1]

            # Send confirmation text to Police only
            api.send_direct_message(user=send_to, text=tweet)
            print("Accident info sent to Police " + send_to)

        else:
            send_to = '@ServicesTraffic'
            send_to2 = '@accidentambula1'
            tweet = final_result[1]

            # Send confirmation text to Police + Ambulance Services
            api.send_direct_message(user=send_to, text=tweet)
            api.send_direct_message(user=send_to2, text=tweet)
            print("Accident info sent to Police " + send_to + " and Ambulance Services " + send_to2)

    else:
        # Get source handle
        query = "SELECT source_handle from rans_informant_rec WHERE message_id= '" + str(send_inputs[1]) + "'"

        query_results = sql.extract_from_db(query)

        tweet = "This info of ref [" + str(send_inputs[1]) + "] was earlier submitted and relevant ERSP have responded. Thank you."

        api.send_direct_message(user=query_results[0], text=tweet)
        print("Assurance notification sent to informant")


#   Module to send confirmation to informants.
def send_informant_note(twitter_file, ref_no, ersp):
    # Get authentication
    auth_api = twitter_oauth(twitter_file)

    api = API(auth_api, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Get all informants who tweeted about same accident
    informant_details = sql.common_tweets_checker(ref_no)

    for informant in informant_details:
        message = ersp + " has responded your notification of ref [" + str(informant[0]) + "]."
        userhandle = "@" + informant[1]

        # Send message text to informant
        api.send_direct_message(user=userhandle, text=message)
        print("ERSP confirmation sent to informant")










    # # If message was not replied, return tuple result
    # if(query_results[0] == 0):
    #     final_result = text_validation.tweet_comparison(send_inputs)
    #
    #     if final_result[2] == 0:
    #         send_to = '@ServicesTraffic'
    #         tweet = final_result[1]
    #
    #         # Send confirmation text to Police only
    #         api.send_direct_message(user=send_to, text=tweet)
    #         print("Accident info sent to Police " + send_to)
    #
    #     else:
    #         send_to = '@ServicesTraffic'
    #         send_to2 = '@accidentambula1'
    #         tweet = final_result[1]
    #
    #         # Send confirmation text to Police + Ambulance Services
    #         api.send_direct_message(user=send_to, text=tweet)
    #         api.send_direct_message(user=send_to2, text=tweet)
    #         print("Accident info sent to Police " + send_to + " and Ambulance Services " + send_to2)