from RANS.api.twitterAPI import twitterAPI
from RANS.methods import text_processing


# JSON files
twitter1 = "credentials/twitter_credentials.json"

string = "hello I am a good boy. [22556546789]"


# twitterAPI.twitter_oauth(twitter1)
twitterAPI.twitter_stream(twitter1)

