#!/usr/bin/python3

import subprocess
import time
import base64
import io

subprocess.call(["./compile.sh"])

ssid = base64.encodebytes(subprocess.check_output(["./serialize", "35.5", "35.5", "2", "2", "1", "5", "3", "1", "0", "6", "16"]))

print(ssid.decode("ascii"))

ssid_f = open("./.ssid_tmp", "wb")
ssid_f.write(base64.decodebytes(ssid))
ssid_f.close()

ssid_f = open("./.ssid_tmp", "rb")

args = subprocess.check_output(["./serialize"], stdin=ssid_f);

ssid_f.close()

print(args.decode("ascii"))

'''
dev_null = open("/dev/null", "w")
hostapd_default_conf = open("./hostapd_default.conf", "r")
default_conf = hostapd_default_conf.read()

#hostapd_bin = subprocess.check_output(["which", "hostapd"])

tick = 0
while True:
    tick += 1
    hostapd_conf = open("./hostapd.conf", "w")
    hostapd_conf.write(default_conf)
    hostapd_conf.write("\nssid=testing{}\n".format(tick))
    hostapd_conf.close()

    hostapd = subprocess.Popen(["hostapd", "./hostapd.conf"], stdout=dev_null, stderr=dev_null)

    time.sleep(1)

    hostapd.terminate()
'''
