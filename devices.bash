#!/bin/bash

#This script lists the current USB devices plugged into your machine.

DEV_MODE=0

list_devices() 
{
	for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev); do
        
		path="${sysdevpath%/dev}"
        devName="$(udevadm info -q name -p $path)"
	
        if [[ "$devName" == "bus/"* ]]; then
			continue
		fi

     	eval "$(udevadm info -q property --export -p $path)"
		#echo $ID_SERIAL

		if [[ -z "$ID_SERIAL" ]]; then
			continue
		else
			if [ "$DEV_MODE" == 1 ];then
				echo "/dev/$devName - $ID_SERIAL"
			else
				echo "$ID_SERIAL"
			fi

			ID_SERIAL=""
		fi
	done
}

if [ $# -eq 1 ]; then
	if [ "$1" == "dev" ]; then
		DEV_MODE=1
		list_devices
	else
		echo "usage: bash devices.bash [dev]"
	fi
else
	list_devices
fi
