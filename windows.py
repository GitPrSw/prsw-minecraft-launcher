import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import auth
import instance
from time import strftime, gmtime, time
import json


class VerticalScrolledFrame(ttk.Frame):
    # A pure Tkinter scrollable frame that actually works!
    # * Use the 'interior' attribute to place widgets inside the scrollable frame.
    # * Construct and pack/place/grid normally.
    # * This frame only allows vertical scrolling.
    # From https://web.archive.org/web/20170514022131id_/http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = ttk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=tk.NW)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion=canvas.bbox(f'0 0 {size} {size}'))
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


def load_main_window():
    # setting up main window
    main_window = tk.Tk()
    main_window.geometry('600x600')
    main_window.title('NPH Launcher')
    main_window.minsize(300, 200)

    # setting up grid
    content = tk.Frame(main_window)
    content.grid(row=0, column=0)
    main_window.rowconfigure(0, weight=1)
    main_window.columnconfigure(0, weight=1)
    content.rowconfigure(0, weight=1)
    content.rowconfigure(1, weight=3)
    content.rowconfigure(2, weight=1)
    content.rowconfigure(3, weight=1)
    content.rowconfigure(4, weight=1)
    content.columnconfigure(0)
    content.columnconfigure(1)
    content.columnconfigure(2)
    content.columnconfigure(3)

    # Account select
    account_select_label = ttk.Label(content, text='Select your account:')
    account_select_label.grid(row=0, column=0, columnspan=3)
    selected_account = tk.StringVar(main_window)
    accounts_dict = instance.load_from_file('accounts.json')
    account_list = []
    if len(accounts_dict) > 0:
        for i in accounts_dict.keys():
            if time() < accounts_dict[i]['expires_in']:
                account_list.append(accounts_dict[i]['name'])
    if len(account_list) > 0:
        account_select_list = ttk.OptionMenu(content, selected_account, *account_list)
        account_select_list.grid(row=0, column=3)
    else:
        auth.authenticate()

    # last played instance launch button
    last_played = instance.last_played_instance()

    def launch_minecraft(current_instance=last_played):
        for i in accounts_dict.keys():
            if accounts_dict[i]['name'] == selected_account.get():
                account = {i: accounts_dict[i]}
                break
        instance.launch_instance(current_instance, account)
    if last_played is not None:
        lastplayed_button = ttk.Button(content, text='Run last played instance: ' + list(last_played)[0],
                                       command=launch_minecraft)
    else:
        lastplayed_button = ttk.Button(content, text='Last played instance not found.', state='disabled')

    def update_play_button(choice):
        lastplayed_button['text'] = 'Run instance: ' + choice
        lastplayed_button['state'] = 'normal'
        for i in instance_data.keys():
            if i == choice:
                choice_dict = {i: instance_data[i]}
                break
        lastplayed_button['command'] = lambda: launch_minecraft(choice_dict)

    lastplayed_button.grid(column=0, row=1, sticky=tk.NSEW, padx=5, pady=5, columnspan=4)

    # instance selection menu
    instance_menu_list_text = ttk.Label(content, anchor=tk.CENTER, text='Choose another instance...')
    instance_menu_list_text.grid(column=0, row=2, sticky=tk.NSEW, padx=5, pady=5, columnspan=3)
    instance_data = instance.load_from_file('instancedata.json')
    instances_list = list(instance_data.keys())
    selected_instance = tk.StringVar(main_window)
    instance_menu_list = ttk.OptionMenu(content, selected_instance, *instances_list, command=update_play_button)
    instance_menu_list.grid(column=3, row=2, sticky=tk.NSEW, padx=5, pady=5)

    # instance edit menu button
    instance_edit_button = ttk.Button(content, text='Edit instances', command=load_instance_window)
    instance_edit_button.grid(column=0, row=3, sticky=tk.NSEW, padx=5, pady=5, columnspan=4)

    # Network preferences edit menu button
    # network_edit_button = ttk.Button(content, text='Edit network preferences')
    # network_edit_button.grid(column=2, row=3, sticky=tk.NSEW, padx=5, pady=5, columnspan=2)

    # Exit button
    exit_button = ttk.Button(content, text='Quit', command=main_window.quit)
    exit_button.grid(column=0, row=4, sticky=tk.NSEW, padx=5, pady=5, columnspan=4)

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
    content.rowconfigure(0, weight=1)
    content.rowconfigure(1, weight=1)
    content.rowconfigure(2, weight=1)
    content.columnconfigure(0, weight=1)

    # Upper buttons
    upper_buttons_frame = ttk.Frame(content)
    upper_buttons_frame.grid(row=0, column=0)
    upper_buttons_frame.columnconfigure(0, weight=1)
    upper_buttons_frame.columnconfigure(1, weight=1)
    upper_buttons_frame.rowconfigure(0, weight=1)
    new_instance_button = ttk.Button(upper_buttons_frame, text='New', command=lambda: load_edit_window(isnew=True))
    new_instance_button.grid(row=0, column=1)
    close_button = ttk.Button(upper_buttons_frame, text='Close', command=instance_window.destroy)
    close_button.grid(row=0, column=0)

    # Other instances list
    instance_list_frame = VerticalScrolledFrame(content)
    instance_list_frame.columnconfigure(0, weight=9)
    instance_list_frame.columnconfigure(1, weight=3)
    instance_list_frame.columnconfigure(2, weight=1)
    instance_list_frame.grid(row=1, column=0, rowspan=2)
    instance_dict = instance.load_from_file()
    x = 0
    instancelabels = []
    instancebuttons = []
    for i in instance_dict.keys():
        instance_list_frame.rowconfigure(x)
        if instance_dict[i]['last_played'] != 0:
            last_played_text = i + '\nLast played: ' + strftime('%a, %d %b %Y %H:%M:%S', gmtime(instance_dict[i]['last_played']))
        else:
            last_played_text = i + '\nLast played: Never'
        instancelabels.append(ttk.Label(instance_list_frame.interior, text=last_played_text))
        instancelabels[-1].grid(row=x, column=0, sticky=tk.W)
        instancebuttons.append(ttk.Button(instance_list_frame.interior,
                                          command=lambda: load_edit_window({i: instance_dict[i]}),
                                          text='Edit'))
        instancebuttons[-1].grid(row=x, column=1, sticky=tk.E)
        x += 1
    scrollbar_warning_label = ttk.Label(content, text='The scrollbar only works with buttons. This is a known issue.')
    scrollbar_warning_label.grid(row=3, column=0)


