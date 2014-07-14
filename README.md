urleater-get
============

Urleater-get is a client to get urls from vhosts and send to my other project urleater-server.


At the moment support:

- Apache
- Nginx

Dependencies
-------------

- python2.7

Installing
-------------

    git clone https://github.com/renanvicente/urleater-get
    cd urleater-get
    ./install_nix.sh

Config example
-------------

    cat /etc/urleater-get.conf
    
      [client]
      customer=renanvicente
      hostname=debian.renanvicente.com
      [server]
      server=urleater.renanvicente.com
      port=7777

The script will try to check if it's running apache or ngynx and get the right directory to search for urls but you can specify the directory if you want to.

      [client]
      customer=renanvicente
      hostname=debian.renanvicente.com
      vhost_directory=/opt/nginx/conf.d
      [server]
      server=urleater.renanvicente.com
      port=7777

if you have more than one directory the automatically search won't work , you need to specify

      [client]
      customer=renanvicente
      hostname=debian.renanvicente.com
      vhost_directory=['/opt/nginx/conf.d','/opt/nginx/sites-enabled']
      [server]
      server=urleater.renanvicente.com
      port=7777


Puppet Module
--------------

If you are using puppet in your infraestruture:
I wrote a module to manage the project:

https://forge.puppetlabs.com/renanvicente/urleater




