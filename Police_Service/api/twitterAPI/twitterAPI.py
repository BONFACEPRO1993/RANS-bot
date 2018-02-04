from tweepy import OAuthHandler, API, Stream, TweepError

from Police_Service.methods import json
from Police_Service.api.twitterAPI import twitterStream

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

def twitter_stream(twitter_file):

    # Get authentication
    auth_api = twitter_oauth(twitter_file)

    try:
        stream = Stream(auth_api, twitterStream.customStreamListener())

        stream.userstream()

    except BaseException as e:
        print("Error in streaming: ", str(e))
        time.sleep(5)


def auto_reply(twitter_file, send_to, tweet):
    # Get authentication
    auth_api = twitter_oauth(twitter_file)

    api = API(auth_api, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Send confirmation text to informant
    api.send_direct_message(user=send_to, text=tweet)
    print("Confirmation sent to RANS. ( " + send_to + ")")