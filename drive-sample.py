"""
Sample usage of gcandy:
    1. prints files owned by account used for auth
    2. prints shared drives
    3. prints shared drive's contents
    4. prints a file's permissions within a shared drive

1. Using service account:
    Obtain your ISS (email address) and private key values
    from Google Console and set as environment variables "ISS" and "KEY" or pass to
    function (see comments).
2. Using your own account:
    Create oauth2 credentials from Google Console

More information on ISS and private key here:
https://developers.google.com/identity/protocols/OAuth2ServiceAccount
"""
from drivecandy import drive


def demo():
    # Create a drive object
    # drive = drive.Drive(iss=<issuer-claim-here>, key=<private-key-here>)
    d = drive.Drive()  # using environment vars ISS and KEY

    # List files owned by account authenticated above
    demo_print(d.get_files())

    drives = d.get_drives()
    demo_print(drives)

    drive_id = drives['drives'][0]['id']
    drive_contents = d.get_drive_contents(drive_id)
    demo_print(drive_contents)

    file_id = drive_contents['files'][0]['id']
    demo_print(d.get_file_permissions(file_id))

    # Let's say our token expires (although the default ttl is 60 minutes)
    demo_print("Getting a new token...")
    d.get_token()
    demo_print(d.get_files())  # test our new token

    # d.get_token("t", "x", "s")


def demo_print(string):
    print(string)
    print('-' * 100)
    print()


if __name__ == '__main__':
    demo()
