# Popup!

Show random cute messages and images from Google Sheets and Drive as desktop notifications. 
Great for surprising your loved ones with sweet reminders!

## Features
- Randomly selects a message from a Google Sheet
- Randomly selects a photo from a Google Drive folder
- Shows a desktop notification with the message and image (as icon)
- Runs on a schedule (configurable)
- Cross-platform (Windows, Mac)

## Setup Instructions

### 1. Google Cloud Setup
- Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
- Create/select a project
- Enable the Google Drive API and Google Sheets API
- Configure the OAuth consent screen (External, add your email as test user)
- Create OAuth credentials: Credentials > Create Credentials > OAuth client ID > Desktop app
- Download the `credentials.json` and place it in the `config/` folder

### 2. Prepare Your Data
- Create a Google Sheet with your messages (one per row)
- Create a Google Drive folder with your images
- Share both with your Google account

### 3. Configure
- Copy and edit `config/config.json`:
  ```json
  {
    "spreadsheet_id": "YOUR_SPREADSHEET_ID",
    "sheet_range": "Sheet1!A:A",
    "drive_folder_id": "YOUR_DRIVE_FOLDER_ID",
    "notification_interval_minutes": 30,
    "download_dir": "downloaded_images"
  }
  ```
- Replace `YOUR_SPREADSHEET_ID` and `YOUR_DRIVE_FOLDER_ID` with your actual IDs.

### 4. Install Requirements
- (Recommended) Create and activate a Python virtual environment:
  ```sh
  python3 -m venv .venv
  source .venv/bin/activate
  ```
- Install dependencies:
  ```sh
  pip install -r requirements.txt
  ```

### 5. Run (Development)
- Run the script:
  ```sh
  python -m notification.main
  ```
- On first run, a browser will open for Google login/consent.

---

## Packaging as a Standalone App (Mac & Windows)

### 1. Prepare App Icons
- Place your icon files in `assets/` as `app_icon.icns`, `app_icon.ico`, and `icon_1024.png`.

### 2. Build with PyInstaller
- Install PyInstaller:
  ```sh
  pip install pyinstaller
  ```
- **Mac:**
  ```sh
  ./scripts/build_mac.sh
  # Output app in DesktopNoti.app
  ```
- **Windows:**
  ```bat
  scripts\build_windows.bat
  # Output app in dist\DesktopNoti.exe
  ```
- The resulting app is portable and can be sent to others. All dependencies are bundled. (On Mac, right-click > Open on first launch due to Gatekeeper.)

### 3. Credentials & Config
- `credentials.json`, `token.json`, and `config.json` must be present in the `config/` directory. Share these only if you are comfortable giving access to your Google Sheets/Drive.

---

## Project Structure
```
DesktopNoti/
├── notification/           # All source code
│   ├── __init__.py
│   ├── main.py             # Entry point
│   ├── notifier.py         # Notification main loop
│   ├── popup.py            # Popup window logic
│   ├── config.py           # Config loading
│   └── google_api.py       # Google Sheets/Drive logic
├── assets/                 # Icons, images
│   ├── app_icon.icns
│   ├── app_icon.ico
│   └── icon_1024.png
├── config/                 # Configuration and credentials (not tracked by git)
│   ├── config.json
│   ├── credentials.json
│   └── token.json
├── scripts/                # Build and packaging scripts
│   ├── build_mac.sh
│   └── build_windows.bat
├── downloaded_images/      # Downloaded images (gitignored)
├── .gitignore
├── README.md
├── requirements.txt
```

## Notes
- The notification popup is cross-platform and uses Tkinter (no system tray icon needed).
- Credentials and config files are included for sharing as requested. Remove them from `.gitignore` if you want to keep them private.
- For security, do not share your Google credentials/token unless you trust the recipient.
- If you want to customize the icon, replace the files in `assets/`.

## License
MIT
