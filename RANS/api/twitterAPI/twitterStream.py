from tweepy.streaming import StreamListener
from RANS.methods import json, text_validation, sql, text_processing
from RANS.api.twitterAPI import twitterAPI


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

                # Check if message is from police or ambulance services
                if (sender_id == 949722412207263748 or sender_id == 949720415794024449):

                    sender_handle = "@" + sender_name

                    tweet = "Thanks for your response."

                    # Send Reply to ERSP
                    twitterAPI.auto_reply(twitter, sender_handle, tweet)

                    reference = text_processing.ref_no_extractor(text)

                    data = (message_id, text, reference, created_at, sender_name, sender_id)

                    # Save to RECEIVE table for ERSP and update send_status
                    sql.insert_rec_ersp(data)

                    # Send notification reply to informants
                    twitterAPI.send_informant_note(twitter, reference, sender_handle)


                # Check message from informant
                elif(receiver_id == 902212028026294272):

                    if(text.find('accident') >= 0 or text.find('Accident') >= 0):
                        sender_handle = "@" + sender_name

                        # Create reference no and text
                        ref_no = str(message_id)
                        tweet = "Thanks for your info. Your reference number is [" + ref_no + "]. To confirm your info as correct, Please reply by typing 'Yes'"

                        verification_status = text_validation.user_tweet_validation(text, created_at, sender_name)

                        if verification_status == 1:
                            spam_tweet = "You have already submitted. Kindly be patient."
                            twitterAPI.auto_reply(twitter, sender_handle, spam_tweet)

                        else:
                            # Send as confirmation to informant
                            twitterAPI.auto_reply(twitter, sender_handle, tweet)

                            # Save to DB
                            parsed_tweet = sql.tokenize(data_list)
                            sql.insert_rec_messages(parsed_tweet)

                    elif(text.find('yes') >= 0 or text.find('Yes') >= 0):
                        sender_handle = "@" + sender_name

                        # Create reference no and text
                        tweet = "Thanks for confirming your info. We will validate and ultimately send to relevant ERSP."

                        # Send as confirmation to informant
                        twitterAPI.auto_reply(twitter, sender_handle, tweet)

                        # Update confirmation status in DB and return reference_no(message_id)
                        ref_num = sql.updateCONF_rec_messages(sender_id)

                        print(ref_num)

                        # Validate tweet and update validation status
                        validated_result = text_validation.informant_validation(ref_num)

                        if(len(validated_result) != 0):
                            print(validated_result)

                            # Send message to relevant ERSP
                            twitterAPI.send_ERSP(twitter, validated_result)

                        else:
                            print("Message not validated.")


                elif(sender_id == 902212028026294272):
                    # If sent to police and/or ambulance services
                    if(receiver_id == 949722412207263748 or receiver_id == 949720415794024449):

                        ref_no = text_processing.ref_no_extractor(text)

                        data = (message_id, text, ref_no, created_at, receiver_name, receiver_id)

                        # Save to SEND table for ERSP and update send_status
                        sql.insert_send_ersp(data)
                        sql.updateSEND_rec_messages(ref_no)


                    elif(sender_id == 902212028026294272 and text.find('responded') >= 0):

                        ref_no = text_processing.ref_no_extractor(text)

                        data = (message_id, text, ref_no, created_at, receiver_name, receiver_id)

                        # Save to SEND table for informant and update replied_status
                        sql.insert_send_informant(data)
                        sql.updateREPLIED_rec_messages(ref_no)

                        print("Reply delivered to user.")


        except BaseException as e:
            print("Failed on data", str(e))

        return True

    def on_error( self, status ):
        print(status)