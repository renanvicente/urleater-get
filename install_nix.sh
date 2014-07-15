#!/bin/bash
DIR=$(dirname "${BASH_SOURCE[0]}")
mkdir -p /usr/local/bin/urleater-get
cp $DIR/src/urleater-get.py /usr/local/bin/urleater-get/
cp $DIR/src/urleater-get.conf /etc/
if [ -f /etc/debian_version ];then
  cp $DIR/initscripts/urleater-get-debian /etc/init.d/
  update-rc.d -n urleater-get defaults
elif [ -f /etc/redhat-version ];then
  cp $DIR/initscripts/urleater-get-redhat /etc/init.d/
  chkconfig --add urleater-get 
  chkconfig urleater on
else
  echo 'System not supported'
fi
