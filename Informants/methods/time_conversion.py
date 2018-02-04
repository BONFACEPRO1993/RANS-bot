# DEFAULT LIBRARIES
from datetime import datetime, timedelta
import time

def local_time_conversion(raw_time):
    # Create timestamp i.e. both unix and datetime data structure
    clean_timestamp = datetime.strptime(raw_time, '%a %b %d %H:%M:%S +0000 %Y')
    unix_timestamp = time.mktime(clean_timestamp.timetuple())

    offset_hours = +3  # offset in hours for EAT timezone

    # account for offset from UTC using timedelta
    local_timestamp = clean_timestamp + timedelta(hours=offset_hours)

    result_time = (unix_timestamp, local_timestamp)

    return result_time

def get_current_time():
    # Get time
    current_time = time.strftime('%H:%M:%S')

    return current_time