#!/usr/bin/python3

import subprocess
import time

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
