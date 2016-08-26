from create_token import create_custom_token
import pyrebase
import os
import json_utils

# auth to firebase
def create_firebase():
    realpath = os.path.dirname(os.path.realpath(__file__))
    # config has to be an object with creds
    config = json_utils.load_json(realpath, 'creds')
    # service account has to be file path to [credentials].json
    config['serviceAccount'] = realpath + '/service_account.json'
    # create_custom_token('z31tg31st')
    return pyrebase.initialize_app(config)

