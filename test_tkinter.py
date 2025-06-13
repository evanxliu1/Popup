import tkinter as tk

root = tk.Tk()
root.title("Tkinter Test")
root.geometry("300x150")
label = tk.Label(root, text="If you see this window, Tkinter works!", font=("Arial", 14))
label.pack(pady=30)
root.mainloop()
