#!/bin/bash
DIR=$(dirname "${BASH_SOURCE[0]}")
mkdir -p /usr/local/bin/urleater-get
cp $DIR/src/urleater-get.py /usr/local/bin/urleater-get/
cp $DIR/src/urleater-get.conf /etc/
cp $DIR/initscripts/* /etc/init.d/
if [ -f /etc/debian_version ];then
  update-rc.d -n urleater-get defaults
elif [ -f /etc/redhat-version ];then
  chkconfig --add urleater-get 
  chkconfig urleater on
fi
