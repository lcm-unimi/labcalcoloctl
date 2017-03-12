#!/usr/bin/python

import argparse
import textwrap
import os
import subprocess, sys
from threading import Thread

parser = argparse.ArgumentParser()

## positional arguments
parser.add_argument( 'cmd', nargs="?", choices=('status','start','stop'), default='status', 
                     help='Specify command to execute, default is \'status\'' )

## optional arguments
parser.add_argument( '-a', '--all', action='store_true', dest='lcm',
                     help='All LCM nodes are considered' )
parser.add_argument( '-n', nargs='+', dest='node',  
                     help='Select one or more nodes (at least one)' )
parser.add_argument( '-1', '--lcm1', action='store_true', dest='lcm1',
                     help='LCM1 nodes are considered' )
parser.add_argument( '-2', '--lcm2', action='store_true', dest='lcm2',
                     help='LCM2 nodes are considered' )
parser.add_argument( '-v', '--version', action='version', version='%(prog)s 1.0', 
                     help='Print program version' )	   
## 
args = parser.parse_args()

## main path (you don't say)
main_path = "/home/elisaaliverti/150/1607_vmcalcolo/main"

class Host(Thread):
   # Constructor
   def __init__(self, name, location):
      # Fork the thread first thing
      Thread.__init__(self)
      # Variables initialization
      self.hostname = name
      self.location = location
      
   # Ping the host to see if it's up
   def isup(self):
      # Is the host up?
      ping = os.popen("ping -w1 -c1 " + self.hostname, "r")
      # print("pinging " + self.hostname)
      if "0 received" in ping.read():
	 return False
      else:
         return True

   def sshcommand(self, command):
      if self.isup():
         ssh = subprocess.Popen( ["ssh", "%s" % self.hostname, command],
       	         		 shell = False,
				 stdout = subprocess.PIPE,
				 stderr = subprocess.PIPE )
         result = ssh.stdout.readlines()
         if result == []:
            error = ssh.stderr.readlines()
	    print >> sys.stderr, "ERROR: %s" % error
         else:
            print result
	    ## non ci sono piu` i colori! :(

   def vmstart(self):
      startcmd = main_path + " 1"
      self.sshcommand(startcmd)

   def vmstop(self):
      stopcmd = main_path + " 0"
      self.sshcommand(stopcmd)

   def vmstatus(self):
   ## si poteva anche fare come per gli altri due, solo che poi dacche` si sarebbe passati da sshcommand avrebbe stampato l'output di grep automaticamente...
      statuscmd = "ps aux | grep qemu"
      if self.isup():
         ssh = subprocess.Popen( ["ssh", "%s" % self.hostname, statuscmd],
       	         		 shell = False,
				 stdout = subprocess.PIPE,
				 stderr = subprocess.PIPE )
         result = ssh.stdout.readlines()
         if result == []:
            error = ssh.stderr.readlines()
	    print >> sys.stderr, "ERROR: %s" % error
         else:
	    # print result
            ## this way, experimentally, you always grep at least 3 processes (ssh host ps aux | grep qemu, ps aux | grep qemu & grep qemu)
            if len(result) < 4:
               print("VM is not running on %s" % self.hostname)
               return False
            else:
               print("VM is running on %s" % self.hostname)
	       return True

### end class Host

## Host list
lcm1 = [Host('abe',	'LCM1'),
	Host('crash',	'LCM1'),
	Host('duke',	'LCM1'),
	Host('glados',	'LCM1'),
	Host('lara',	'LCM1'),
	Host('link',	'LCM1'),
	Host('king',	'LCM1'),
	Host('pang',	'LCM1'),
	Host('pong',	'LCM1'), 
        Host('snake',	'LCM1'),
	Host('sonic',	'LCM1'),
	Host('spyro',	'LCM1'),
	Host('yoshi',	'LCM1')]
lcm2 = [Host('actarus',	'LCM2'),
	Host('elwood',	'LCM2'),
	Host('gex',	'LCM2'),
	Host('gin',	'LCM2'),
	Host('jake',	'LCM2'),
	Host('kirk',	'LCM2'),
	Host('martini',	'LCM2'),
	Host('picard',	'LCM2'),
        Host('q',	'LCM2'),
	Host('raziel',	'LCM2'),
	Host('sarek',	'LCM2'),
	Host('spock',	'LCM2'),
	Host('tron',	'LCM2'),
	Host('worf',	'LCM2'),
	Host('zombie',	'LCM2')]
lcm = lcm1 + lcm2
##


hosts = []

if ( args.lcm or (args.lcm1 and args.lcm2) ): hosts += lcm
else: 
   if args.lcm1: 
      hosts += lcm1 
      if args.node:
         for i in args.node: 
	    for j in lcm2: 
	       if (i==j.hostname): hosts.append(j) 
   elif args.lcm2:
      hosts += lcm2
      if args.node:
         for i in args.node:
	    for j in lcm1:
	       if (i==j.hostname): hosts.append(j)
   elif args.node:
      for i in args.node:
         for j in lcm: 
	    if (i==j.hostname): hosts.append(j)
   ## n.b.: non ci sono controlli sui nomi dei nodi che vengono passati...
   ## inoltre non so se sia ovvio, ma se si scrive il comando status/start/stop DOPO -n nomenodo crede sia un nome sbagliato di nodo e esegue il comando status (default)

# print hosts

if args.cmd == 'status':
   # print("status")
   for i in hosts:
      i.vmstatus()
elif args.cmd == 'start':
   # print("start")
   for i in hosts:
      i.vmstart()
elif args.cmd == 'stop':
   # print("stop")
   for i in hosts:
      i.vmstop()
