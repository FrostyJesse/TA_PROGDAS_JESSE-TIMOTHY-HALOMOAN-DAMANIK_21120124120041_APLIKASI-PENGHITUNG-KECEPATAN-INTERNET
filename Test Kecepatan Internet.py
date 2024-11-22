import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Canvas
from datetime import datetime
import math
import requests
import speedtest

def is_connected():  #Function / Modul 4
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except requests.ConnectionError:
        return False

def run_speed_test():      #Pengkondisian / Modul 2
    if not is_connected():
        messagebox.showerror("No Internet Connection", "The device is not connected to the internet.")
        return

    internet_speed = speedtest.Speedtest()
    internet_speed.get_best_server()
    ping = internet_speed.results.ping
    download_byte = internet_speed.download()
    upload_byte = internet_speed.upload()
    download = bytes_to_mb(download_byte)
    upload = bytes_to_mb(upload_byte)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    isp = isp_var.get() 
    connection = "LAN" if connection_var.get() == 1 else "WiFi" #Pengkondisian / Modul 2

    result = {                   #Variabel / Modul 1
        "timestamp": timestamp,
        "ping": round(ping, 2),  #Tipe Data Integer / Modul 1
        "download": download,
        "upload": upload,
        "isp": isp,
        "connection": connection,
    }
    speed_stack.push(result)

    ping_label.config(text=f"Ping: {result['ping']} ms")
    download_label.config(text=f"Download: {result['download']}")
    upload_label.config(text=f"Upload: {result['upload']}")


def bytes_to_mb(size_bytes):
    i = int(math.floor(math.log(size_bytes, 1024)))
    megabit = math.pow(1024, i)
    size = round(size_bytes / megabit, 2)
    return f"{size} Mbps"

class SpeedTestStack:     # Array/Class (OOP/Stack & Queue) / Modul 1 & 5 & 7 
    def __init__(self):   # Constructor(OOP) / Modul 5
        self.stack = []

    def push(self, data):  # Method/Setter / Modul 4 & 6
        self.stack.append(data)

    def is_empty(self):
        return len(self.stack) == 0

    def get_all(self):  # Getter / Modul 6
        return self.stack

def update_start_button():  #Pengkondisian
    if connection_var.get() != 0 and isp_var.get():
        start_button.config(state="normal")
    else:
        start_button.config(state="disabled")

#GUI
def open_speed_test_window():
    root.withdraw()  

    global speed_test_window, ping_label, download_label, upload_label
    speed_test_window = tk.Toplevel()
    speed_test_window.title("Speed Test")
    speed_test_window.geometry("500x500")
    speed_test_window.configure(bg="black")

    def go_back():
        speed_test_window.destroy()
        root.deiconify()  

    tk.Label(speed_test_window, text="Results:", font=("Calibri", 20, "bold"), bg="black", fg="white").pack(pady=5)

    ping_label = tk.Label(speed_test_window, text="Ping: -- ms", bg="black", fg="white", font=("Calibri", 16))
    ping_label.pack(pady=5)

    download_label = tk.Label(speed_test_window, text="Download: -- Mbps", bg="black", fg="white", font=("Calibri", 16))
    download_label.pack(pady=5)

    upload_label = tk.Label(speed_test_window, text="Upload: -- Mbps", bg="black", fg="white", font=("Calibri", 16))
    upload_label.pack(pady=5)

    test_image = PhotoImage(file="wifi-small.png")  
    tk.Label(speed_test_window, image=test_image, bg="black").pack(pady=10)
    speed_test_window.image = test_image  

    
    bottom_frame = tk.Frame(speed_test_window, bg="black")
    bottom_frame.pack(side="bottom", fill="x", pady=10)

    
    back_button = tk.Button(bottom_frame, text="Back", command=go_back, bg="grey", fg="white", font=("Calibri", 12))
    back_button.pack(side="left", padx=10)

    
    action_frame = tk.Frame(bottom_frame, bg="black")
    action_frame.pack(side="right", padx=10)

    start_test_button = tk.Button(action_frame, text="Run Speed Test", command=run_speed_test, bg="light grey", fg="black", font=("Calibri", 12))
    start_test_button.pack(side="left", padx=5)

    history_button = tk.Button(action_frame, text="Show History", command=show_history, bg="light grey", fg="black", font=("Calibri", 12))
    history_button.pack(side="left", padx=5)

