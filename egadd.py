#!/usr/bin/python3
import sys
import datetime		# log files will be named with current date/time
import subprocess	# execute the bash script 
import time 		# used to sleep get_devices()
import json 		# used to store devices

# usage: python egadd.py [dev]
# 	dev: run in dev mode, for testing purposes only & no log file is created

# COLOR CODES
CRESET = '\33[0m'
CGREEN = '\33[32m'
CRED   = '\33[31m'

# which subsystem do we want to monitor / analyze?
# default = USB
subsys = "usb"
# stores and imports settings
settings_dict = {}

# devices list (need to change this dictionary)
device_list = []

# list of default machine devices
hardware_list = []

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
	file_name = datetime.datetime.now().strftime("logs/%Y-%m-%d")
	curr_time = datetime.datetime.now().strftime("%H:%M:%S")
	
	print("Logging devices in file: {} @ {}".format(file_name, curr_time))
	file = open(file_name, "a+")
	file.write("-----" + curr_time + "-----" + "\n")

	# If there are no devices currently plugged into the machine
	if not device_list:
		file.write(str("No devices!\n"))
	else: 
		for device in device_list:
			file.write(str(device) + "\n")
	file.close()
	return


def set_hardware_devices():

	time.sleep(1.5)
	# execute our poltergust3000 script and pipe the results into the devices variable
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
	global hardware_list

	for dev in split_devs:
		if dev != "":
			#line format is $ID_SERIAL|$ID_PATH_TAG|$ID_TYPE
			dev_info = dev.split("|")
			hardware_list.append(dev)
	
	hardware_list = list(set(hardware_list))
	with open('data/hardware.json', 'w') as outfile:
		json.dump(hardware_list, outfile, indent=4)
	
	hardware_list = []

def get_hardware_devices():
	global hardware_list
	try:
		with open('data/hardware.json') as data:
			hardware_list = json.load(data)
	except:
		print("Error opening hardware.json!")

	#print(hardware_list)

# get the devices with the bash script poltergust3000
# 	action:		if the device was removed or added, provided by parascope.py
#				if egadd is ran alone, it will be the mode
def get_devices(cache=0):

	#time.sleep(1.5)
	# execute our poltergust3000 script and pipe the results into the devices variable
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
	global hardware_list

	#clearing the list on every call
	device_list = []
	for dev in split_devs:
		if dev != "":
			#line format is $ID_SERIAL|$ID_PATH_TAG|$ID_TYPE
			dev_info = dev.split("|")
			
			# only append the action if it's coming from the parascope.py script
			if dev not in hardware_list:
				device_list.append(dev)

	
	# make sure all devices are distinct
	device_list = list(set(device_list))

	if not cache:
		log_devices()
	else:
		return device_list

	return	

if __name__ == "__main__":
	# pass in the mode if egadd is being run alone
	get_devices()


