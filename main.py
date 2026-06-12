import tkinter as tk
from tkinter import filedialog
import os
from crypto_utils import *
from sender import *
from receiver import *
from tkinter import simpledialog
import threading
from room_manager import generate_room_code
from PIL import Image, ImageTk
from network_utils import get_local_ip
from qr_utils import (
    generate_qr,
    read_qr
)

BG_COLOR = "#0A0A0A"
FG_COLOR = "#00FF88"
BUTTON_BG = "#111111"
BUTTON_ACTIVE = "#00CC66"


paired_ip = None


splash = tk.Tk()


splash.title("SALVUS")

width = 500
height = 350

screen_width = splash.winfo_screenwidth()
screen_height = splash.winfo_screenheight()

x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)

splash.geometry(
    f"{width}x{height}+{x}+{y}"
)


splash.configure(bg="#0A0A0A")

splash.overrideredirect(True)


logo = tk.PhotoImage(
    file="assets/salvus.png"
)

logo_label = tk.Label(
    splash,
    image=logo,
    bg="#0A0A0A"
)

logo_label.pack(
    expand=True
)

title_label = tk.Label(
    splash,
    text="SALVUS",
    font=("Montserrat", 24, "bold"),
    fg="#00FF88",
    bg="#0A0A0A"
)

title_label.pack()

subtitle_label = tk.Label(
    splash,
    text="Encrypted Peer-to-Peer Transfer",
    font=("Montserrat", 10),
    fg="#00CC66",
    bg="#0A0A0A"
)

subtitle_label.pack()


loading_label = tk.Label(
    splash,
    text="Loading",
    font=("Consolas", 10),
    fg=FG_COLOR,
    bg="#0A0A0A"
)

loading_label.pack(
    side="bottom",
    pady=20
)


def animate_loading(count=0):

    dots = "." * (count % 4)

    loading_label.config(
        text=f"Loading{dots}"
    )

    splash.after(
        500,
        animate_loading,
        count + 1
    )


def start_app():

    splash.destroy()

    root.deiconify()


root = tk.Tk()
root.withdraw()



root.configure(bg=BG_COLOR)


header = tk.Label(
    root,
    text="SALVUS",
    font=("Chesna grotesk", 30, "bold"),
    bg=BG_COLOR,
    fg=FG_COLOR
)
header.pack(pady=15)

subtitle = tk.Label(
    root,
    text="Encrypted Peer-to-Peer File Transfer",
    font=("Montserrat", 9),
    bg=BG_COLOR,
    fg="#00CC66"
)

subtitle.pack()


separator = tk.Frame(
    root,
    bg=FG_COLOR,
    height=1,
    width=500
)

separator.pack(
    pady=15
)

ip_label = tk.Label(
    root,
    text=f"Your IP: {get_local_ip()}",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=("Montserrat", 10)
)


ip_label.pack(pady=5)

root.title(
    "SALVUS - Secure File Transfer"
)
root.geometry("1280x720")
root.resizable(False, False)

room_label = tk.Label(
    root,
    text="Room Code",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=("Montserrat", 11, "bold")
)


action_frame = tk.Frame(
    root,
    bg=BG_COLOR
)
action_frame.pack(pady=15)

room_label.pack(pady=5)

room_entry = tk.Entry(
    root,
    width=15,
    bg="#111111",
    fg=FG_COLOR,
    insertbackground=FG_COLOR,
    justify="center",
    font=("Consolas", 18, "bold"),
    relief="flat",
    bd=0
)


room_entry.pack()

room_entry.insert(
    0,
    generate_room_code()
)

selected_file = ""


def show_qr():

    ip = get_local_ip()
    room = room_entry.get()

    generate_qr(ip, room)

    qr_window = tk.Toplevel(root)
    qr_window.configure(
        bg=BG_COLOR
    )
    qr_window.title("Pairing QR")

    img = Image.open("pairing_qr.png")

    photo = ImageTk.PhotoImage(img)

    label = tk.Label(
        qr_window,
        image=photo,
        bg=BG_COLOR
    )
    label.image = photo
    label.pack(padx=10, pady=10)

def scan_qr():

    global paired_ip

    qr_path = filedialog.askopenfilename(
        filetypes=[
            ("PNG Files", "*.png")
        ]
    )

    if not qr_path:
        return

    data = read_qr(qr_path)

    if not data:

        status_label.config(
            text="Invalid QR"
        )

        return

    paired_ip = data["ip"]

    room_entry.delete(
        0,
        tk.END
    )

    room_entry.insert(
        0,
        data["room"]
    )

    status_label.config(
        text="QR Paired"
    )


room_button_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

room_button_frame.pack(
    pady=10
)


scan_button = tk.Button(
    room_button_frame,
    text="Scan QR",
    command=scan_qr,
    bg=BUTTON_BG,
    fg=FG_COLOR,
    activebackground=BUTTON_ACTIVE,
    activeforeground="black",
    relief="flat",
    width=14
)

scan_button.pack(
    side=tk.LEFT,
    padx=5
)


