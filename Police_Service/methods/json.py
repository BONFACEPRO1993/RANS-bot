# DEFAULT LIBRARIES
import json

def load_from_file(filename):
    # Load json file from credentials
    data_file = open(filename)
    auth_data = json.load(data_file)
    return auth_data

def load_from_variable(variable):
    data = json.loads(variable)

    return data

def load_from_variable2(variable):
    data = variable._json

    return data