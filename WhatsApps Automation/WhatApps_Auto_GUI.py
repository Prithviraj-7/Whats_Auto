
   #before you start building first make one twilio account  


import tkinter as tk
from twilio.rest import Client
from datetime import datetime
import time
import threading
from PIL import Image, ImageTk

# Twilio credentials
account_sid = "xyz"        #Must hide from others, make twilio account copy this from dashborad
auth_token = "xyz"           #Must hide from others, make twilio account copy this from dashborad
client = Client(account_sid, auth_token)

# Function to send message
def send_whatsapp_message(recipient_number, message_body):
    try:
        message = client.messages.create(
            from_="whatsapp:xyz",
            body=message_body,
            to=f"whatsapp:{recipient_number}"
        )
        print(f"Message sent to {recipient_number}. SID: {message.sid}")
    except Exception as e:
        print("Error:", e)

# Function to schedule message
def schedule_message():
    name = name_entry.get()
    numbers = number_entry.get()
    message = message_entry.get()
    date = date_entry.get()
    time_ = time_entry.get()

    recipient_numbers = [num.strip() for num in numbers.split(",")]

    try:
        schedule_time = datetime.strptime(f"{date} {time_}", "%Y-%m-%d %H:%M")
        now = datetime.now()
        delay = (schedule_time - now).total_seconds()

        if delay <= 0:
            result_label.config(text="⛔ Time is in the past! Enter a future time.")
            return

        result_label.config(text=f"⏳ Message will be sent at {schedule_time}")

        def delayed_send():
            time.sleep(delay)
            for number in recipient_numbers:
                send_whatsapp_message(number, message)
            result_label.config(text="✅ Message sent successfully!")

        threading.Thread(target=delayed_send).start()

    except ValueError:
        result_label.config(text="❌ Invalid date or time format!")

# GUI setup
root = tk.Tk()
root.title("WhatsApp Message Scheduler")
root.geometry("500x600")
root.iconbitmap("Icon-For-wa.ico") 

# Load and place background image
bg_image = Image.open("Bg.whatsapp.jpg")
bg_image = bg_image.resize((1500, 1600), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

background_label = tk.Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Widgets on top of background
tk.Label(root, text="Enter your Name:", font=("Arial", 15), bg="lightblue").pack()
name_entry = tk.Entry(root, width=29)
name_entry.pack(pady=15)

tk.Label(root, text="Enter WhatsApp Numbers (With country code):", font=("Arial", 12), bg="lightblue").pack()
number_entry = tk.Entry(root, width=29)
number_entry.pack(pady=15)

tk.Label(root, text="Enter Message:", font=("Arial", 15), bg="lightblue").pack()
message_entry = tk.Entry(root, width=29)
message_entry.pack(pady=15)

tk.Label(root, text="Enter Date (YYYY-MM-DD):", font=("Arial", 15), bg="lightblue").pack()
date_entry = tk.Entry(root, width=29)
date_entry.pack(pady=15)

tk.Label(root, text="Enter Time (HH:MM 24hr):", font=("Arial", 15), bg="lightblue").pack()
time_entry = tk.Entry(root, width=29)
time_entry.pack(pady=15)

tk.Button(root, text="Schedule Message", font=("Arial", 30), bg="lightgreen", command=schedule_message).pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12), bg="white", fg="red")
result_label.pack(pady=15)

root.mainloop()