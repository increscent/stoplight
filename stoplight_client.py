#!/usr/bin/python3

import subprocess
import time
import base64
import io
import commands
import re

# compile the serializer
subprocess.call(["./compile.sh"])

dev_null = open("/dev/null", "w")
server = subprocess.Popen(["http-server", "ui", "-c-1"], stdout=dev_null, stderr=dev_null)

prev_ssid = None
consecutive = 0
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

        state_f = open("./ui/state.txt", "w");
        state_f.write(args.decode("ascii"));
        state_f.close();

        #print(args.decode("ascii"))

        if ssid == prev_ssid:
            consecutive += 1
        else:
            print("Beacons per second: " + str(consecutive))
            consecutive = 1
            prev_ssid = ssid
