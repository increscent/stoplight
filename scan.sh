#!/bin/bash

iw wlp3s0 scan freq 2412 flush passive | grep "SSID:" | awk '{ print $2 }'
