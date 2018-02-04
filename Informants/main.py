# INTERNAL LIBRARIES
from Informants.api import twitterAPI
from Informants.methods import sql


# JSON files
# Informant 1 twitter credentials
twitter1 = "credentials/informant_1/get_twitter.json"
twitter2 = "credentials/informant_1/post_twitter.json"

# Informant 2 twitter credentials
twitter3 = "credentials/informant_2/get_twitter.json"
twitter4 = "credentials/informant_2/post_twitter.json"

#MySQL credentials
mysql_db = "credentials/mysql.json"

# Search Queries
query1 = "ma3route accident at"
query2 = "kenyanTraffic accident at"

# MySQL Queries
sql_query = "SELECT `id`,`tweet` FROM captured_tweets2;"

twitterAPI.post_dm(twitter1,mysql_db,sql_query)
# sql.extract_from_db(mysql_db,sql_query)
# sql.insert_db(mysql_db, query2, twitter3)
# sql.update_db(mysql_db, sql_query)
# sql.tokenize(query1, twitter2)

# twitterAPI.twitter_auth(twitter2)




