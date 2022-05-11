import subprocess
import os
import requests
import json
import tkinter as tk
import platform
import zipfile
import shutil
import asyncio
import time


def last_played_instance():
    instance_dict = load_from_file()
    last_played = None
    last_playedtime = 0
    for i in instance_dict.keys():
        if instance_dict[i]['last_played'] > last_playedtime:
            last_played = {i: instance_dict[i]}
            last_playedtime = instance_dict[i]['last_played']
    return last_played


def load_from_file(filename='instancedata.json'):
    file = open(filename)
    file_dict = json.loads(''.join(file.readlines()))
    file.close()
    return file_dict


def download_file(url, file_path, timeout):
    os.makedirs('\\'.join(file_path.split('/')[:-1]), exist_ok=True)
    get_file = requests.get(url, timeout=timeout, stream=True)
    with open(file_path, mode='wb') as fd:
        for chunk in get_file.iter_content(chunk_size=256):
            fd.write(chunk)


def install_instance(instance_dict):
    # Implementing logging system
    instance_name = list(instance_dict.keys())[0]
    log_window = tk.Tk()
    log_window.title('Installing instance ' + instance_name)
    log_text = tk.Text(log_window, state='disabled')
    log_text.grid()

    async def log(message):
        log_text['state'] = 'normal'
        log_text.insert(tk.END, time.strftime('[%H:%M:%S] ', time.localtime()) + message + '\n')
        log_text['state'] = 'disabled'
        log_window.update()

    async def install():
        timeout = 30  # seconds

        # Importing version_manifest.json
        assets_dict = load_from_file('minecraft_assets\\version_manifest.json')

        # Downloading version.json
        get_version_json = None
        for i in assets_dict['versions']:
            if i['id'] == instance_dict[instance_name]['version']:
                get_version_json = requests.get(i['url'])
                break
        if get_version_json is None:
            raise ValueError('Invalid Minecraft version!')
        version_json = get_version_json.json()
        os.makedirs('instances\\' + instance_name + '\\versions\\' + instance_dict[instance_name]['version'])
        version_json_file = open('instances\\' + instance_name + '\\versions\\' + instance_dict[instance_name]['version'] +
                                 '\\' + instance_dict[instance_name]['version'] + '.json', mode='w')
        version_json_file.write(json.dumps(version_json))
        version_json_file.close()

        # First log message
        await log('Downloaded ' + instance_dict[instance_name]['version'] + '.json')

        # Downloading client.jar
        download_file(version_json['downloads']['client']['url'], 'instances/' + instance_name + '/versions/' +
                      instance_dict[instance_name]['version'] + '/' + instance_dict[instance_name]['version'] + '.jar',
                      timeout)
        await log('Downloaded ' + instance_dict[instance_name]['version'] + '.jar')

        # Downloading Log4J config
        download_file(version_json['logging']['client']['file']['url'], 'instances/' + instance_name + '/' +
                      version_json['logging']['client']['file']['id'], timeout)
        await log('Downloaded ' + version_json['logging']['client']['file']['id'])

        # Downloading assets config

        download_file(version_json['assetIndex']['url'], 'instances/' + instance_name +
                      '/assets/indexes/' + version_json['assetIndex']['id'] + '.json', timeout)
        await log('Downloaded ' + version_json['assetIndex']['url'].split('/')[-1])

        # Downloading libraries
        os_name = platform.platform()
        if os_name.startswith('Windows'):
            os_name = 'windows'
        elif os_name.startswith('Darwin'):
            os_name = 'osx'
        elif os_name.startswith('Linux'):
            os_name = 'linux'
        libraries = version_json['libraries']
        os.makedirs('instances/' + instance_name + '/bin/libraries')
        for library in libraries:
            artifact_is_allowed = True
            if 'rules' in library.keys():
                for i in library['rules']:
                    if 'os' in i:
                        if (i['action'] == 'disallow' and i['os']['name'] == os_name) or (
                                i['action'] == 'allow' and i['os']['name'] != os_name):
                            artifact_is_allowed = False
            if artifact_is_allowed and 'classifiers' not in library['downloads'].keys():
                download_file(library['downloads']['artifact']['url'], 'instances/' + instance_name + '/libraries/' +
                              library['downloads']['artifact']['path'], timeout)
                await log('Downloaded ' + library['downloads']['artifact']['path'].split('/')[-1])
            elif 'classifiers' in library['downloads'].keys():
                natives = ''
                if os_name == 'windows':
                    natives = 'natives-windows'
                elif os_name == 'osx':
                    natives = 'natives-macos'
                elif os_name == 'linux':
                    natives = 'natives-linux'
                if natives in library['downloads']['classifiers']:
                    download_file(library['downloads']['classifiers'][natives]['url'], 'instances/' + instance_name +
                                  '/libraries/' + library['downloads']['classifiers'][natives]['path'], timeout)
                    await log('Downloaded ' + library['downloads']['classifiers'][natives]['path'].split('/')[-1])
                    with zipfile.ZipFile('instances/' + instance_name + '/libraries/' +
                                         library['downloads']['classifiers'][natives]['path']) as downloaded_file:
                        downloaded_file.extractall('instances/' + instance_name + '/bin/libraries')
                    if 'META-INF' in os.listdir('instances/' + instance_name + '/bin/libraries'):
                        shutil.rmtree('instances/' + instance_name + '/bin/libraries/META-INF')
                    await log('Extracted ' + library['downloads']['classifiers'][natives]['path'].split('/')[-1])

        # Downloading assets
        assets_index = load_from_file('instances/' + instance_name + '/assets/indexes/1.18.json')
        x = 1
        for i in assets_index['objects'].keys():
            asset_hash = assets_index['objects'][i]['hash']
            download_file('https://resources.download.minecraft.net/' + asset_hash[:2] + '/' + asset_hash,
                          'instances/' + instance_name + '/assets/objects/' + asset_hash[:2] + '/' + asset_hash, timeout)
            await log(f"Downloaded asset {i.split('/')[-1]} ({x}/{len(assets_index['objects'])})")
            x += 1
        await log('Finished!')

    # Handling async
    loop = asyncio.get_event_loop()
    loop.run_until_complete(install())
    loop.close()


