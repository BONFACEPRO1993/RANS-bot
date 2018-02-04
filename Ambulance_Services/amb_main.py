from Ambulance_Services.api.twitterAPI import twitterAPI


# JSON files
twitter1 = "credentials/twitter_credentials.json"


# twitterAPI.twitter_oauth(twitter1)
twitterAPI.twitter_stream(twitter1)