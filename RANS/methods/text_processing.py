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

    # Removes links from texts
    string = re.sub(r"http\S+", "", string)

    # Unwanted spaces
    string = string.lstrip()
    string = string.rstrip()

    if not string:
        string = "No text captured!!"

    return string

def ref_no_extractor(text):

    string = text

    # Search Reference number
    ref_list = re.findall(r'\[([0-9]+)]', string)

    ref_num = ref_list[0]

    return ref_num

def common_text_remover(text):

    text_content = text.split()
    count = 0

    string = ""

    while len(text_content):
        if text_content[0] == "on" or text_content[0] == "near" or text_content[0] == "at" or text_content[0] =="along":
            text_content.pop(0)
            break

        text_content.pop(0)



    for text in text_content:
        string = string + " " + text

    return string