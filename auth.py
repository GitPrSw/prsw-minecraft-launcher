import socket
import tkinter as tk
from tkinter import ttk
import requests
import json
import time


# All online authentication actions are from https://mojang-api-docs.netlify.app/authentication/msa.html


def authenticate():
    def copylinktoclipboard():
        try:
            # checking for internet connection
            if socket.gethostbyname(socket.gethostname()) == '127.0.0.1':
                raise requests.exceptions.ConnectionError

            # getting the login link
            session = requests.Session()
            request = session.get(
                'https://login.live.com/oauth20_authorize.srf?client_id=000000004C12AE6F&redirect_uri=https://login.live'
                '.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type'
                '=token&locale=en', timeout=1)
            auth_window.clipboard_clear()
            auth_window.clipboard_append(request.text.split('urlPost:\'')[1].split("',")[0])
            link_copy_button['text'] = 'Copied!'
            auth_window.update()
        except requests.exceptions.ConnectionError:
            # Happens when there's no Internet connection.
            output_label['foreground'] = 'red'
            output.set('Error. Please ensure that you are connected to the Internet!')
        except Exception as e:
            # To catch all unknown errors.
            output_label['foreground'] = 'red'
            output.set('Unknown error: ' + str(e))

    def login():
        try:
            # checking for internet connection
            if socket.gethostbyname(socket.gethostname()) == '127.0.0.1':
                raise requests.exceptions.ConnectionError

            # Extracting Microsoft token
            redirectlink = auth_window.clipboard_get()
            confirm_button['text'] = 'Pasted!'
            auth_window.update()
            microsoft_token = redirectlink.split('access_token=')[1].split('&token_type=')[0]

            # Logging into Xbox Live (XBL)
            xbl_payload = {"Properties": {"AuthMethod": "RPS", "SiteName": "user.auth.xboxlive.com",
                                          "RpsTicket": microsoft_token},
                           "RelyingParty": "http://auth.xboxlive.com", "TokenType": "JWT"}
            xbl_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            xbl_request = requests.post('https://user.auth.xboxlive.com/user/authenticate', headers=xbl_headers,
                                        json=xbl_payload)
            xbl_response = xbl_request.json()

            # Getting an XSTS token
            xsts_payload = {"Properties": {"SandboxId": "RETAIL", "UserTokens": [xbl_response['Token']]},
                            "RelyingParty": "rp://api.minecraftservices.com/", "TokenType": "JWT"}
            xsts_request = requests.post('https://xsts.auth.xboxlive.com/xsts/authorize', headers=xbl_headers,
                                         json=xsts_payload)
            xsts_response = xsts_request.json()

            # Getting the Minecraft bearer token
            mojang_payload = {'identityToken': 'XBL3.0 x=' + xsts_response['DisplayClaims']['xui'][0]['uhs'] + ';' +
                                               xsts_response['Token'], 'ensureLegacyEnabled': True}
            mojang_headers = {'Content-Type': 'application/json'}
            mojang_request = requests.post('https://api.minecraftservices.com/authentication/login_with_xbox',
                                           headers=mojang_headers, json=mojang_payload)
            mojang_response = mojang_request.json()
            expires_in = mojang_response['expires_in'] + time.time()

            # Getting the Minecraft username and UUID
            uuid_headers = {'Authorization': 'Bearer ' + mojang_response['access_token']}
            uuid_request = requests.get('https://api.minecraftservices.com/minecraft/profile', headers=uuid_headers)
            uuid_response = uuid_request.json()

            # Saving the login information to accounts.json
            accountfile = open('accounts.json', mode='r')
            accountdict = json.loads(''.join(accountfile.readlines()))
            accountfile.close()
            account_details[uuid_response['id']] = {'name': uuid_response['name'],
                                                    'access_token': mojang_response['access_token'],
                                                    'expires_in': expires_in}
            accountdict[uuid_response['id']] = account_details[uuid_response['id']]
            accountfile = open('accounts.json', mode='w')
            accountfile.write(json.dumps(accountdict))
            accountfile.close()

            # Finishing up
            output_label['foreground'] = 'green'
            output.set('Success! Closing.')
            auth_window.update()
            time.sleep(5)
            auth_window.destroy()

        except IndexError:
            # Happens when the link syntax is wrong.
            output_label['foreground'] = 'red'
            output.set('Error. Please ensure you have copied the redirected link before pressing the Paste button!')
        except requests.exceptions.ConnectionError:
            # Happens when there's no Internet connection.
            output_label['foreground'] = 'red'
            output.set('Error. Please ensure that you are connected to the Internet!')
        except Exception as e:
            # To catch all unknown errors.
            output_label['foreground'] = 'red'
            output.set('Unknown error: ' + str(e))

    # Setting up authentication window.
    auth_window = tk.Tk()
    auth_window.geometry('400x400')
    auth_window.title('Log in with a Microsoft account.')
    auth_window.attributes('-toolwindow', True)
    auth_window.attributes('-topmost', True)

    # Setting up grid
    auth_window.columnconfigure(0, weight=1)
    auth_window.rowconfigure(0, weight=1)
    content = tk.Frame(auth_window)
    content.columnconfigure(0, weight=1)
    content.rowconfigure(0, weight=2)
    content.rowconfigure(1, weight=1)
    content.rowconfigure(2, weight=1)
    content.rowconfigure(3, weight=1)
    content.rowconfigure(4, weight=1)
    content.rowconfigure(5, weight=1)
    content.grid(row=0, column=0)

    # Top text
    top_label = ttk.Label(content, text='To log in with your Microsoft account, please open this link in your browser.',
                          wraplength=300)
    top_label.grid(row=0, column=0, sticky=tk.NSEW)

    # link copy button
    link_copy_button = ttk.Button(content, text='Click to copy the link to your clipboard.', command=copylinktoclipboard)
    link_copy_button.grid(row=2, column=0, sticky=tk.NSEW)

    # link paste button
    link_input_label = ttk.Label(content, text='Copy the link you were redirected to and click here.', wraplength=300)
    link_input_label.grid(row=3, column=0, sticky=tk.NSEW)
    confirm_button = ttk.Button(content, text='Paste the redirected link.', command=login)
    confirm_button.grid(row=4, column=0, sticky=tk.NSEW)

    # Output label
    output = tk.StringVar()
    output_label = ttk.Label(content, textvariable=output, wraplength=300)
    output_label.grid(row=5, column=0, sticky=tk.NSEW)

    # Start GUI
    account_details = {}
    auth_window.update()

    # Finish
    return account_details


if __name__ == '__main__':
    authenticate()
