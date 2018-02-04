# INTERNAL LIBRARIES
from RANS.api.twitterAPI import twitterAPI
from RANS.methods import json, time_conversion, text_processing, text_validation


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

    # Convert created_at variable to datetime variable
    created_time = time_conversion.local_time_conversion(result[2])

    # Remove twitter handles and time from text
    tweet = text_processing.handle_remover(result[1])
    tweet = text_processing.time_remover(tweet)
    tweet = text_processing.text_remover(tweet)

    # Save as a tuple
    refined_data = (result[0], tweet, created_time, result[3], result[4], result[5], result[6])

    return refined_data

# ALL INSERT MODULES
# For received informant notifications
def insert_rec_messages(twitter_data):
    # Variables
    data = twitter_data     #Result from tokenize method (tuple)
    mysql_cred = "credentials/mysql.json"

    # Create database connection
    conn = db_connect(mysql_cred)

    # Create cursor
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO rans_informant_rec (message_id, message, created_time, source_handle, source_id) "
               "VALUES (%s, %s, %s, %s, %s) ", (data[0], data[1], data[2], data[3], data[4]))

        conn.commit()

        print("Record Saved on RECEIVED table for Informants!!")

    except pymysql.err.IntegrityError as e:
        print("MySQL Error: " + str(e))


    cur.close()
    conn.close()

# For notifications to ERSP
def insert_send_ersp(twitter_data):
    # Variables
    data = twitter_data     #Result from tokenize method (tuple)
    mysql_cred = "credentials/mysql.json"

    # Preprocess created_at to datetime type
    created_time = time_conversion.local_time_conversion(data[3])

    # Create database connection
    conn = db_connect(mysql_cred)

    # Create cursor
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO rans_ersp_send (message_id, message, ref_num, created_time, destination_handle, destination_id) "
               "VALUES (%s, %s, %s, %s, %s, %s) ", (data[0], data[1], data[2], created_time, data[4], data[5]))

        conn.commit()

        print("Record Saved on SENT table for ERSP!!")

    except pymysql.err.IntegrityError as e:
        print("MySQL Error: " + str(e))


    cur.close()
    conn.close()

# For notifications from ERSP
def insert_rec_ersp(twitter_data):
    # Variables
    data = twitter_data     #Result from tokenize method (tuple)
    mysql_cred = "credentials/mysql.json"

    # Preprocess created_at to datetime type
    created_time = time_conversion.local_time_conversion(data[3])

    # Create database connection
    conn = db_connect(mysql_cred)

    # Create cursor
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO rans_ersp_rec (message_id, message, ref_num, created_time, source_handle, source_id) "
               "VALUES (%s, %s, %s, %s, %s, %s) ", (data[0], data[1], data[2], created_time, data[4], data[5]))

        conn.commit()

        print("Record Saved on RECEIVED table for ERSP!!")

    except pymysql.err.IntegrityError as e:
        print("MySQL Error: " + str(e))


    cur.close()
    conn.close()


# For notifications to Informant after ERSP response
def insert_send_informant(twitter_data):
    # Variables
    data = twitter_data     #Result from tokenize method (tuple)
    mysql_cred = "credentials/mysql.json"

    # Preprocess created_at to datetime type
    created_time = time_conversion.local_time_conversion(data[3])

    # Create database connection
    conn = db_connect(mysql_cred)

    # Create cursor
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO rans_informant_send (message_id, message, ref_num, created_time, destination_handle, destination_id) "
               "VALUES (%s, %s, %s, %s, %s, %s) ", (data[0], data[1], data[2], created_time, data[4], data[5]))

        conn.commit()

        print("Record Saved on SENT table for Informant!!")

    except pymysql.err.IntegrityError as e:
        print("MySQL Error: " + str(e))


    cur.close()
    conn.close()

# Extract multiple data from database
def extract_from_dbs(mySQL_query):

    mysql_cred = "credentials/mysql.json"

    # Create database connection
    conn = db_connect(mysql_cred)

    # Create cursor
    cur = conn.cursor()

    # MySQL query
    query = mySQL_query

    try:
        cur.execute(query)

        results = cur.fetchall()

        return results

    except pymysql.err.IntegrityError as e:
        print("MySQL Error: " + str(e))

    cur.close()
    conn.close()



# Extract  one data-item from database
def extract_from_db(mySQL_query):

    mysql_cred = "credentials/mysql.json"

    # Create database connection
    conn = db_connect(mysql_cred)

    # Create cursor
    cur = conn.cursor()

    # MySQL query
    query = mySQL_query

    try:
        cur.execute(query)

        results = cur.fetchone()

        return results

    except pymysql.err.IntegrityError as e:
        print("MySQL Error: " + str(e))

    cur.close()
    conn.close()



