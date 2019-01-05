#!/usr/bin/python3
import sys
import pyudev
# Once a device is plugged into the machine, we want to begin logging the device
from egadd import log_devices

# usage: python3 parascope.py

# The program to implement Monitor

# First ensure pyudev has been successfully installed on the current machine
if 'pyudev' not in sys.modules:
	print("In order to run this program, you must import the pyudev module")
	print("\t$ python3 -m pip install pyudev")
	sys.exit()
	
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='input')
for action, device in monitor:
	print("{}: {}".format(action, device))
	
