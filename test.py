
from drivecandy import drive


def demo():
    # Create a drive object
    # drive = drive.Drive(iss=<issuer-claim-here>, key=<private-key-here>)
    d = drive.Drive()  # using environment vars ISS and KEY

    # List files owned by account authenticated above
    # demo_print(d.get_files())

    drives = d.get_drives()
    # demo_print(drives)

    drive_id = drives['drives'][0]['id']
    drive_contents = d.get_drive_contents(drive_id)
    demo_print(drive_contents)
    demo_print(d.get_drive_permissions(drive_id))
    # https://www.googleapis.com/drive/v3/files/0AKoXpkbilrmLUk9PVA/permissions/?
    # supportsAllDrives=True
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
