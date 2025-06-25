import random
import io
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from notification.config import SPREADSHEET_ID, SHEET_RANGE, DRIVE_FOLDER_ID, TOKEN_PATH, CREDENTIALS_PATH, DOWNLOAD_DIR

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
]

def get_google_creds():
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    return creds

creds = get_google_creds()
sheets_service = build('sheets', 'v4', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

def get_random_message():
    try:
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID, range=SHEET_RANGE).execute()
        values = result.get('values', [])
        messages = [row[0] for row in values if row]
        if not messages:
            return 'You are loved!'
        return random.choice(messages)
    except Exception as e:
        logging.error(f"Failed to fetch messages: {e}")
        return 'You are loved!'

def get_random_image():
    try:
        results = drive_service.files().list(
            q=f"'{DRIVE_FOLDER_ID}' in parents and mimeType contains 'image/' and trashed = false",
            fields="files(id, name, mimeType)",
        ).execute()
        files = results.get('files', [])
        if not files:
            logging.warning("No images found in Drive folder.")
            return None
        file = random.choice(files)
        file_id = file['id']
        file_name = file['name']
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        fh.seek(0)
        local_path = DOWNLOAD_DIR / file_name
        with open(local_path, 'wb') as f:
            f.write(fh.read())
        return str(local_path)
    except Exception as e:
        logging.error(f"Failed to fetch image: {e}")
        return None
