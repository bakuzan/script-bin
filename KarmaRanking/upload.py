from __future__ import print_function
import pickle
import os
import os.path
from googleapiclient.discovery import build, MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from log import log

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def upload_files(filenames):
    """Basic usage of the Drive v3 API.
    Upload files to gdrive
    """
    log("Authorising google drive...")

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    drive_service = build('drive', 'v3', credentials=creds)

    folder_id = os.environ.get("DRIVE_FOLDER_ID")
    log("Uploading files to google drive...")

    for filename in filenames:
        name = filename.split('\\').pop()
        file_metadata = {'name': name, 'parents': [folder_id]}
        media = MediaFileUpload(filename,
                                mimetype='image/png')
        file = drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        print('Uploaded %s, File Id: %s' % (name, file.get('id')))

    log("Uploading complete.")
