import instance
import windows
import json

instances = []
instancekeys = []

# accessing previously saved instance data

instancefile = open('instancedata.json')
try:
    instancedict = json.loads(''.join(instancefile.readlines()))
except:
    instancedict = {}
instancefile.close()

for i in instancedict.keys():
    instancekeys.append(i)
instancekeys.sort(reverse=True)
for i in instancekeys:
    instances.append(instance.minecraft_instance(instancedict['instance_name'],
                                                 instancedict['instance_path'],
                                                 instancedict['executable_name'],
                                                 instancedict['versionargs'],
                                                 i,
                                                 instancedict['java_path'],
                                                 instancedict['maxmem'],
                                                 instancedict['minmem'],
                                                 instancedict['extra_args']))

# Rendering main window
windows.load_main_window(instances)

export = open('instancedata.json', mode='w')
exportdict = {}

try:
    for i in instances:
        exportdict += i.exportdata()
finally:
    export.write(json.dumps(exportdict))
    export.close()
