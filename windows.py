import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import instance
from time import strftime, gmtime


def load_main_window():
    main_window = tk.Tk()
    # setting up main window
    main_window.geometry('600x600')
    main_window.title('NPH Launcher')
    main_window.minsize(300, 200)

    # setting up grid
    content = tk.Frame(main_window)
    content.grid(row=0, column=0)
    main_window.rowconfigure(0, weight=1)
    main_window.columnconfigure(0, weight=1)
    content.rowconfigure(0, weight=3)
    content.rowconfigure(1, weight=1)
    content.rowconfigure(2, weight=1)
    content.rowconfigure(3, weight=1)
    content.columnconfigure(0)
    content.columnconfigure(1)
    content.columnconfigure(2)
    content.columnconfigure(3)

    # last played instance launch button
    last_played = instance.last_played_instance()
    if type(last_played) != bool:
        lastplayed_button = ttk.Button(content, text='Run last played instance: ' + list(last_played)[0],
                                       command=instance.launch_instance(last_played))
    else:
        lastplayed_button = ttk.Button(content, text='Last played instance not found.', state='disabled')

    lastplayed_button.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=4)

    # instance selection menu
    instance_menu_list_text = ttk.Label(content, anchor=tk.CENTER, text='Choose another instance...')
    instance_menu_list_text.grid(column=0, row=1, sticky=tk.NSEW, padx=5, pady=5, columnspan=3)
    instance_menu_list = ttk.OptionMenu(content, tk.StringVar(main_window, 'Select:'))
    instance_menu_list.grid(column=3, row=1, sticky=tk.NSEW, padx=5, pady=5)

    # instance edit menu button
    instance_edit_button = ttk.Button(content, text='Edit instances', command=lambda: load_instance_window())
    instance_edit_button.grid(column=0, row=2, sticky=tk.NSEW, padx=5, pady=5, columnspan=2)

    # Network preferences edit menu button
    network_edit_button = ttk.Button(content, text='Edit network preferences')
    network_edit_button.grid(column=2, row=2, sticky=tk.NSEW, padx=5, pady=5, columnspan=2)

    # Exit button
    exit_button = ttk.Button(content, text='Quit', command=main_window.quit)
    exit_button.grid(column=0, row=3, sticky=tk.NSEW, padx=5, pady=5, columnspan=4)

    main_window.mainloop()


def load_instance_window():
    # Setting up the instance window
    instance_window = tk.Tk()
    instance_window.geometry('400x400')
    instance_window.title('Instance editor')

    # Setting up grid
    content = ttk.Frame(instance_window)
    instance_window.rowconfigure(0, weight=1)
    instance_window.columnconfigure(0, weight=1)
    content.grid(row=0, column=0)
    content.rowconfigure(0)
    content.rowconfigure(1)
    content.columnconfigure(0, weight=3)
    content.columnconfigure(1, weight=1)

    # Upper buttons
    new_instance_button = ttk.Button(content, text='New', command=lambda: load_edit_window(isnew=True))
    new_instance_button.grid(row=0, column=1)
    close_button = ttk.Button(content, text='Close', command=lambda: instance_window.quit())
    close_button.grid(row=0, column=0)

    # Other instances list
    instance_list_frame = ttk.Frame(content)
    instance_list_frame.columnconfigure(0, weight=3)
    instance_list_frame.columnconfigure(1, weight=1)
    instance_list_frame.grid(row=1, column=0, columnspan=2)
    instance_dict = instance.load_instances_from_file()
    x = 0
    instancelabels = []
    instancebuttons = []
    for i in instance_dict.keys():
        instance_list_frame.rowconfigure(x)
        instancelabels.append(ttk.Label(instance_list_frame,
                                        text=i + '\nLast played: ' + strftime('%a, %d %b %Y %H:%M:%S',
                                                                              gmtime(instance_dict[i]['last_played']))))
        instancelabels[-1].grid(row=x, column=0, sticky=tk.W)
        instancebuttons.append(ttk.Button(instance_list_frame,
                                          command=lambda: load_edit_window({i: instance_dict[i]}),
                                          text='Edit'))
        instancebuttons[-1].grid(row=x, column=1, sticky=tk.E)
        x += 1


def load_edit_window(loaded_instance={'': {'minmem': 256, 'maxmem': 2048, 'extra_args': ''}}, isnew=False):
    def openfile(title, filetypes=("all files", "*.*")):
        file_open_window = tk.Tk()
        file_open_window.filename = filedialog.askopenfilename(initialdir='C:\\', title=title, filetypes=filetypes)

    def label_and_entry(text, textvariable, row):
        labels.append(ttk.Label(content, text=text))
        labels[-1].grid(row=row, column=0)
        entries.append(ttk.Entry(content, textvariable=textvariable))
        entries[-1].grid(row=row, columnspan=3, column=1)
        entries[-1].insert(0, textvariable.get())

    # Setting up window
    instance_edit_window = tk.Tk()
    instance_edit_window.geometry('400x400')
    if isnew:
        instance_edit_window.title('Create new instance')
    else:
        instance_edit_window.title('Editing instance ' + list(loaded_instance.keys())[0])
    content = ttk.Frame(instance_edit_window)
    instance_edit_window.rowconfigure(0, weight=1)
    instance_edit_window.columnconfigure(0, weight=1)
    content.grid(row=0, column=0)
    content.columnconfigure(0, weight=1)
    content.columnconfigure(1, weight=1)
    content.columnconfigure(2, weight=1)
    content.columnconfigure(3, weight=1)
    content.rowconfigure(0, weight=1)
    content.rowconfigure(1, weight=1)
    content.rowconfigure(2, weight=1)
    content.rowconfigure(3, weight=1)

    # Setting up variables for entry boxes
    name_field_textvar = tk.StringVar(instance_edit_window, list(loaded_instance.keys())[0])
    minmem_field_textvar = tk.StringVar(instance_edit_window, loaded_instance[list(loaded_instance.keys())[0]]['minmem'])
    maxmem_field_textvar = tk.StringVar(instance_edit_window, loaded_instance[list(loaded_instance.keys())[0]]['maxmem'])
    extra_args_field_textvar = tk.StringVar(instance_edit_window, loaded_instance[list(loaded_instance.keys())[0]]['extra_args'])

    # Setting up entry boxes
    labels = []
    entries = []
    label_and_entry('Instance name:', name_field_textvar, 0)
    label_and_entry('Minimum memory:', minmem_field_textvar, 1)
    label_and_entry('Maximum memory:', maxmem_field_textvar, 2)
    label_and_entry('Extra arguments:', extra_args_field_textvar, 3)
