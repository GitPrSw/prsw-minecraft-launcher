import windows
import requests
import json
import os

files = ['instancedata.json', 'accounts.json']
for i in files:
    if not os.path.exists(i):
        with open(i, mode='x') as file:
            file.close()

# Updating version_manifest.json
version_manifest_update = requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json')
version_manifest = version_manifest_update.json()
version_manifest_file = open('minecraft_assets\\version_manifest.json', mode='w')
version_manifest_file.write(json.dumps(version_manifest))
version_manifest_file.close()

# Rendering main window
windows.load_main_window()

