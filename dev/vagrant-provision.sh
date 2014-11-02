#!/bin/bash
##########################################
# Put all installation commands here
##########################################
sudo apt-get update
sudo apt-get install -y vim
sudo apt-get install -y python-virtualenv python-dev
#
# Run a bunch of commands as the user
echo "===> Running scripts"
su $1 << 'SCRIPT'
#cd /vagrant
#virtualenv ve
#ls
SCRIPT
