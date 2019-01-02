#!/usr/bin/python3
#import pyudev
import sys
import datetime		# log files will be named with current date/time
import subprocess	# execute the bash script 

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
device_list = []

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
	file_name = timestamp.strftime("logs/%Y-%m-%d_%H-%M-%S")
	print("Logging devices in file: {}".format(file_name))
	file = open(file_name, "w+")
	for device in device_list:
		file.write(str(device) + "\n")
	file.close()
	return

# get the devices with the bash script poltergust3000
def get_devices():
	try:
		# save the output to devices
		devices = subprocess.run(["./poltergust3000"], stdout=subprocess.PIPE)
	except:
		print(CRED + "Error: Unable to execute poltergust3000!" + CRESET)
		sys.exit()
	
	# decode the output 
	decoded_devs = devices.stdout.decode('utf-8')
	
	# split the results of the output by new-line char
	split_devs = decoded_devs.split("\n")
	
	# for nice output to the log file, loop through the split result
	# and append the data to the device list
	global device_list
	for dev in split_devs:
		device_list.append(dev)
	
	# make sure all devices are distinct
	device_list = list(set(device_list))

	if mode == DEV_MODE:
		print("{}".format('\n'.join(device_list)))
	return	

if __name__ == "__main__":
	get_devices()
	if mode == USR_MODE:
		log_devices()


