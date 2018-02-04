import re

# Remove twitter handles from text
def handle_remover(text):

    string = text

    # Regex to search all twitter handles
    handles = re.findall(r'@[A-Za-z0-9_]+', string)

    for handle in handles:
        # Remove twitter handles
        string = string.replace(handle,'')

    return string

# Remove time from text
def time_remover(text):

    string = text

    # Regex to search all twitter handles
    times = re.findall(r'[0-2][0-9:]+', string)

    for result in times:
        # Remove twitter handles
        string = string.replace(result, '')


    return string

# Removes unwanted strings in text
def text_remover(text):

    string = text

    # Unwanted strings
    string = string.replace("RT : ", "")
    string = string.replace("…", "")

    # Unwanted spaces
    string = string.lstrip()
    string = string.rstrip()

    if not string:
        string = "No text captured!!"

    return string

