#!/bin/bash
DIR=$(dirname "${BASH_SOURCE[0]}")
mkdir -p /usr/local/bin/urleater-get
cp $DIR/src/urleater-get.py /usr/local/bin/urleater-get/
cp $DIR/src/urleater-get.conf /etc/
if [ -f /etc/debian_version ];then
  cp $DIR/initscripts/urleater-get-debian /etc/init.d/urleater-get
  update-rc.d -n urleater-get defaults
elif [ -f /etc/redhat-release ];then
  cp $DIR/initscripts/urleater-get-redhat /etc/init.d/urleater-get
  chkconfig --add urleater-get 
  chkconfig urleater-get on
else
  echo 'System not supported'
fi
