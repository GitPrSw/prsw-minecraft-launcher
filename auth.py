import tkinter as tk
from tkinter import ttk
import subprocess
import requests

def authenticate():

    def login(email: str, password: str):
        accounts_file=open("auth\\accounts.txt", mode='w')
        accounts_file.write(email+':'+password)
        accounts_file.close()
        subprocess.call('auth\\xboxlive-auth.exe', shell=True)


    # Setting up authentication window.
    auth_window = tk.Tk()
    auth_window.geometry('400x400')
    auth_window.title('Log in with a Microsoft account.')
    auth_window.attributes('-toolwindow', True)

    # Setting up grid
    auth_window.columnconfigure(0, weight=1)
    auth_window.columnconfigure(1, weight=3)
    auth_window.rowconfigure(0, weight=2)
    auth_window.rowconfigure(1, weight=1)
    auth_window.rowconfigure(2, weight=1)
    auth_window.rowconfigure(3, weight=1)

    # Top text
    top_label = ttk.Label(text='Log in with your Microsoft account.')
    top_label.grid(row=0, column=0, sticky=tk.NSEW, columnspan=2)

    # e-mail
    email_label = ttk.Label(text='E-mail')
    email_label.grid(row=1, column=0, sticky=tk.E)
    email_input = ttk.Entry(auth_window)
    email_input.grid(row=1, column=1)

    # password
    password_label = ttk.Label(text='Password')
    password_label.grid(row=2, column=0, sticky=tk.E)
    password_input = ttk.Entry(auth_window, show='*')
    password_input.grid(row=2, column=1)

    # send button

    confirm_button = ttk.Button(auth_window, text='Confirm', command=lambda: login(email_input.get(), password_input.get()))
    confirm_button.grid(row=3, column=1, sticky=tk.E)

    auth_window.mainloop()


authenticate()