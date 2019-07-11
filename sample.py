"""
Sample usage of drivecandy:
    1. prints files owned by account used for auth
    2. prints shared drives
    3. prints shared drive's contents
    4. prints a file's permissions within a shared drive

Before running sample obtain your ISS (email address) and private key values
from Google Console and set as environment variables "ISS" and "KEY" or pass to
function (see comments).

More information on ISS and private key here:
https://developers.google.com/identity/protocols/OAuth2ServiceAccount
"""
import drivecandy.drive as gdrive


def demo():
    # Create a drive object
    # drive = drivecandy.Drive(iss=<issuer-claim-here>, key=<private-key-here>)
    # drive = drivecandy.drive.Drive()  # using environment vars ISS and KEY
    drive = gdrive.Drive()  # using environment vars ISS and KEY

    # List files owned by account authenticated above
    demo_print(drive.get_files())

    drives = drive.get_drives()
    demo_print(drives)

    drive_id = drives['drives'][0]['id']
    drive_contents = drive.get_drive_contents(drive_id)
    demo_print(drive_contents)

    file_id = drive_contents['files'][0]['id']
    demo_print(drive.get_file_permissions(file_id))

    # Let's say our token expires (although the default ttl is 60 minutes)
    demo_print("Getting a new token...")
    drive.get_token()
    demo_print(drive.get_files())  # test our new token

    # drive.get_token("t", "x", "s")


def demo_print(string):
    print(string)
    print('-' * 100)
    print()


if __name__ == '__main__':
    demo()
