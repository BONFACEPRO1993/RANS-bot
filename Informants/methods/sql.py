# INTERNAL LIBRARIES
from Informants.api import twitterAPI
from Informants.methods import json, time_conversion, text_processing


# EXTERNAL LIBRARIES
import pymysql

# Database Connection
def db_connect(filename):
    # Call json
    db_credentials = json.load_from_file(filename)

    # Extract info to access MySQL database
    db_host = db_credentials['host']
    db_user = db_credentials['user']
    db_password = db_credentials['password']
    db_database = db_credentials['database']
    db_charset = db_credentials['charset']

    # Create connection
    connection = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_database, charset=db_charset)

    return connection;

# Breakdown twitter data
def tokenize(search_word, json_file_cred):

    result = twitterAPI.twitter_search(search_word, json_file_cred)

    # Empty List
    data_list = []

    for tweet_data in result:

        # Tweet info
        created_at = tweet_data['created_at']
        tweet_id = tweet_data['id']
        raw_tweet = tweet_data['text']
        raw_url = tweet_data['entities']['urls']

        # Twitter user details
        userHandle = tweet_data['user']['screen_name']
        userName = tweet_data['user']['name']
        userID = tweet_data['user']['id']


        # Convert created_at variable to unix timestamp and local time
        created_time = time_conversion.local_time_conversion(created_at)    #Returns a tuple

        created_at_time = created_time[1]
        created_at_ts = created_time[0]

        # Remove twitter handles and time from text
        tweet = text_processing.handle_remover(raw_tweet)
        tweet = text_processing.time_remover(tweet)
        tweet = text_processing.text_remover(tweet)

        print(tweet)

        # Extract url
        if raw_url:
            url = raw_url[0]['expanded_url']

        else:
            url = "no url"

        # Create list containing twitter data extracted
        data = [tweet_id, tweet, url, created_at_time, userHandle,userName, userID]

        # Append to a common list
        data_list.append(data)

    return data_list

def insert_db(mySQL_file, search_term, twitter_file):
    # Extract data from tokenize method
    raw_data = tokenize(search_term,twitter_file)

    # Create database connection
    conn = db_connect(mySQL_file)

    # Create cursor
    cur = conn.cursor()


    for data in raw_data:
        try:
            cur.execute("INSERT INTO captured_tweets1 (tweet_id, tweet, associated_url, created_time, user_handle, user_name, user_id) "
                "VALUES (%s, %s, %s, %s, %s, %s,%s) ", (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))

            conn.commit()

            print("Record Saved!!")

        except pymysql.err.IntegrityError as e:
            print("MySQL Error: " + str(e))
            continue

    cur.close()
    conn.close()

# Extract data from database
def extract_from_db(mySQL_file, mySQL_query):
    # Create database connection
    conn = db_connect(mySQL_file)

    # Create cursor
    cur = conn.cursor()

    # MySQL query
    query = mySQL_query

    cur.execute(query)

    results = cur.fetchmany(10)

    cur.close()
    conn.close()

    return results

# Update tweet text after removing unwanted text
def update_db(mySQL_file, mySQL_query):
    # Create database connection
    conn = db_connect(mySQL_file)

    # Create cursor
    cur = conn.cursor()

    # MySQL query
    query = mySQL_query

    cur.execute(query)

    results = cur.fetchall()

    for result in results:
        text = text_processing.time_remover(result[1])
        final_text = text_processing.text_remover(text)

        update_query = """UPDATE captured_tweets2
                          SET `tweet` = %s
                          WHERE `id` = %s """

        data = (final_text, result[0])

        cur.execute(update_query, data)
        conn.commit()

        print("Record Updated")




    cur.close()
    conn.close()

    # return results
