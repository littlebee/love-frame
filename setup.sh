#!/bin/bash

# echo on
set -x

# stop on all errors
set -e

TARGET_DIR="/home/pi/love-frame"

mkdir -p "$TARGET_DIR/data/messages"
mkdir -p "$TARGET_DIR/data/gallery"

# sudo apt-get update
# sudo apt-get -y upgrade

# audio and video needs
sudo apt install -y ffmpeg python3-pyaudio
sudo pip3 install pyaudio pygame

# opencv
sudo apt install -y libatlas-base-dev libjasper-dev libqtgui4  libqt4-test libhdf5-dev
sudo pip3 install flask opencv-contrib-python==4.5.5.62 imutils opencv-python==3.4.2.17 numpy==1.14.5
sudo pip3 install numpy --upgrade

# system utils
sudo pip3 install psutil

# needed for the LEDs
sudo pip3 install adafruit-circuitpython-neopixel

# Make the pigame app automatically start in raspian desktop, full screen
sudo cp $TARGET_DIR/setup/files/lxe-autostart /etc/xdg/lxsession/LXDE-pi/autostart

# I needed to change the default pulseaudio device to use the HDMI audio out.
# The Elecrow 7" has a loud amplifier built in.
pacmd set-default-sink 0