# Update confirm_status after informant's reply
def updateCONF_rec_messages(sender):

    mysql_cred = "credentials/mysql.json"

    # Create database connection
    conn = db_connect(mysql_cred)

    # Create cursor
    cur = conn.cursor()

    # Last tweet received from sender
    search_query = "SELECT MAX(message_id) FROM rans_informant_rec WHERE source_id= " + str(sender)

    cur.execute(search_query)

    result = cur.fetchone()

    tweet_ref = result[0]


    update_query = """UPDATE rans_informant_rec
                      SET conf_status = 1
                      WHERE source_id = %s AND message_id = %s"""

    data = (sender, tweet_ref)

    try:
        cur.execute(update_query, data)
        conn.commit()

        print("Record Updated: confirmation_status")

        return tweet_ref

    except pymysql.err.IntegrityError as e:
        print("MySQL Error: " + str(e))



    cur.close()
    conn.close()




# Update validation status of tweet
def updateVALID_rec_messages(identifier1, identifier2):

    mysql_cred = "credentials/mysql.json"

    # Create database connection
    conn = db_connect(mysql_cred)

    # Create cursor
    cur = conn.cursor()

    query = "SELECT valid_status FROM rans_informant_rec WHERE message_id = '" + str(identifier1) + "'"

    query_result = extract_from_db(query)

    if query_result[0]== 0:
        # update both past and current tweet records
        update_query = """UPDATE rans_informant_rec
                      SET valid_status = 1
                      WHERE message_id = %s OR message_id = %s"""


        data = (identifier1, identifier2)

        try:
            cur.execute(update_query, data)
            conn.commit()
            print("Record Updated : validation_status")

        except pymysql.err.IntegrityError as e:
            print("MySQL Error: " + str(e))

    else:
        # update current tweet record
        update_query = """UPDATE rans_informant_rec
                          SET valid_status = 1
                          WHERE message_id = %s """



        try:
            cur.execute(update_query, identifier2)
            conn.commit()
            print("Record Updated : validation_status")

        except pymysql.err.IntegrityError as e:
            print("MySQL Error: " + str(e))

    cur.close()
    conn.close()


# Update send_status after informant's reply
def updateSEND_rec_messages(reference):

    mysql_cred = "credentials/mysql.json"

    # Create database connection
    conn = db_connect(mysql_cred)

    # Create cursor
    cur = conn.cursor()

    # Check is send_status value
    query = "SELECT sent_status FROM rans_informant_rec WHERE message_id = '" + str(reference) + "'"

    query_result = extract_from_db(query)

    if(query_result[0] == 1):
        print("No update done. Message was already sent to ERSP.")

    else:
        # Perform update
        update_query = """UPDATE rans_informant_rec
                        SET sent_status = 1
                        WHERE message_id = %s"""

        try:
            cur.execute(update_query, reference)
            conn.commit()

            print("Record Updated: sent_status")


        except pymysql.err.IntegrityError as e:
            print("MySQL Error: " + str(e))



    cur.close()
    conn.close()

# Update send_status after informant's reply
def updateREPLIED_rec_messages(reference):

    mysql_cred = "credentials/mysql.json"

    # Create database connection
    conn = db_connect(mysql_cred)

    # Create cursor
    cur = conn.cursor()

    # Check is replied_status value
    query = "SELECT replied_status FROM rans_informant_rec WHERE message_id = '" + str(reference) + "'"

    query_result = extract_from_db(query)

    if(query_result[0] == 1):
        print("No update done. Message was already sent to ERSP.")

    else:
        # Perform update
        update_query = """UPDATE rans_informant_rec
                        SET replied_status = 1
                        WHERE message_id = %s"""

        try:
            cur.execute(update_query, reference)
            conn.commit()

            print("Record Updated: sent_status")


        except pymysql.err.IntegrityError as e:
            print("MySQL Error: " + str(e))

    cur.close()
    conn.close()


# Module for common messages
def common_tweets_checker(reference):
    # Check if previous tweet as well as future tweets if replied to
    query = "SELECT message, created_time, source_handle from rans_informant_rec WHERE message_id= '" + str(reference) + "'"

    query_results = extract_from_db(query)

    message_time = query_results[1]
    used_message = query_results[0]

    tweet_list = [(reference, query_results[2])]

    # Return time boundary i.e. 15 min before and after
    times = time_conversion.time_range(message_time)

    # Get all messages that have not been sent to informant after reply
    query2 = "SELECT message_id, message, source_handle FROM rans_informant_rec WHERE created_time >= '" + str(times[0]) + \
             " 'AND created_time < ' " + str(times[1]) + "' AND sent_status = 0"

    query2_results = extract_from_dbs(query2)

    if len(query2_results) != 0:
        for result in query2_results:
            # Check similarity in tweets
            string_match = text_validation.tweet_validation(result[1], used_message)

            if (string_match >= 60):
                data = (result[0], result[2])
                tweet_list.append(data)

    print(tweet_list)
    return tweet_list