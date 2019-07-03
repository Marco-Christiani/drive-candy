'''
Wrapper for the Google Drive REST API using HTTP.
'''
import jwt
import requests
import os
from exceptions import *
from datetime import datetime, timedelta

'''
Google Drive instance
'''


class Drive:
    def __init__(self):
        key = os.environ['KEY']
        self.key = key.replace('\\n', '\n')
        self.base_url = 'https://www.googleapis.com/drive/v2/'
        self.access_token = None

    '''
    Requests an access token from Google by sending a JWT.
    
    Args:
        iss: the issuer claim identifies the principal that issued the
        JWT. The "iss" value is a case-sensitive string containing a StringOrURI
        value. (rfc7519 section-4.1.1)
        ttl: time to live in minutes, max ttl for an access token is 60 minutes
    
    '''

    def get_token(self, iss, ttl=60):
        if not (1 <= ttl <= 60):
            raise InvalidTimeToLive(f'get_token({iss}, ttl={ttl})',
                                    'Please enter a valid ttl between 1 and 60 minutes.')
        fields = {
            "iss": iss,
            "scope": "https://www.googleapis.com/auth/drive",
            "aud": "https://www.googleapis.com/oauth2/v4/token",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=ttl)
        }

        encoded_jwt = jwt.encode(fields, self.key, algorithm='RS256')

        resp = requests.post('https://www.googleapis.com/oauth2/v4/token',
                             data={
                                 'grant_type':
                                     'urn:ietf:params:oauth:grant-type:jwt-bearer',
                                 'assertion': encoded_jwt
                             })

        self.access_token = resp.json()['access_token']

        return self.access_token

    def get_file_list(self):
        # url = f'{base_url}files/?access_token=' + access_token
        url = self.build_url('files/')
        resp = requests.get(url)
        return resp.json()

    def get_file_permissions(self, file_id):
        url = self.build_url(f'files/{file_id}/permissions')
        resp = requests.get(url)
        return resp.json()

    def get_drives(self):
        url = self.build_url(f'drives/')
        resp = requests.get(url)
        return resp.json()

    def build_url(self, path, **kwargs):
        access_token = kwargs.get('access_token', None)
        if not access_token:
            access_token = self.access_token
        if not access_token:
            exp = f'build_url(path={path}, access_token=self.access_token)'
            msg = 'No access_token. Get an access token by calling getToken() ' \
                  'or provide one as a parameter.'
            # raise Exception(msg)
            raise TokenRequired(exp, msg)
        return f'{self.base_url}{path}?access_token={access_token}'


def main():
    drive = Drive()
    drive.get_token("<service-account-here>")
    print(drive.get_file_list())
    print('-' * 50)
    print()
    print(drive.get_file_permissions('<any-file-id>'))
    print('-' * 50)
    print()
    print(drive.get_drives())


if __name__ == '__main__':
    main()
