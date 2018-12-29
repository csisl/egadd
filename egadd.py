#!/usr/bin/python3
import pyudev
import sys
import datetime		# log files will be named with current date/time

# usage: python egadd.py [dev]
# 	dev: run in dev mode, for testing purposes only & no log file is created

# COLOR CODES
CRESET = '\33[0m'
CGREEN = '\33[32m'
CRED   = '\33[31m'

# which subsystem do we want to monitor / analyze?
# default = USB
subsys = "usb"

# get current date and time for naming log file
timestamp = datetime.datetime.now()

# devices list
devices = [None]

# which mode are we running the program in
DEV_MODE = 1
USR_MODE = 2
# default is user mode unless parameter is passed to program
mode = USR_MODE

if(len(sys.argv) == 2):
	if (sys.argv[1] == "dev"):
		print(CGREEN + "Running in dev mode, no log file created" + CRESET)
		mode = DEV_MODE
	else:
		print("usage: python egadd.py [dev]")
		sys.exit()

# only log the devices if the program is being run in user mode (USR_MODE)
def log_devices():
	# create a file with the format {YEAR} {MONTH} {DAY} {HOUR} {MINUTE} {SECOND}
	file_name = timestamp.strftime("logs/[%Y-%m-%d]-[%H-%M-%s]")
	print("Logging udev in file: {}".format(file_name))
	file = open(file_name, "w+")
	for device in devices:
		file.write(str(device) + "\n")
	file.close()
	return

def udev_connect():
	# establish a connection to the udev device database
	context = pyudev.Context()
	
	# list the devices in the usb subsystem
	for device in context.list_devices(subsystem=subsys):
		devices.append(device)
		if mode == DEV_MODE:
			print('{0} ({1})' .format(device, device.device_type))
                        #print('{0}'.format(device.device_type))
	return

	
if __name__ == "__main__":
	udev_connect()
	if mode == USR_MODE:
		log_devices()
