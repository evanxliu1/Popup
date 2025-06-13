# DesktopNoti

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
- Download the `credentials.json` and place it in your project folder

### 2. Prepare Your Data
- Create a Google Sheet with your messages (one per row)
- Create a Google Drive folder with your images
- Share both with your Google account

### 3. Configure
- Copy and edit `config.json`:
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
  python notification.py
  ```
- On first run, a browser will open for Google login/consent.

---

## Packaging as a Standalone App (Mac & Windows)

### 1. Generate App Icons
- Make sure `IMG_4278.JPG` exists in `downloaded_images/`.
- Run:
  ```sh
  pip install pillow icnsutil
  python make_icons.py
  ```
- This creates `app_icon.icns` (Mac) and `app_icon.ico` (Windows) in the project root.

### 2. Build with PyInstaller
- Install PyInstaller:
  ```sh
  pip install pyinstaller
  ```
- **Mac:**
  ```sh
  pyinstaller pyinstaller-mac.spec.txt
  # Output app in dist/DesktopNoti
  ```
- **Windows:**
  ```sh
  pyinstaller pyinstaller-win.spec.txt
  # Output app in dist/DesktopNoti
  ```
- The resulting app is portable and can be sent to others. All dependencies are bundled. (On Mac, right-click > Open on first launch due to Gatekeeper.)

### 3. Credentials & Config
- `credentials.json`, `token.json`, and `config.json` must be present in the app directory. Share these only if you are comfortable giving access to your Google Sheets/Drive.

---

## Project Structure
- `notification.py` — Main script
- `requirements.txt` — Python dependencies
- `pyinstaller-mac.spec.txt` — Mac app build spec
- `pyinstaller-win.spec.txt` — Windows app build spec
- `make_icons.py` — Utility to generate app icons from your JPG
- `app_icon.icns`/`app_icon.ico` — Generated icons for app packaging
- `downloaded_images/` — Images for notifications & source for app icon
- `credentials.json`, `token.json`, `config.json` — Google API credentials/config (required for app to run)

---

## Notes
- The notification popup is cross-platform and uses Tkinter (no system tray icon needed).
- Credentials and config files are included for sharing as requested. Remove them from `.gitignore` if you want to keep them private.
- For security, do not share your Google credentials/token unless you trust the recipient.
- If you want to customize the icon, replace `IMG_4278.JPG` and re-run `make_icons.py`.

## License
MIT
