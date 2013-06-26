import multiprocessing
import netifaces
import os
import socket

# some config variables
cfg_eth0_address = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr'] # usually the public IP on Rackspace/VM
cfg_eth1_address = netifaces.ifaddresses('eth1')[netifaces.AF_INET][0]['addr'] # usually the internal IP on Rackspace/VM
cfg_port = '8000' # the port we should bind to

# if we are athena use the localhost
if 'athena' in socket.gethostname():
    cfg_eth1_address = '127.0.0.1'

# the gunicorn parameters
bind = cfg_eth1_address + ':' + cfg_port
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync' # default: sync; alternate: gevent
pidfile = 'gunicorn.pid'
proc_name = 'snap_api'
timeout = 120
graceful_timeout = 120