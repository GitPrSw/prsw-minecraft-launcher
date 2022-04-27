import tkinter as tk
from tkinter import ttk
import subprocess


def load_main_window(instances):
    main_window = tk.Tk()
    # setting up main window
    main_window.geometry('400x400')
    main_window.title('NPH Launcher')
    main_window.minsize(300, 200)

    # setting up grid
    main_window.rowconfigure(0, weight=3)
    main_window.rowconfigure(1, weight=1)
    main_window.rowconfigure(2, weight=1)
    main_window.rowconfigure(3, weight=1)
    main_window.columnconfigure(0)
    main_window.columnconfigure(1)
    main_window.columnconfigure(2)
    main_window.columnconfigure(3)

    # last played instance launch button
    try:
        lastplayed_button = ttk.Button(main_window, text='Run last played instance: ' + instances[0].instance_name,
                                       command=lambda: instances[0].launch())
    except:
        lastplayed_button = ttk.Button(main_window, text='Last played instance not found.', state='disabled')

    lastplayed_button.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=4)

    # instance selection menu
    instance_menu_list_text = ttk.Label(main_window, anchor=tk.CENTER, text='Choose another instance...')
    instance_menu_list_text.grid(column=0, row=1, sticky=tk.NSEW, padx=5, pady=5, columnspan=3)
    instance_menu_list = ttk.OptionMenu(main_window, tk.StringVar(main_window, 'Select:'))
    instance_menu_list.grid(column=3, row=1, sticky=tk.NSEW, padx=5, pady=5)

    # instance edit menu button
    instance_edit_button = ttk.Button(main_window, text='Edit instances')
    instance_edit_button.grid(column=0, row=2, sticky=tk.NSEW, padx=5, pady=5, columnspan=2)

    # Network preferences edit menu button
    network_edit_button = ttk.Button(main_window, text='Edit network preferences')
    network_edit_button.grid(column=2, row=2, sticky=tk.NSEW, padx=5, pady=5, columnspan=2)

    # Exit button
    exit_button = ttk.Button(main_window, text='Quit', command=lambda: main_window.quit())
    exit_button.grid(column=0, row=3, sticky=tk.NSEW, padx=5, pady=5, columnspan=4)

    main_window.mainloop()