def load_edit_window(loaded_instance={'': {'minmem': 256, 'maxmem': 2048, 'extra_args': '', 'java_path': 'java', 'version': '1.18.2'}},
                     isnew=False):
    def openfile(title, textvariable):
        file_open_window = tk.Tk()
        file_open_window.filename = filedialog.askopenfilename(initialdir='C:\\', title=title)
        textvariable.set(file_open_window.filename)

    def label_and_entry(text, textvariable, row):
        labels.append(ttk.Label(content, text=text))
        labels[-1].grid(row=row, column=0)
        entries.append(ttk.Entry(content, textvariable=textvariable))
        entries[-1].grid(row=row, columnspan=3, column=1)

    # Setting up window
    instance_name = list(loaded_instance.keys())[0]
    instance_edit_window = tk.Tk()
    instance_edit_window.geometry('400x400')
    if isnew:
        instance_edit_window.title('Create new instance')
    else:
        instance_edit_window.title('Editing instance ' + instance_name)
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
    content.rowconfigure(4, weight=1)
    content.rowconfigure(5, weight=1)
    content.rowconfigure(6, weight=1)
    content.rowconfigure(7, weight=1)

    # Setting up variables for entry boxes
    name_field_textvar = tk.StringVar(instance_edit_window, instance_name)
    minmem_field_textvar = tk.StringVar(instance_edit_window, loaded_instance[instance_name]['minmem'])
    maxmem_field_textvar = tk.StringVar(instance_edit_window, loaded_instance[instance_name]['maxmem'])
    extra_args_field_textvar = tk.StringVar(instance_edit_window, loaded_instance[instance_name]['extra_args'])

    # Setting up version select list
    selected_version = tk.StringVar(instance_edit_window, loaded_instance[instance_name]['version'])
    version_dict = instance.load_from_file('minecraft_assets\\version_manifest.json')
    releases_variable = tk.IntVar(instance_edit_window, 1)
    snapshots_variable = tk.IntVar(instance_edit_window, 0)
    old_alpha_variable = tk.IntVar(instance_edit_window, 0)
    old_beta_variable = tk.IntVar(instance_edit_window, 0)
    version_list = []
    for i in version_dict['versions']:
        if i['type'] == 'release' and bool(releases_variable.get()):
            version_list.append(i['id'])
    version_select_list = ttk.Combobox(content, textvariable=selected_version, values=version_list)
    version_select_list.grid(row=1, column=2)

    def reload_version_list():
        new_version_list = []
        for i in version_dict['versions']:
            if (i['type'] == 'release' and bool(releases_variable.get())) or (i['type'] == 'snapshot' and bool(snapshots_variable.get())) or (i['type'] == 'old_beta' and bool(old_beta_variable.get())) or (i['type'] == 'old_alpha' and bool(old_alpha_variable.get())):
                new_version_list.append(i['id'])
        version_select_list.config(values=new_version_list)

    releases_checkbox = ttk.Checkbutton(content, command=reload_version_list,
                                        variable=releases_variable, text='Releases')
    releases_checkbox.grid(row=0, column=0)
    snapshots_checkbox = ttk.Checkbutton(content, command=reload_version_list,
                                         variable=snapshots_variable, text='Snapshots')
    snapshots_checkbox.grid(row=0, column=1)
    old_beta_checkbox = ttk.Checkbutton(content, command=reload_version_list,
                                        variable=old_beta_variable, text='Beta')
    old_beta_checkbox.grid(row=0, column=2)
    old_alpha_checkbox = ttk.Checkbutton(content, command=reload_version_list,
                                         variable=old_alpha_variable, text='Alpha')
    old_alpha_checkbox.grid(row=0, column=3)
    version_select_label = ttk.Label(content, text='Game version:')
    version_select_label.grid(row=1, column=0)

    # Setting up entry boxes
    labels = []
    entries = []
    label_and_entry('Instance name:', name_field_textvar, 2)
    label_and_entry('Minimum memory:', minmem_field_textvar, 3)
    label_and_entry('Maximum memory:', maxmem_field_textvar, 4)
    label_and_entry('Extra arguments:', extra_args_field_textvar, 5)

    # Setting up file select box
    java_path_textvar = tk.StringVar(instance_edit_window, loaded_instance[instance_name]['java_path'])
    java_path_label = ttk.Label(content, text='Java path:')
    java_path_label.grid(row=6, column=0)
    java_path_button = ttk.Button(content, textvariable=java_path_textvar,
                                  command=lambda: openfile('Select Java path', java_path_textvar))
    java_path_button.grid(row=6, column=1, columnspan=3)

    # Cancel button

    cancel_button = ttk.Button(content, command=instance_edit_window.destroy, text='Cancel')
    cancel_button.grid(row=7, column=0, columnspan=2)

    # Save button
    def save_instance(install=False):
        instances_dict = instance.load_from_file()
        instance_dict = {'minmem': int(minmem_field_textvar.get()),
                         'maxmem': int(maxmem_field_textvar.get()),
                         'extra_args': extra_args_field_textvar.get(),
                         'java_path': java_path_textvar.get(),
                         'last_played': 0,
                         'version': selected_version.get()}
        instances_dict[name_field_textvar.get()] = instance_dict
        with open('instancedata.json', mode='w') as instances_file:
            instances_file.write(json.dumps(instances_dict))
        instance_edit_window.destroy()
        if install:
            instance.install_instance({name_field_textvar.get(): instance_dict})

    if isnew:
        save_button = ttk.Button(content, command=lambda: save_instance(True), text='Save and install')
        save_button.grid(row=7, column=2, columnspan=2)
    else:
        save_button = ttk.Button(content, command=save_instance, text='Save')
        save_button.grid(row=7, column=2)
        reinstall_button = ttk.Button(content, command=lambda: save_instance(True), text='Reinstall')
        reinstall_button.grid(row=7, column=3)
