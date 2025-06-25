import time
from notification.google_api import get_random_message, get_random_image
from notification.popup import show_notification
from notification.config import NOTIF_INTERVAL
import logging

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
