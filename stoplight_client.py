#!/usr/bin/python3

import subprocess
import time
import base64
import io
import commands
import re

# compile the serializer
subprocess.call(["./compile.sh"])

while True:
    ssid_list = subprocess.check_output(commands.scan).decode("ascii")
    ssids = list(filter(lambda x: len(x) == 32, re.findall(r'SSID: (.*)\n', ssid_list)))

    for ssid in ssids:
        ssid_f = open("./.ssid_tmp", "wb")
        ssid_f.write(base64.b64decode(ssid))
        ssid_f.close()

        ssid_f = open("./.ssid_tmp", "rb")
        args = subprocess.check_output(["./serialize"], stdin=ssid_f);
        ssid_f.close()

        print(args.decode("ascii"))
