import windows
import requests
import json

# Updating version_manifest.json
version_manifest_update = requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json')
version_manifest = version_manifest_update.json()
version_manifest_file = open('minecraft_assets\\version_manifest.json', mode='w')
version_manifest_file.write(json.dumps(version_manifest))
version_manifest_file.close()

# Rendering main window
windows.load_main_window()

