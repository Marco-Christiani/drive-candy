"""
Wrapper for the Google Drive HTTP REST API.
"""
import jwt
import requests
import os
from exceptions import TokenRequired, InvalidTimeToLive
from datetime import datetime, timedelta

"""
Google Drive instance
"""


class Drive:
    def __init__(self):
        key = os.environ['KEY']
        self.key = key.replace('\\n', '\n')
        self.base_url = 'https://www.googleapis.com/drive/v3/'
        self.access_token = None

    def get_token(self, iss, ttl=60):
        """
        Requests an access token from Google by sending a JWT.

        Args:
            iss: the issuer claim identifies the principal that issued the
            JWT. The iss value is a case-sensitive string containing a
            StringOrURI value. (rfc7519 section-4.1.1)

            ttl: time to live in minutes, max ttl for an access token is
            60 minutes
        """
        if not (1 <= ttl <= 60):
            raise InvalidTimeToLive(
                f'get_token({iss}, ttl={ttl})',
                'Please enter a valid ttl between '
                '1 and 60 minutes.')
        fields = {
            "iss": iss,
            "scope": "https://www.googleapis.com/auth/drive",
            "aud": "https://www.googleapis.com/oauth2/v4/token",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=ttl)
        }

        encoded_jwt = jwt.encode(fields, self.key, algorithm='RS256')
        grant_type = 'urn:ietf:params:oauth:grant-type:jwt-bearer'

        resp = requests.post('https://www.googleapis.com/oauth2/v4/token',
                             data={
                                 'grant_type': grant_type,
                                 'assertion': encoded_jwt
                             })

        try:
            self.access_token = resp.json()['access_token']
        except KeyError:
            print('No access token was sent.', resp.json())

        return self.access_token

    def get_file_list(self):
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

    def get_drive_contents(self, drive_id):
        url = self.build_url(f'files/', driveId=drive_id,
                             includeItemsFromAllDrives='True', corpora='drive',
                             supportsAllDrives='True')
        print(url)
        resp = requests.get(url)
        return resp.json()

    # Helper Functions ---------------------------------------------------------
    def build_url_backup(self, path, **kwargs):
        access_token = kwargs.get('access_token', None)
        if not access_token:
            access_token = self.access_token
        if not access_token:
            exp = f'build_url(path={path}, access_token=self.access_token)'
            msg = 'No access_token. Get an access token by calling getToken()' \
                  ' or provide one as a parameter.'
            # raise Exception(msg)
            raise TokenRequired(exp, msg)
        return f'{self.base_url}{path}?access_token={access_token}'

    def build_url(self, path, **kwargs):
        try:
            access_token = kwargs.pop('access_token')
        except KeyError:
            access_token = self.access_token
        if not access_token:  # self.access token has not been set
            exp = f'build_url(path={path}, access_token=self.access_token)'
            msg = 'No access_token. Get an access token by calling getToken()' \
                  ' or provide one as a parameter.'
            raise TokenRequired(exp, msg)
        # Parse kwargs
        if len(kwargs) != 0:
            args = '&'.join("{!s}={!s}".format(key, val)
                            for (key, val) in kwargs.items())
            return f'{self.base_url}{path}?access_token={access_token}&{args}'

        return f'{self.base_url}{path}?access_token={access_token}'


def main():
    drive = Drive()
    # drive.get_token("<service-account-here>")
    drive.get_token("zerotrust@zerotrust-246114.iam.gserviceaccount.com")
    # drive.get_token("service-account-2@hyperqubesite.iam.gserviceaccount.com")
    print(drive.get_file_list())
    print('-' * 50)
    print()
    # print(drive.get_file_permissions('<any-file-id>'))
    # print(drive.get_file_permissions('0B5F0TQr2Zeblc3RhcnRlcl9maWxl'))
    print('-' * 50)
    print()
    drives = drive.get_drives()
    print(drives)
    print('-' * 50)
    print()
    print(drive.get_drive_contents(drives['drives'][0]['id']))


if __name__ == '__main__':
    main()
