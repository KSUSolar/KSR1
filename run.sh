#!/bin/sh

sudo ip link set can0 type can bitrate 500000
sudo ifconfig can0 up

python /home/pi/Desktop/KSR1/main.py
exit 0