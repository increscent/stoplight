#!/usr/bin/python3

import subprocess
import time
import base64
import io

# compile the serializer
subprocess.call(["./compile.sh"])

ssid = base64.b64encode(subprocess.check_output(["./serialize", "35.5", "35.5", "2", "2", "1", "5", "3", "1", "0", "6", "16"])).decode("ascii")

print(ssid)

dev_null = open("/dev/null", "w")
hostapd_default_conf = open("./hostapd_default.conf", "r").read()

while True:
    hostapd_conf = open("./hostapd.conf", "w")
    hostapd_conf.write(hostapd_default_conf)
    hostapd_conf.write("\nssid={}\n".format(ssid))
    hostapd_conf.close()

    hostapd = subprocess.Popen(["hostapd", "./hostapd.conf"], stdout=dev_null, stderr=dev_null)
    time.sleep(1)
    hostapd.terminate()