def choose_file():
    global selected_file

    selected_file = filedialog.askopenfilename()

    if selected_file:
        file_label.config(
            text=os.path.basename(selected_file)
        )

file_title = tk.Label(
    root,
    text="Selected File",
    font=("Montserrat", 11, "bold"),
    bg=BG_COLOR,
    fg=FG_COLOR,
)

file_title.pack(pady=(15, 0))


file_label = tk.Label(
    root,
    text="No file selected",
    font=("Montserrat", 10),
    wraplength=500,
    bg=BG_COLOR,
    fg=FG_COLOR,
)

file_label.pack(pady=10)

select_button = tk.Button(
    root,
    text="Select File",
    command=choose_file,
    bg=BUTTON_BG,
    fg=FG_COLOR,
    activebackground=BUTTON_ACTIVE,
    activeforeground="black",
    relief="flat"
)

select_button.pack()


log_title = tk.Label(
    root,
    text="Activity Log",
    font=("Montserrat", 11, "bold"),
    bg=BG_COLOR,
    fg=FG_COLOR
)

log_title.pack(
    pady=(20, 5)
)

log_box = tk.Text(
    root,
    height=6,
    width=60,
    bg="#111111",
    fg=FG_COLOR,
    insertbackground=FG_COLOR,
    relief="flat"
)

log_box.pack()


def log(message):

    log_box.insert(
        tk.END,
        f"[+] {message}\n"
    )

    log_box.see(tk.END)





status_label = tk.Label(
    root,
    text="Status: Ready",
    bg="#111111",
    fg=FG_COLOR,
    anchor="w",
    relief="flat"
)

status_label.pack(
    fill="x",
    side="bottom"
)


def send_file_worker():

    if not selected_file:
        status_label.config(
            text="Select a file first"
        )
        return

    room_code = room_entry.get()

    if not room_code:
        status_label.config(
            text="Enter room code"
        )
        return

    try:

        status_label.config(
            text="Encrypting..."
        )

        key = room_code_to_key(
            room_code
        )

        encrypted_data = encrypt_file(
            selected_file,
            key
        )

        status_label.config(
            text="Waiting for receiver..."
        )

        start_sender(
            selected_file,
            encrypted_data
        )

        status_label.config(
            text="Transfer Complete"
        )

    except Exception as e:

        status_label.config(
            text=f"Error: {e}"
        )
def send_file():

    thread = threading.Thread(
        target=send_file_worker
    )

    thread.start()

send_button = tk.Button(
    action_frame,
    text="Send",
    width=12,
    command=send_file,
    bg=BUTTON_BG,
    fg=FG_COLOR,
    activebackground=BUTTON_ACTIVE,
    activeforeground="black",
    relief="flat"
)


send_button.pack(
    side=tk.LEFT,
    padx=5
)
def new_room_code():

    room_entry.delete(
        0,
        tk.END
    )

    room_entry.insert(
        0,
        generate_room_code()
    )


new_room_button = tk.Button(
    room_button_frame,
    text="New Room Code",
    command=new_room_code,
    bg=BUTTON_BG,
    fg=FG_COLOR,
    activebackground=BUTTON_ACTIVE,
    activeforeground="black",
    relief="flat",
    width=14
)

new_room_button.pack(
    side=tk.LEFT,
    padx=5
)



qr_button = tk.Button(
    room_button_frame,
    text="Show QR",
    command=show_qr,
    bg=BUTTON_BG,
    fg=FG_COLOR,
    activebackground=BUTTON_ACTIVE,
    activeforeground="black",
    relief="flat",
    width=14
)


qr_button.pack(
    side=tk.LEFT,
    padx=5
)


def receive_file_worker():

    room_code = room_entry.get()

    if not room_code:
        status_label.config(
            text="Enter room code"
        )
        return

    try:

        if not paired_ip:

            status_label.config(
                text="Scan QR First"
            )

            return

        sender_ip = paired_ip
        if not sender_ip:
            return

        status_label.config(
            text="Receiving..."
        )

        filename, encrypted_data = receive_file(
            sender_ip
        )

        key = room_code_to_key(
            room_code
        )

        decrypted = decrypt_data(
            encrypted_data,
            key
        )

        os.makedirs(
           "received_files",
            exist_ok=True
        )

        save_path = os.path.join(
            "received_files",
            filename
        )
        with open(
            save_path,
            "wb"
        ) as file:

            file.write(
                decrypted
            )

        status_label.config(
            text=f"Received: {filename}"
        )
    except Exception as e:

        status_label.config(
            text=f"Error: {e}"
        )


def receive_file_gui():

    thread = threading.Thread(
        target=receive_file_worker
    )

    thread.start()



receive_button = tk.Button(
    action_frame,
    text="Receive",
    width=12,
    command=receive_file_gui,
    bg=BUTTON_BG,
    fg=FG_COLOR,
    activebackground=BUTTON_ACTIVE,
    activeforeground="black",
    relief="flat"
)

receive_button.pack(
    side=tk.LEFT,
    padx=5
)

animate_loading()

splash.after(
    2500,
    start_app
)


splash.mainloop()