from tweepy.streaming import StreamListener
from Police_Service.methods import json, text_processing
from Police_Service.api.twitterAPI import twitterAPI


class customStreamListener(StreamListener):

    def __init__(self):
        self.tweetCount = 0

    def on_connect(self):
        print("Connection established!!")

    def on_disconnect(self, notice):
        print("Connection lost!! : ", notice)

    def on_data(self, status):
        try:
            # Convert to JSON dictionary
            raw_data = json.load_from_variable(status)

            # Twitter Credentials variable
            twitter = "credentials/twitter_credentials.json"

            if(raw_data["direct_message"]):
                # Message Info
                message_id = raw_data["direct_message"]["id"]
                text = raw_data["direct_message"]["text"]

                # Message metadata
                created_at = raw_data["direct_message"]["created_at"]
                sender_id = raw_data["direct_message"]["sender_id"]
                sender_name = raw_data["direct_message"]["sender_screen_name"]
                receiver_id = raw_data["direct_message"]["recipient_id"]
                receiver_name = raw_data["direct_message"]["recipient_screen_name"]

                data_list = (message_id, text, created_at, sender_name, sender_id, receiver_name, receiver_id)

                text_lower = text.lower()

                # Check if message is from RANS
                if (sender_id == 902212028026294272 and text_lower.find('accident')>= 0):
                    sender_handle = "@" + sender_name

                    # Extract reference no from tweet
                    ref_num = text_processing.ref_no_extractor(text)

                    # Create reply to RANS based on reference number provided
                    tweet = "Ref [" + str(ref_num) + "]. Message received and we will dispatch our team shortly. @" + receiver_name

                    # Send to RANS
                    twitterAPI.auto_reply(twitter, sender_handle, tweet)



        except BaseException as e:
            print("Failed on data", str(e))

        return True

    def on_error( self, status ):
        print(status)