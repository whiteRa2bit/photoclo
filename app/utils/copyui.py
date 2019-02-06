#!/usr/bin/env python
"""
This file helps to load client files to server. Requires scp module. Install it:
pip install scp

Usage:
./copyui.py config

In config file write destination all the files. Syntax:
<source>
<host>
<port>(NULL, if not)
<username>
<password>(NULL, if not)
<RSA_key>(NULL, if not)
index.html /home/user/server/templates/index.html
js,css /home/user/server/static/js # Folders recursively, files in together
/home/user/server/static # Other destinations without any names, comment after #
"""
import os
import sys

from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

config = sys.argv[1]
# source = sys.argv[2]
# url = re.split('@|:', sys.argv[3])
# password = sys.argv[4] if len(sys.argv) == 5 else None
with open(config) as file:
    lines = file.read().split('\n')

source = lines[0]
host = lines[1]
port = int(lines[2]) if lines[2] != 'NULL' else 22
username = lines[3]
password = lines[4] if lines[4] != 'NULL' else None
RSA_key_source = lines[5]


files2dist = dict()
files = set(f for f in os.listdir(source))

for i in range(6, len(lines)):
    line = lines[i]
    data = line.split('#')[0]
    files_and_dist = data.split(' ')
    if len(files_and_dist) > 1:
        for file in files_and_dist[0].split(','):
            files2dist[file] = files_and_dist[1]
            files.remove(file)
    else:
        for file in files:
            files2dist[file] = files_and_dist[0]

ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect(hostname=host, port=port, username=username, password=password,
            key_filename=RSA_key_source)

with SCPClient(ssh.get_transport()) as scp:
    for file in files2dist:
        if os.path.isfile(file):
            scp.put(file, remote_path=files2dist[file])
        else:
            scp.put(file, recursive=True, remote_path=files2dist[file])

ssh.close()

if __name__ == 'main':
    config = sys.argv[1]

    files2dist = dict()
    files = set(f for f in os.listdir(source))

    with open(config) as file_config:
        for line in file_config:
            data = line.split('#')[0]
            files_and_dist = data.split(' ')
            if len(files_and_dist) > 1:
                for file in files_and_dist[0].split(','):
                    files2dist[file] = files_and_dist[1]
                    files = files - set(file)
            else:
                for file in files:
                    files2dist[file] = files_and_dist[0]

    ssh = SSHClient()
    ssh.load_system_host_keys()
    if len(url) > 2:
        ssh.connect(hostname=url[1], username=url[0], port=int(url[3]))
    elif len(url) > 1:
        ssh.connect(hostname=url[1], username=url[0])
    else:
        ssh.connect(hostname=url[0])

    with SCPClient(ssh.get_transport()) as scp:
        for file in files2dist:
            if os.path.isfile(file):
                scp.put(file, remote_path=files2dist[file])
            else:
                scp.put(file, recursive=True, remote_path=files2dist[file])
