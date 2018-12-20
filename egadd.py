#!/usr/bin/python3
import pyudev
import sys
import datetime		# log files will be named with current date/time

# usage: python egadd.py

# which subsystem do we want to monitor / analyze?
# default = USB
subsys = "usb"

# get current date and time for naming log file
timestamp = datetime.datetime.now()

# devices list
devices = [None]

def udev_connect():
	# establish a connection to the udev device database
	context = pyudev.Context()
	
	# create a file with the format {YEAR} {MONTH} {DAY} {HOUR} {MINUTE} {SECOND}
	file_name = timestamp.strftime("logs/%Y%m%d%H%M%s")
	file = open(file_name, "w+")

	# list the devices in the usb subsystem
	for device in context.list_devices(subsystem=subsys):
		#print("{}".format(device))
		file.write(str(device) + "\n")
	
	file.close()
	return

	
if __name__ == "__main__":
	udev_connect()
	
