import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent.resolve()
CONFIG_PATH = SCRIPT_DIR / 'config' / 'config.json'
TOKEN_PATH = SCRIPT_DIR / 'config' / 'token.json'
CREDENTIALS_PATH = SCRIPT_DIR / 'config' / 'credentials.json'
DOWNLOAD_DIR = SCRIPT_DIR / 'downloaded_images'

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

SPREADSHEET_ID = config['spreadsheet_id']
SHEET_RANGE = config['sheet_range']
DRIVE_FOLDER_ID = config['drive_folder_id']
NOTIF_INTERVAL = int(config.get('notification_interval_minutes', 30))
DOWNLOAD_DIR = Path(config.get('download_dir', DOWNLOAD_DIR)).expanduser()
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
