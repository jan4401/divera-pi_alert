#!bin/bash

#setup raspberry pi as ff divera for mon and alert

apt install git
apt install python3-pip
pip3 install requests

apt install python3-rpi.gpio
sudo systemctl enable pialert.service 
systemctl start pialert.service

#
cd /opt
#git clone REPO
git clone https://github.com/jan4401/divera-pi_alert.git

cp /opt/divera-pi_alert/static/pialert.service /etc/systemd/system/

