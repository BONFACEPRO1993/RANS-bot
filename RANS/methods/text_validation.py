from RANS.methods import sql, text_processing, time_conversion
from fuzzywuzzy import fuzz
from textblob import TextBlob


# Validation Checker for tweets within 15 minutes window
def informant_validation(reference):

    # Select tweet of a certain message_id
    query = "SELECT message, created_time from rans_informant_rec WHERE message_id= '" + str(reference) + "'"

    query_results = sql.extract_from_db(query)

    start_time = time_conversion.time_limit(query_results[1])
    current_tweet = query_results[0]

    # Select saved tweets within 15 minute window
    query2 = "SELECT message_id, message,created_time FROM rans_informant_rec WHERE created_time >= '" + str(start_time) +\
             " 'AND created_time < ' " + str(query_results[1]) + "'"

    query2_results = sql.extract_from_dbs(query2)

    if(len(query2_results) != 0):
        for result in query2_results:
            # Check similarity in tweets
            string_match = tweet_validation(result[1], current_tweet)


            # Exists substantial similarity
            if string_match >= 60:
                print("Match Found!! Tweet validated")

                # Update valid status in DB
                status_result = sql.updateVALID_rec_messages(result[0], reference)

                validated_data = (result[0], reference)

                return validated_data

                break

            else:
                continue

    else:
        print("No match was found!! Cannot validate tweet.")
        validated_data = ()
        return validated_data





# String matching module
def tweet_validation(string1, string2):

    text1 = text_processing.common_text_remover(string1)
    text2 = text_processing.common_text_remover(string2)

    score = fuzz.partial_ratio(text1, text2)
    return score

# compares two tweets to determine most suitable
def tweet_comparison(references):

    # Extract messages from DB
    query = "SELECT message FROM rans_informant_rec WHERE message_id = '" + str(references[0]) +\
             " 'OR message_id = ' " + str(references[1]) + "'"

    query_results = sql.extract_from_dbs(query)

    text1 = query_results[0][0]     #Previous message
    text2 = query_results[1][0]     #Current message

    text1_lower = text1.lower()
    text2_lower = text2.lower()

    if (text1_lower.find('bad') >= 0 or text1_lower.find('tragic') >= 0 or text1_lower.find('major') >= 0 or text1_lower.find('nasty') >= 0
        or text1_lower.find('fatal') >= 0 or text1_lower.find('horrific') >= 0):
        message = "Ref ["+ str(references[0]) + "] - " +text1 + "\nStatus: Critical"
        status = 2
        result = (references[0],message, status)

    elif (text2_lower.find('bad') >= 0 or text2_lower.find('tragic') >= 0 or text2_lower.find('major') >= 0 or text2_lower.find('nasty') >= 0
        or text2_lower.find('fatal') >= 0 or text2_lower.find('horrific') >= 0):
        message = "Ref [" + str(references[1]) + "] - " + text1 + "\nStatus: Critical"
        status = 2
        result = (references[1], message, status)

    elif (text1_lower.find('minor') >= 0 or text1_lower.find('small') >= 0):
        message = "Ref [" + str(references[0]) + "] - " + text1 + "\nStatus: Less Critical"
        status = 0
        result = (references[0], message, status)

    elif (text2_lower.find('minor') >= 0 or text2_lower.find('small') >= 0):
        message = "Ref [" + str(references[1]) + "] - " + text1 + "\nStatus: Critical"
        status = 0
        result = (references[1], message, status)

    else:
        message = "Ref [" + str(references[0]) + "] - " + text1 + "\nStatus: Emergency"
        status = 1
        result = (references[0], message, status)

    print(message)
    return result

# Checks if same user has tweeted on the same tweet
def user_tweet_validation(message, message_time, informant):

    modified_time = time_conversion.local_time_conversion(message_time)

    # Determine lower_bound time limit
    start_time = time_conversion.time_limit(modified_time)

    # Select saved tweets within 15 minute window
    query2 = "SELECT  message, source_handle FROM rans_informant_rec WHERE created_time >= '" + str(start_time) + \
             " 'AND created_time < ' " + str(modified_time) + "'"

    query2_results = sql.extract_from_dbs(query2)

    status = 0

    if (len(query2_results) != 0):
        for result in query2_results:
             # Check similarity in tweets
            string_match = tweet_validation(result[0], message)

            # Exists substantial similarity
            if informant == result[1] and string_match >= 60:
                status = 1
                print(result)
                break

            else:
                continue

    return status