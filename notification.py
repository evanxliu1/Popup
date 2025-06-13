"""
DesktopNoti: Show random cute messages and images from Google Sheets/Drive as desktop notifications.
Modern, config-driven, OAuth-based, cross-platform.
"""
import random
import json
import io
import time
import logging
from pathlib import Path
import random
import json
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# --- CUTE CUSTOM POPUP NOTIFICATION ---
def show_notification(message, image_path=None, duration=8):
    """
    Show a cute custom popup window with an image and a message below.
    The popup auto-closes after `duration` seconds.
    """
    root = tk.Tk()
    root.title("💖 Cute Message! 💖")
    root.configure(bg="#ffe4ec")  # Soft pink background
    root.attributes('-topmost', True)
    root.resizable(False, False)
    # Remove overrideredirect(True) so the window has a border and X button
    # root.overrideredirect(True)

    # Set window size and position (medium size, centered)
    win_w, win_h = 340, 420
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w // 2) - (win_w // 2)
    y = (screen_h // 2) - (win_h // 2)
    root.geometry(f"{win_w}x{win_h}+{x}+{y}")

    # Load and display image (rounded corners for extra cute)
    if image_path:
        try:
            img = Image.open(image_path)
            img = img.convert('RGBA')
            img.thumbnail((280, 280))
            # Optionally, add rounded corners
            from PIL import ImageDraw
            mask = Image.new('L', img.size, 0)
            corner_radius = 40
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle([(0, 0), img.size], corner_radius, fill=255)
            img.putalpha(mask)
            tk_img = ImageTk.PhotoImage(img)
            img_label = tk.Label(root, image=tk_img, bg="#ffe4ec", bd=0)
            img_label.image = tk_img  # Keep reference
            img_label.pack(pady=(30, 16))
        except Exception as e:
            img_label = tk.Label(root, text="(Image not found)", bg="#ffe4ec", fg="#d48fb6", font=("Comic Sans MS", 12, "italic"))
            img_label.pack(pady=(30, 16))
    else:
        img_label = tk.Label(root, text="(No image)", bg="#ffe4ec", fg="#d48fb6", font=("Comic Sans MS", 12, "italic"))
        img_label.pack(pady=(30, 16))

    # Display message below image
    msg_label = tk.Label(
        root,
        text=message,
        bg="#ffe4ec",
        fg="#d48fb6",
        font=("Comic Sans MS", 18, "bold"),
        wraplength=320,
        justify="center",
        pady=12
    )
    msg_label.pack()

    # Add a cute close button (optional, but popup will auto-close anyway)
    style = ttk.Style()
    style.configure("Cute.TButton", font=("Comic Sans MS", 12), foreground="#fff", background="#f8a1d1", borderwidth=0)
    close_btn = ttk.Button(root, text="OK! 💕", style="Cute.TButton", command=root.destroy)
    close_btn.pack(pady=(10, 22))
    # User can now also close the window with the standard X button

    # Auto-close after duration seconds
    root.after(duration * 1000, root.destroy)
    root.mainloop()


from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from PIL import Image

# --- CONFIGURATION ---
SCRIPT_DIR = Path(__file__).parent.resolve()
CONFIG_PATH = SCRIPT_DIR / 'config.json'
TOKEN_PATH = SCRIPT_DIR / 'token.json'
CREDENTIALS_PATH = SCRIPT_DIR / 'credentials.json'  # Downloaded from Google Cloud Console

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# --- LOAD CONFIG ---
def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

config = load_config()
SPREADSHEET_ID = config['spreadsheet_id']
SHEET_RANGE = config['sheet_range']
DRIVE_FOLDER_ID = config['drive_folder_id']
NOTIF_INTERVAL = int(config.get('notification_interval_minutes', 30))
DOWNLOAD_DIR = Path(config.get('download_dir', SCRIPT_DIR / 'downloaded_images')).expanduser()
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

# --- GOOGLE AUTH ---
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

# --- FETCH RANDOM MESSAGE ---
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

# --- FETCH RANDOM IMAGE FROM DRIVE FOLDER ---
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

# --- MAIN LOOP ---
def main_loop():
    while True:
        message = get_random_message()
        image_path = get_random_image()
        if image_path:
            show_notification(message, image_path)
        else:
            show_notification(message)
        logging.info(f"Notification sent: {message} (image: {image_path})")
        time.sleep(NOTIF_INTERVAL * 60)

if __name__ == "__main__":
    print("Starting the notification script...")
    main_loop()
