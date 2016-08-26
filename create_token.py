import jwt
import Crypto.PublicKey.RSA as RSA
import datetime
import os
import io
import json

path = realpath = os.path.dirname(os.path.realpath(__file__))
filename = 'service_account'
with io.open('{0}/{1}.json'.format(path, filename),
             encoding='utf-8') as f:
    creds = json.loads(f.read())

# Get your service account's email address and private key from the JSON key file
service_account_email = creds['client_email']
private_key = RSA.importKey(creds['private_key'])

def create_custom_token(uid, is_premium_account):
  try:
    payload = {
      "iss": service_account_email,
      "sub": service_account_email,
      "aud": "https://identitytoolkit.googleapis.com/google.identity.identitytoolkit.v1.IdentityToolkit",
      "uid": uid,
      "claims": {
        "premium_account": is_premium_account
      }
    }
    exp = datetime.timedelta(minutes=60)
    return jwt.generate_jwt(payload, private_key, "RS256", exp)
  except Exception as e:
    print("Error creating custom token: " + e.message)
    return None
