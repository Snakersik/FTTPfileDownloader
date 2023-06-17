from tkinter import messagebox
from ftplib import FTP
from threading import Thread
import json
from tkinter import filedialog
import os
import tkinter

BLUE = "#08D9D6"
GRAY = "#252A34"
PINK = "#FF2E63"
GREEN = "#54B435"
LIGHT_GRAY = "#6B728E"
ENTRY_HINT_FONT = ("Courier", 8, 'italic')


def click(event):
    print(clicked.get())



def browse():
    file_path = filedialog.askdirectory()
    local_path.insert(0, file_path)

def save_config():
    profile = profile_name.get()
    ftp_address = ftp_server_address.get()
    username = user_name.get()
    user_password = password.get()
    path_local = local_path.get()
    path_ftp = ftp_path.get()
    host = ftp_host.get()

    if profile == "":
        messagebox.showwarning(title="Empty place", message="Profile name can't be empty")
    else:
        new_profile = {
            profile:{
                "ftp_server": ftp_address,
                "username": username,
                "password": user_password,
                "download_destination": path_local,
                "ftp_path": path_ftp,
                "host": host,
            }
        }

        try:
            with open("data.json", "r") as config_file:
                datafile = json.load(config_file)
        except FileNotFoundError:
            with open("data.json", "w") as config_file:
                json.dump(new_profile, config_file, indent=4)
        else:
            datafile.update(new_profile)
            with open("data.json", "w") as config_file:
                json.dump(datafile, config_file, indent=4)


def threading():
    Thread(target=download).start()


def download():
    status = tkinter.Entry()
    status.config(fg=BLUE, width=20)
    status.grid(column=0, row=8, columnspan=5, sticky=tkinter.W + tkinter.E)
    # Connecting to FTP
    ftp = FTP(ftp_server_address.get())
    ftp.login(user=user_name.get(), passwd=password.get())
    FTP.getwelcome(ftp)

    # declaring local path
    path = local_path.get()

    # Declaring working directories
    os.chdir(path)

    # Changing directory on ftp server
    ftp.cwd(ftp_path.get())

    # list of files in FTP current directory
    fnames = ftp.nlst()

    for i in fnames:
        filename = i
        files = os.listdir(path)
        if i in files:
            status.insert(0, f"{i} already installed")
            pass
        else:
            # Write file in binary mode
            with open(filename, "wb") as file:
                # Command for Downloading the file "RETR filename"
                ftp.retrbinary(f"RETR {filename}", file.write)
            files_updates = os.listdir(path)
            if i in files_updates:
                status.insert(0, f"{i} successful download")
            else:
                status.insert(0, f"{i} download failed")

            if len(fnames) == len(files_updates):
                print("All files downloaded")


windows = tkinter.Tk()
windows.title("FTP downloader")
windows.config(padx=30, pady=30, bg=GRAY)
windows.resizable(False, False)
windows.geometry("320x350")




theme_label = tkinter.Label()
theme_label.config(text="FTP downloader", font=("Courier", 20), bg=GRAY, fg=BLUE)
theme_label.grid(column=1, row=1, columnspan=2)

ftp_server_address = tkinter.Entry(fg=LIGHT_GRAY, font=ENTRY_HINT_FONT, width=25, justify='center')
ftp_server_address.insert(0, "FTP server")
ftp_server_address.grid(column=1, row=3, pady=7)
ftp_server_address.bind("<Button-1>", lambda entry: ftp_server_address.delete(0, tkinter.END))

user_name = tkinter.Entry(fg=LIGHT_GRAY, font=ENTRY_HINT_FONT, justify='center')
user_name.insert(0, "Username")
user_name.grid(column=1, row=4, pady=10, sticky=tkinter.W + tkinter.E)
user_name.bind("<Button-1>", lambda entry: user_name.delete(0, tkinter.END))


password = tkinter.Entry(fg=LIGHT_GRAY, font=ENTRY_HINT_FONT, justify='center')
password.insert(0, "Password")
password.grid(column=1, row=5, pady=7, sticky=tkinter.W + tkinter.E)
password.bind("<Button-1>", lambda entry: password.delete(0, tkinter.END))

local_path = tkinter.Entry(fg=LIGHT_GRAY, font=ENTRY_HINT_FONT, justify='center')
local_path.grid(column=1, row=6, pady=7, sticky=tkinter.W + tkinter.E)
local_path.insert(0, "Destination folder")
local_path.bind("<Button-1>", lambda entry: local_path.delete(0, tkinter.END))

ftp_path = tkinter.Entry(fg=LIGHT_GRAY, font=ENTRY_HINT_FONT,  justify='center')
ftp_path.grid(column=1, row=7, pady=7, sticky=tkinter.W + tkinter.E)
ftp_path.insert(0, "Files location on FTP")
ftp_path.bind("<Button-1>", lambda entry: ftp_path.delete(0, tkinter.END))



profile_name = tkinter.Entry(fg=LIGHT_GRAY, font=ENTRY_HINT_FONT, width=25, justify='center')
profile_name.grid(column=1, row=8, pady=10)
profile_name.insert(0, "Profile name")
profile_name.bind("<Button-1>", lambda entry: profile_name.delete(0, tkinter.END))

ftp_host = tkinter.Entry(fg=LIGHT_GRAY, font=ENTRY_HINT_FONT, width=9, justify='center')
ftp_host.grid(column=2, row=3)
ftp_host.insert(0, "Host")
ftp_host.bind("<Button-1>", lambda entry: ftp_host.delete(0, tkinter.END))


browse_button = tkinter.Button(text="Browse", width=9, command=browse)
browse_button.grid(column=2, row=6, padx=10)


save_button = tkinter.Button(command=save_config, text="Save profile")
save_button.grid(column=2, row=8, padx=10)

download_button = tkinter.Button(command=threading, text="Download!", )
download_button.grid(column=1, row=9, pady=10,sticky=tkinter.W + tkinter.E )


try:
    with open("data.json", "r") as config_file:
        datafile = json.load(config_file)
        clicked = tkinter.StringVar()
except FileNotFoundError:
    profile_list = []
    clicked = tkinter.StringVar()
    clicked.set("Profiles")

else:
    profile_list = [key for key in datafile]
    clicked.set("Profiles")




    profile_selection = tkinter.OptionMenu(windows, clicked, *profile_list)
    profile_selection.config(highlightthickness=0)
    profile_selection.grid(column=1, row=2, sticky=tkinter.W + tkinter.E)
    profile_selection.bind("<Button-1>", click)

select_button = tkinter.Button(width=9, text="Select")
select_button.grid(column=2, row=2)





windows.mainloop()

