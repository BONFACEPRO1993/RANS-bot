# DEFAULT LIBRARIES
from datetime import datetime, timedelta
import time

# Convert twitter time_format to datetime
def local_time_conversion(raw_time):
    # Create timestamp i.e. both unix and datetime data structure
    clean_timestamp = datetime.strptime(raw_time, '%a %b %d %H:%M:%S +0000 %Y')
    unix_timestamp = time.mktime(clean_timestamp.timetuple())

    offset_hours = +3  # offset in hours for EAT timezone

    # account for offset from UTC using timedelta
    local_timestamp = clean_timestamp + timedelta(hours=offset_hours)

    return local_timestamp

def time_difference(tweet_time, past_tweet_time):
    fmt = '%Y-%m-%d %H:%M:%S'

    time1 = datetime.strptime(past_tweet_time, fmt)
    time2 = datetime.strptime(tweet_time, fmt)

    # Convert to Unix timestamp
    time1_ts = time.mktime(time1.timetuple())
    time2_ts = time.mktime(time2.timetuple())

    # They are now in seconds, subtract and then divide by 60 to get minutes.
    diff = int(time2_ts - time1_ts) / 60

    print(diff)

# Computes time 15 minutes before tweet created_at time
def time_limit(tweet_time):

    time_check = tweet_time - timedelta(minutes=15)

    return time_check

# Computes time-range, 15 minutes before and after tweet created_at time
def time_range(tweet_time):

    lower_bound = tweet_time - timedelta(minutes=15)

    upper_bound = tweet_time + timedelta(minutes=15)

    result = (lower_bound, upper_bound)

    return result


def get_current_time():
    # Get time
    current_time = time.strftime('%H:%M:%S')

    return current_time