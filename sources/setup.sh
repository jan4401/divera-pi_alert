#!bin/bash

#setup raspberry pi as ff divera for mon and alert
apt update
apt upgrade
apt install git
apt install python3-pip
pip3 install requests
sudo adduser fireman
apt install python3-rpi.gpio
sudo systemctl enable pialert.service 
systemctl start pialert.service

#
cd /opt
#git clone REPO

cp /opt/ffpi/static/pialert.service /etc/systemd/system/

chown -R fireman /opt/ffpi
