#!/usr/bin/python3
import sys
import pyudev
import re
import json

# Once a device is plugged into the machine, we want to begin logging the device
from egadd import get_devices, get_hardware_devices, set_hardware_devices
from cache import Cache

# usage: python3 parascope.py [dev]
#	dev		a mode to run for debugging so the log files don't get clogged up

# The program to implement Monitor

# First ensure pyudev has been successfully installed on the current machine

settings_dict = {}

# get_settings
def get_settings():
	global settings_dict
	try:
		with open('data/settings.json') as data:
			settings_dict = json.load(data)
	except:
		print("Error opening settings.json!")

def set_settings():
	global settings_dict
	try:
		with open('data/settings.json', 'w') as outfile:
			json.dump(settings_dict, outfile, indent=4)
	except:
		print("Error opening settings.json!")

if 'pyudev' not in sys.modules:
	print("In order to run this program, you must import the pyudev module")
	print("\t$ python3 -m pip install pyudev")
	sys.exit()

# grabbing settings before anything else and checking for first run
get_settings()
# checking if first_run is true (true = this is the users first time running the program)
if settings_dict["first_run"]:
	settings_dict["first_run"] = 0
	set_hardware_devices()
	set_settings()

get_hardware_devices()
Cache.set_cache()

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
	print("Press Ctrl + C to terminate")

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')

try:
	for action, device in monitor:
		# using split to count how many sub dir
		slash_count = str(device).split("/")

		if action == "add":
			if len(slash_count) == 7:
				if dev_mode == True:
					get_devices()
				else:
					print("\33[31m{}:{}\33[0m".format(action, device))
					Cache.check_cache()	
					get_devices()
		elif action == "remove": # this works perfect
			if len(slash_count) == 7:
				if dev_mode == True:
					get_devices()
				else:
					print("\33[31m{}:{}\33[0m".format(action, device))
					Cache.check_cache()
					get_devices()
		elif action == "bind" or action == "unbind":
			continue
		else:
			sys.exit()
except KeyboardInterrupt:
	print("\n")
	print("Parascope Monitor Terminated")
	pass