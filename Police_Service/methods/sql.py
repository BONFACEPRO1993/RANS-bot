# INTERNAL LIBRARIES
from Police_Service.api.twitterAPI import twitterAPI
from Police_Service.methods import json, time_conversion, text_processing

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
def tokenize(tweet_data):

    result = tweet_data

    # Convert created_at variable to unix timestamp and local time
    created_time = time_conversion.local_time_conversion(result[2])    #Returns a datetime variable

    # Remove twitter handles and time from text
    tweet = text_processing.handle_remover(result[1])
    tweet = text_processing.time_remover(tweet)
    tweet = text_processing.text_remover(tweet)

    # Save as a tuple
    refined_data = (result[0], tweet, created_time, result[3], result[4], result[5], result[6])

    insert_db_messages(refined_data)

    return tweet


def insert_db_messages(twitter_data):
    # Variables
    data = twitter_data     #Result from tokenize method (tuple)
    mysql_cred = "credentials/mysql.json"

    # Create database connection
    conn = db_connect(mysql_cred)

    # Create cursor
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO rans_messages (tw_message_id, tweet, tw_created, tw_sender_name, tw_sender_id, tw_recipient_name, tw_recipient_id) "
               "VALUES (%s, %s, %s, %s, %s, %s,%s) ", (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))

        conn.commit()

        print("Record Saved!!")

    except pymysql.err.IntegrityError as e:
        print("MySQL Error: " + str(e))


    cur.close()
    conn.close()

# # Extract data from database
# def extract_from_db(mySQL_file, mySQL_query):
#     # Create database connection
#     conn = db_connect(mySQL_file)
#
#     # Create cursor
#     cur = conn.cursor()
#
#     # MySQL query
#     query = mySQL_query
#
#     cur.execute(query)
#
#     results = cur.fetchmany(10)
#
#     cur.close()
#     conn.close()
#
#     return results

# Update tweet text after removing unwanted text
# def update_db(mySQL_file, mySQL_query):
#     # Create database connection
#     conn = db_connect(mySQL_file)
#
#     # Create cursor
#     cur = conn.cursor()
#
#     # MySQL query
#     query = mySQL_query
#
#     cur.execute(query)
#
#     results = cur.fetchall()
#
#     for result in results:
#         text = text_processing.time_remover(result[1])
#         final_text = text_processing.text_remover(text)
#
#         update_query = """UPDATE captured_tweets2
#                           SET `tweet` = %s
#                           WHERE `id` = %s """
#
#         data = (final_text, result[0])
#
#         cur.execute(update_query, data)
#         conn.commit()
#
#         print("Record Updated")
#
#
#
#
#     cur.close()
#     conn.close()


