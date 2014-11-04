#!/bin/bash
##########################################
# Put all installation commands here
##########################################
sudo apt-get update
sudo apt-get install -y vim
sudo apt-get install -y python-virtualenv python-dev
# Scripts for PIL
# from: http://codeinthehole.com/writing/how-to-install-pil-on-64-bit-ubuntu-1204/
sudo apt-get install python-dev libjpeg-dev libfreetype6-dev zlib1g-dev
sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/
sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/
# after this PIL section you can now do a pip install PIL and it will work
#
# Run a bunch of commands as the user
echo "===> Running scripts"
su $1 << 'SCRIPT'
#cd /vagrant
#virtualenv ve
#ls
SCRIPT
