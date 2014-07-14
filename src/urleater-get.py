#!/usr/bin/env python
from os.path import join,isfile,realpath,dirname,isdir
from os import walk
from sys import exit, stderr
from fnmatch import fnmatch
from re import compile,IGNORECASE
from json import dumps, loads
from socket import socket, AF_INET, SOCK_STREAM, gethostname
from ConfigParser import ConfigParser
from time import sleep


'''
Function to find all files that match with a pattern
'''
def find(pattern, path):
  result = []
  for root, dirs, files in walk(path):
    for name in files:
      if fnmatch(name, pattern):
        result.append(join(root, name))
  return result

'''
Function to find all vhost files
'''

def check_system():
  if isfile('/etc/debian_version'):
    if isdir('/etc/nginx/sites-enabled'):
      directory = '/etc/nginx/sites-enabled'
    elif isdir('/etc/nginx/conf.d'):
      directory = '/etc/nginx/conf.d'
    elif isdir('/etc/apache2/sites-enabled'):
      directory = '/etc/apache2/sites-enabled',
    else:
      directory = None
      print >> stderr, ('No directory to search')
      exit(1)
  elif isfile('/etc/redhat-release'):
    if isdir('/etc/nginx/sites-enabled'):
      directory = '/etc/nginx/sites-enabled'
    elif isdir('/etc/nginx/conf.d'):
      directory = '/etc/nginx/conf.d'
    elif isdir('/etc/httpd/sites-enabled'):
      directory = '/etc/httpd/sites-enabled'
    else:
      directory = None
      print >> stderr, ('No directory to search')
      exit(1)
  else:
    directory = None
    print('system not supported yet')
    exit(1)
  return directory

def find_all_files(path):
  files = find('*', path)
  return files

'''
Function to get all vhosts names
'''
def get_vhosts_name(paths):
  NAMES_VHOST_RE = compile(r'^(\s+)?(ServerAlias|ServerName|server_name)\s(.+)',IGNORECASE)
  vhosts = ''
  for path in paths:
    for file in find_all_files(path):
      if file is not 'default':
        vhostfile = open(file,'r')
        for linha in vhostfile:
          match = NAMES_VHOST_RE.match(linha)
          if match is not None:
            if 'default'  not in match.group(3):
              vhosts += match.group(3).strip() + ' '
  return vhosts


def send_data(server,server_port,path,hostname,customer):
  sock = socket(AF_INET, SOCK_STREAM)
  sock.connect((server,server_port))
  ip = sock.getsockname()[0]
  vhost_dict = { 'customer': customer,
                 'hostname': hostname,
                 'ip':  ip,
                 'urls': get_vhosts_name(path) }
  sock.send(dumps(vhost_dict))
  result = loads(sock.recv(1024))
  print result


def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


def getConfigValues(section,filename=dirname(realpath(__file__)) + '/urleater.conf'):
  Config.read(filename)
  if section == 'server':
    if ConfigSectionMap(section).has_key('server'):
      server = ConfigSectionMap(section)['server']
    if ConfigSectionMap(section).has_key('port'):
      port = int(ConfigSectionMap(section)['port'])
    config_dict = {'server': server, 'port': port }
  else:
    if ConfigSectionMap(section).has_key('hostname'):
      hostname = ConfigSectionMap(section)['hostname']
    else:
      hostname = gethostname()
    if ConfigSectionMap(section).has_key('customer'):
      customer   = ConfigSectionMap(section)['customer']
    else:
      customer   = 'others'
    if ConfigSectionMap(section).has_key('vhost_directory'):
      vhost_directory = ConfigSectionMap(section)['vhost_directory']
    else:
      vhost_directory = check_system()
    print vhost_directory
    config_dict = {'hostname': hostname, 'customer': customer , 'directory': vhost_directory }
  return config_dict
  


if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option("-f","--config",dest="filename",help='Config file',metavar='CONFIG_FILE')
  ( options, args) = parser.parse_args()
  Config = ConfigParser()
  if options.filename:
    conf_server = getConfigValues('server',options.filename)
    conf_client = getConfigValues('client',options.filename)
  else:
    conf_server = getConfigValues('server')
    conf_client = getConfigValues('client')
  while True:
    send_data(conf_server['server'],conf_server['port'],conf_client['directory'],conf_client['hostname'],conf_client['customer'])
    sleep(1800)
