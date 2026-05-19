from notifypy import Notify
import time
import threading
import requests
from bs4 import BeautifulSoup
import datetime


running = False
prev_href = ""

def get_latest_notification():
    base_url = "https://www.acs.uns.ac.rs"
    url = f"{base_url}/sr"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return f"Greška pri učitavanju: {e}"

    soup = BeautifulSoup(response.text, "html.parser")

    link = soup.select_one('a[href^="/sr/node/"]')

    if link:
        title = link.get("title") or link.text.strip()
        href = link.get("href")
        poslednja_cetiri = href[-4:]
        return f"{title}", poslednja_cetiri
    else:
        return "Nema pronađenih obaveštenja."

import customtkinter as ctk

ctk.set_appearance_mode("dark") 
app = ctk.CTk()
window_width = 500
window_height = 400
app.geometry("500x400")
app.title("CustomTkinter GUI")

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

app.geometry(f"{window_width}x{window_height}+{x}+{y}")

def on_click():

    global running, get_latest_notification, hour, minute
    if running:
        return 
    running = True

    def loop():
        global prev_href
        print("Starteed loop")
        while running:
            str, now_herf =  get_latest_notification()
            notification = Notify()
            if(prev_href == now_herf):
                notification.title = "OLD"
            else:
                notification.title = "***NEW***"
                notification.audio = "new.wav"
            notification.message = str
            notification.send()
            time.sleep(60)
            prev_href = now_herf
        print("Stopped loop.")

    threading.Thread(target=loop, daemon=True).start()

def end_click():
    global running
    running = False
    

button = ctk.CTkButton(app, text="Click Me", command=on_click)
button.pack(pady=50)
button2 = ctk.CTkButton(app, text="END", command=end_click)
button2.pack(pady=50)

app.mainloop()
