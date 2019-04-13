#!/usr/bin/python3
import sys
import datetime		
import subprocess	 
import time 		
import json 		
import argparse


CRESET = '\33[0m'
CGREEN = '\33[32m'
CRED   = '\33[31m'

# which subsystem do we want to monitor / analyze?
subsys = "usb"

settings_dict = {}

# devices list (need to change this dictionary)
device_list = []

# list of default machine devices
hardware_list = []

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

	try:
		devices = subprocess.run(["./poltergust3000"], stdout=subprocess.PIPE)
	except:
		print(CRED + "Error: Unable to execute poltergust3000!" + CRESET)
		sys.exit()
	
	decoded_devs = devices.stdout.decode('utf-8')
	
	split_devs = decoded_devs.split("\n")
	
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

	if debug: print(hardware_list)

	return

def get_devices(cache=0):

	try:
		devices = subprocess.run(["./poltergust3000"], stdout=subprocess.PIPE)
	except:
		print(CRED + "Error: Unable to execute poltergust3000!" + CRESET)
		sys.exit()
	
	decoded_devs = devices.stdout.decode('utf-8')
	
	# split the results of the output by new-line char
	split_devs = decoded_devs.split("\n")
	
	global device_list
	global hardware_list

	device_list = []
	for dev in split_devs:
		if dev != "":
			#line format is $ID_SERIAL|$ID_PATH_TAG|$ID_TYPE
			dev_info = dev.split("|")
			
			# only append the action if it's coming from the parascope.py script
			if dev not in hardware_list:
				device_list.append(dev)

	device_list = list(set(device_list))

	if not cache:
		log_devices()
	else:
		return device_list

	return	

if __name__ == "__main__":

	global debug
	global DEV_MODE
	debug = False
	DEV_MODE = False

	parser = argparse.ArgumentParser(description='USB port logger')

	parser.add_argument("-dev", action="store_true",
			help="Run egadd in dev mode and don't log results to a file")
	parser.add_argument("-d", "--debug", action="store_true",
			help="Run egadd in debug mode")

	args = parser.parse_args()

	if args.dev:
		print("Running in dev mode")
		DEV_MODE = True
	if args.debug:
		print("Running with debug on")
		debug = True

	get_devices()

