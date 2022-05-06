import platform


def version_json_parser(filename):
    pass


def prepare_launch_command(java_path, instance_path, executable_name, maxmem, minmem, versionargs, extra_args, major_version, login_information):
    command = f'{java_path}'
    if platform.platform().startswith('Windows-10'):
        command += ' "-Dos.name=Windows 10" -Dos.version=10.0'
    command += f' -XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump ' \
               f'-Djava.library.path=%APPDATA%\.minecraft\\versions\\{major_version}\\{executable_name} '