def launch_instance(instance_dict, user_details):
    instance_name = list(instance_dict.keys())[0]
    uuid = list(user_details.keys())[0]
    arguments_dict = load_from_file('instances/' + instance_name + '/versions/' +
                                    instance_dict[instance_name]['version'] + '/' +
                                    instance_dict[instance_name]['version'] + '.json')
    arguments = ''
    os_name = platform.platform()
    if os_name.startswith('Windows'):
        if os_name.startswith('Windows-10'):
            os_name = 'windows-10'
        else:
            os_name = 'windows'
    elif os_name.startswith('Darwin'):
        os_name = 'osx'
    elif os_name.startswith('Linux'):
        os_name = 'linux'
    if 'arguments' not in arguments_dict and 'minecraftArguments' in arguments_dict:
        arguments_dict['arguments'] = {}
        arguments_dict['arguments']['game'] = arguments_dict['minecraftArguments'].split(' ')
        arguments_dict['arguments']['jvm'] = [{"rules": [{"action": "allow", "os": {"name": "osx"}}],
                                               "value": ["-XstartOnFirstThread"]},
                                              {"rules": [{"action": "allow", "os": {"name": "windows"}}],
                                               "value": "-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw."
                                                        "exe_minecraft.exe.heapdump"},
                                              {"rules": [{"action": "allow", "os": {"name": "windows",
                                                                                    "version": "^10\\."}}],
                                               "value": ["-Dos.name=Windows 10", "-Dos.version=10.0"]},
                                              {"rules": [{"action": "allow", "os": {"arch": "x86"}}],
                                               "value": "-Xss1M"}, "-Djava.library.path=${natives_directory}",
                                              "-Dminecraft.launcher.brand=${launcher_name}",
                                              "-Dminecraft.launcher.version=${launcher_version}",
                                              "-cp", "${classpath}"]
    for i in arguments_dict['arguments']['jvm']:
        if type(i) == dict:
            if 'rules' in i.keys():
                if i['rules'][0]['action'] == 'allow':
                    if 'version' in i['rules'][0]['os'] and os_name.endswith('-10'):
                        arguments += '"-Dos.name=Windows 10" -Dos.version=10.0 '
                    elif 'name' in i['rules'][0]['os']:
                        if os_name == i['rules'][0]['os']['name']:
                            if type(i['value']) == list:
                                for j in i['value']:
                                    arguments += j + ' '
                            elif type(i['value']) == str:
                                arguments += i['value'] + ' '
                    elif 'arch' in i['rules'][0]['os']:
                        arguments += i['value'] + ' '
        elif i == '-cp':
            files = []
            for library in arguments_dict['libraries']:
                is_allowed = True
                if 'rules' in library.keys():
                    for j in library['rules']:
                        if 'os' in j:
                            if (j['action'] == 'disallow' and j['os']['name'] == os_name) or (
                                    j['action'] == 'allow' and j['os']['name'] != os_name):
                                is_allowed = False
                if is_allowed and 'artifact' in library['downloads']:
                    files.append('instances/' + instance_name + '/libraries/' +
                                 library['downloads']['artifact']['path'])
            files.append('instances/' + instance_name + '/versions/' +
                         instance_dict[instance_name]['version'] + '/' +
                         instance_dict[instance_name]['version'] + '.jar')
            arguments += (i + ' ' + ';'.join(files) + ' ')
        elif '$' in i:
            argument_name = i.split('=')[0] + '='
            if argument_name == '-Djava.library.path=':
                arguments += (argument_name + 'instances/' + instance_name + '/bin/libraries ')
            elif argument_name == '-Dminecraft.launcher.brand=':
                arguments += (argument_name + 'minecraft-launcher ')
            elif argument_name == '-Dminecraft.launcher.version=':
                arguments += (argument_name + '2.3.136 ')  # random version I got from my launch command,
                                                           # subject to change whenever necessary.
        else:
            arguments += i + ' '
    arguments += (arguments_dict['mainClass'] + ' -Xmx' + str(instance_dict[instance_name]['maxmem']) + 'M -Xms' +
                  str(instance_dict[instance_name]['minmem']) + 'M ' +
                  arguments_dict['logging']['client']['argument'].split('=')[0] + '=' + 'instances/' + instance_name +
                  '/' + arguments_dict['logging']['client']['file']['id'] + ' -XX:+UnlockExperimentalVMOptions '
                                                                            '-XX:+UseG1GC -XX:G1NewSizePercent=20 '
                                                                            '-XX:G1ReservePercent=20 '
                                                                            '-XX:MaxGCPauseMillis=50 '
                                                                            '-XX:G1HeapRegionSize=32M ')
    for i in arguments_dict['arguments']['game']:
        if type(i) == str:
            if i.startswith('$'):
                continue
            elif i == '--username':
                arguments += (i + ' ' + user_details[uuid]['name'] + ' ')
            elif i == '--version':
                arguments += (i + ' ' + arguments_dict['id'] + ' ')
            elif i == '--gameDir':
                arguments += (i + ' instances/' + instance_name + ' ')
            elif i == '--assetsDir':
                arguments += (i + ' instances/' + instance_name + '/assets ')
            elif i == '--assetIndex':
                arguments += (i + ' ' + arguments_dict['assets'] + ' ')
            elif i == '--uuid':
                arguments += (i + ' ' + uuid + ' ')
            elif i == '--accessToken':
                arguments += (i + ' ' + user_details[uuid]['access_token'] + ' ')
            elif i == '--userType':
                arguments += (i + ' msa ')
        else:
            continue
    print(arguments)
    subprocess.call(instance_dict[instance_name]['java_path'] + ' ' + arguments, shell=True)


if __name__ == '__main__':
    print('why?')
