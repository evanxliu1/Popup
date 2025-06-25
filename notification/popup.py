import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

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

    # Properly handle window close (X button)
    root.protocol("WM_DELETE_WINDOW", root.destroy)

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
            from PIL import ImageDraw
            mask = Image.new('L', img.size, 0)
            corner_radius = 40
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle([(0, 0), img.size], corner_radius, fill=255)
            img.putalpha(mask)
            tk_img = ImageTk.PhotoImage(img)
            img_label = tk.Label(root, image=tk_img, bg="#ffe4ec", bd=0)
            img_label.image = tk_img
            img_label.pack(pady=(30, 16))
        except Exception:
            img_label = tk.Label(root, text="(Image not found)", bg="#ffe4ec", fg="#d48fb6", font=("Comic Sans MS", 12, "italic"))
            img_label.pack(pady=(30, 16))
    else:
        img_label = tk.Label(root, text="(No image)", bg="#ffe4ec", fg="#d48fb6", font=("Comic Sans MS", 12, "italic"))
        img_label.pack(pady=(30, 16))

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

    style = ttk.Style()
    style.configure("Cute.TButton", font=("Comic Sans MS", 12), foreground="#fff", background="#f8a1d1", borderwidth=0)
    close_btn = ttk.Button(root, text="OK! 💕", style="Cute.TButton", command=root.destroy)
    close_btn.pack(pady=(10, 22))

    root.after(duration * 1000, root.destroy)
    root.mainloop()
