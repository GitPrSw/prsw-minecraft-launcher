import subprocess


class minecraft_instance:
    def __init__(self, instance_name: str,
                 instance_path: str,
                 executable_name: str,
                 versionargs: str,
                 lastplayed: int,
                 major_version: str,
                 java_path: str='java',
                 maxmem: int = 1024,
                 minmem: int = 256,
                 extra_args: str = ''):
        self.instance_name = instance_name
        self.instance_path = instance_path
        self.executable_name = executable_name
        self.versionargs = versionargs
        self.java_path = java_path
        self.maxmem = maxmem
        self.minmem = minmem
        self.extra_args = extra_args
        self.lastplayed = lastplayed
        self.major_version = major_version

    def launch(self, login_details):
        subprocess.call('{0} -jar {1}{2} -Xmx{3}M -Xms{4} {5} {6} -{7} -{8} -{9}'.format(self.java_path, self.instance_path, self.executable_name,
                                                              str(self.maxmem), str(self.minmem), self.versionargs,
                                                              self.extra_args, login_details[0], login_details[1], login_details[2]), shell=True)

    def exportdata(self):
        return {str(self.lastplayed): {'instance_name': self.instance_name,
                                       'instance_path': self.instance_path,
                                       'executable_name': self.executable_name,
                                       'versionargs': self.versionargs,
                                       'java_path': self.java_path,
                                       'maxmem': self.maxmem,
                                       'minmem': self.minmem,
                                       'extra_args': self.extra_args}}
