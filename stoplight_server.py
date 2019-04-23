#!/usr/bin/python3

import subprocess
import time
import base64
import io
import stoplight_config

# compile the serializer
subprocess.call(["./compile.sh"])

config = stoplight_config.config1

start = time.time()

def get_state(config, start):
    lon = config['lon']
    lat = config['lat']
    current = time.time() - start

    state = [lon, lat, len(config['directions'])]

    for d in config['directions']:
        cycle = d['green'] + d['yellow'] + d['red']
        d_current = current
        d_current += d['green']-d['time'] if d['color'] == 'green' else 0
        d_current += d['green']+d['yellow']-d['time'] if d['color'] == 'yellow' else 0
        d_current += d['green']+d['yellow']+d['red']-d['time'] if d['color'] == 'red' else 0
        d_current %= cycle

        d_color = 1 # green
        d_time = d['green']-d_current
        if d_current > d['green']:
            d_color = 2 # yellow
            d_time = d['green']+d['yellow']-d_current
        if d_current > d['green']+d['yellow']:
            d_color = 3 # red
            d_time = d['green']+d['yellow']+d['red']-d_current

        state += [d_color, 1 if d['left'] else 0, d['direction'], int(d_time)+1]

    return list(map(lambda x: str(x), state))

dev_null = open("/dev/null", "w")
hostapd_default_conf = open("./hostapd_default.conf", "r").read()

while True:
    state = get_state(config, start)
    print(state);
    ssid = base64.b64encode(subprocess.check_output(["./serialize"] + state)).decode("ascii")
    print(ssid)

    hostapd_conf = open("./hostapd.conf", "w")
    hostapd_conf.write(hostapd_default_conf)
    hostapd_conf.write("\nssid={}\n".format(ssid))
    hostapd_conf.close()

    hostapd = subprocess.Popen(["hostapd", "./hostapd.conf"], stdout=dev_null, stderr=dev_null)
    time.sleep(1)
    hostapd.terminate()
