## drive-candy (Google Drive v3 API)
### Python package for Google REST API
To set up, you have 2 authorization options:
1. Using service account: 

   Create a service account and save the email address and private key and set as environment variables "ISS" and "KEY" or pass to drive constructor.
2. Using your own account **not yet supported**

   Create oauth2 credentials from Google Console
```python
from drivecandy import drive
my_drive = drive.Drive()
```
