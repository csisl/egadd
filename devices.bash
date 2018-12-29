#!/bin/bash

#This script lists the current USB devices plugged into your machine.
for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev); do
        
	path="${sysdevpath%/dev}"
        devName="$(udevadm info -q name -p $path)"

        if [[ "$devName" == "bus/"* ]]; then
		continue
	fi

     	eval "$(udevadm info -q property --export -p $path)"
	echo $ID_SERIAL

	if [[ -z "$ID_SERIAL" ]]; then
		continue
	else
		echo "/dev/$devName - $ID_SERIAL"
		ID_SERIAL=""
	fi
done

