#!/usr/bin/python3
import sys
import pyudev
import re
# Once a device is plugged into the machine, we want to begin logging the device
from egadd import get_devices

# usage: python3 parascope.py [dev]
#	dev		a mode to run for debugging so the log files don't get clogged up

# The program to implement Monitor

# First ensure pyudev has been successfully installed on the current machine
if 'pyudev' not in sys.modules:
	print("In order to run this program, you must import the pyudev module")
	print("\t$ python3 -m pip install pyudev")
	sys.exit()

# by default it will not run dev mode
dev_mode = False

if (len(sys.argv) == 2):
	if (sys.argv[1] == "dev"):
		# running in dev mode, do not create log files and only print the device/action
		dev_mode = True
		print("\33[32mMonitoring dev mode\33[0m")
	else:
		print("usage: python3 parascope.py [dev]")
		sys.exit()

# list of actions that occur
actions = []

# simple message to notify user of a successful launch
if dev_mode == False:
	print("\33[33mMonitoring started, not in dev mode\33[0m")

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')

for action, device in monitor:
	# using split to count how many sub dir
	slash_count = str(device).split("/")

	if action == "add":
			if len(slash_count) == 7:
				print("\33[31m{}:{}\33[0m".format(action, device))	
				#get_devices("ADD")
				get_devices()
	elif action == "remove": # this works perfect
		if len(slash_count) == 7:
			print("\33[31m{}:{}\33[0m".format(action, device))
			#get_devices("REMOVE")
			get_devices()
	elif dev_mode == True:
		get_devices(1)
	elif action == "bind" or action == "unbind":
		continue
	else:
		#unknown action occured
		#print (action)
		sys.exit()