root = tk.Tk()
root.title("El Kecepatan Internet")
root.geometry("852x480")

bg = PhotoImage(file="Wheel.png") 
my_canvas = Canvas(root, width=852, height=480)
my_canvas.pack(fill="both", expand=True)
my_canvas.create_image(0, 0, image=bg, anchor="nw")

speed_stack = SpeedTestStack()

title_label = tk.Label(root, text="ÉL Kecepatan Internet", font=("Arial", 16, "bold"), bg="black", fg="white")
my_canvas.create_window(426, 50, window=title_label) 

connection_var = tk.IntVar(value=0)  

lan_checkbox = tk.Checkbutton(
    root, text="LAN", variable=connection_var, onvalue=1, offvalue=0, command=update_start_button, bg="black", fg="grey"
)
wifi_checkbox = tk.Checkbutton(
    root, text="WiFi", variable=connection_var, onvalue=2, offvalue=0, command=update_start_button, bg="black", fg="grey"
)

my_canvas.create_window(352, 400, window=lan_checkbox)
my_canvas.create_window(500, 400, window=wifi_checkbox)

isp_label = tk.Label(root, text="Select your ISP:", bg="black", fg="white")
my_canvas.create_window(300, 350, window=isp_label)

isp_var = tk.StringVar(value="")
isp_dropdown = ttk.Combobox(
    root, textvariable=isp_var, state="readonly",
    values=["Indihome", "First Media", "MNC Play", "Biznet", "My Republic", "CBN", "Hotspot"]
)
isp_dropdown.bind("<<ComboboxSelected>>", lambda e: update_start_button())
my_canvas.create_window(450, 350, window=isp_dropdown)

start_button = tk.Button(root, text="Start", state="disabled", command=open_speed_test_window, bg="light grey")
my_canvas.create_window(426, 450, window=start_button)

def show_history():
    global speed_test_window
    if speed_stack.is_empty():
        messagebox.showinfo("History", "No history available.")
        return

    if speed_test_window is not None:
        speed_test_window.withdraw()

    history_window = tk.Toplevel()
    history_window.title("Speed Test History")
    history_window.geometry("600x500")
    history_window.configure(bg="black")

    frame = tk.Frame(history_window, bg="light grey")
    frame.pack(fill="both", expand=True)

    history_text = tk.Text(frame, wrap="word", height=15, bg="black", fg="white", font=("Calibri", 12))
    history_text.pack(side="top", fill="both", expand=True, padx=5, pady=5)

    back_button_frame = tk.Frame(frame, bg="light grey")
    back_button_frame.pack(side="bottom", fill="x", pady=5)

    def back_to_speed_test():
        history_window.destroy()  
        if speed_test_window is not None:
            speed_test_window.deiconify()  

    back_button = tk.Button(
        back_button_frame,
        text="Back",
        command=back_to_speed_test,
        bg="grey",
        fg="white",
        font=("Calibri", 14),
    )
    back_button.pack(pady=5)

    history = speed_stack.get_all()
    for record in history:          #Perulangan / Modul 3
        history_text.insert(
            "end",
            f"Date and Time: {record['timestamp']}\n"
            f"ISP: {record['isp']}\n"
            f"Connection: {record['connection']}\n"
            f"Ping: {record['ping']} ms\n"
            f"Download: {record['download']}\n"
            f"Upload: {record['upload']}\n\n",
        )
    history_text.config(state="disabled") 

root.mainloop()
