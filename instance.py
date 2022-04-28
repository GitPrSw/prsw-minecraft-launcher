import subprocess
import json


def last_played_instance():
    instance_dict = load_instances_from_file()
    last_played = {}
    last_playedtime = 0
    for i in instance_dict.keys():
        if instance_dict[i]['last_played'] > last_playedtime:
            last_played = {i: instance_dict[i]}
            last_playedtime = instance_dict[i]['last_played']
    if last_played == 0:
        return False
    else:
        return last_played


def load_instances_from_file():
    instance_file = open('instancedata.json')
    instance_dict = json.loads(''.join(instance_file.readlines()))
    instance_file.close()
    return instance_dict


def launch_instance(instance_dict):
    # subprocess.call(f'java {args}', shell=True)
    # Shall be added with a robust system for what arguments we need and how to get them.
    pass
