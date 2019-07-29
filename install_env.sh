#!/usr/bin/env bash

# Install dependencies
sudo apt install python3 python3-pip git unzip
# Create a new virtual env
python3 -m venv tasmota
# Activate, upgrade pip, install platformio and esptool
. tasmota/bin/activate
pip install --upgrade pip
pip install -U platformio
pip install esptool
# Download sources
#git clone https://github.com/arendst/Sonoff-Tasmota.git
# Sources have been downloaded and are attached for stability
unzip Sonoff-Tasmota.zip
mv Sonoff-Tasmota-development src-tasmota
# Final steps
mkdir bin
sudo usermod -a -G dialout $usermod
echo "Debe reinicar el computador."