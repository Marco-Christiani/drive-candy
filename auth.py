import jwt
import requests
import os
from datetime import datetime, timedelta

key = os.environ['KEY']

fields = {
    "iss": "service-account@hyperqubesite.iam.gserviceaccount.com",
    "scope": "https://www.googleapis.com/auth/drive",
    "aud": "https://www.googleapis.com/oauth2/v4/token",
    "iat": datetime.utcnow(),
    "exp": datetime.utcnow()+timedelta(hours=1),
}

encoded_jwt = jwt.encode(fields, key, algorithm='HS256')
resp = requests.post('https://www.googleapis.com/oauth2/v4/token',
                     data={'grant_type': 'urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer', 'assertion': encoded_jwt})
print(resp)
