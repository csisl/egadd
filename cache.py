#!/usr/bin/python3

# This python file will handle device caching.
# Some machines are faster / slower than others, so caching our devices
# allows for proper confirmation of an insertion or removal. 
# There is a 5 second timeout for checking the cache. For most modern CPUs
# this should be plenty of time.

from egadd import get_devices
import time

cache_list = []

##### invalidate_cache #####
# Purpose:
#       This function resets the device cache using get_devices().
#       This is used on the initial run of parascope.py and everytime
#       a device is inserted/removed.
def invalidate_cache():
    global cache_list
    cache_list = get_devices(1)


##### check_cache #####
# Purpose:
#       This function compares the current cache to a temp list. 
#       get_devices() returns the list for the temp list. 
#       When a difference is found that means that a device was properly
#       detected or removed from the machine. 
#       Once the difference is found, invalidate_cache() is called.
def check_cache():
    global cache_list
    temp_list = []

    # sorting the list for direct comparison
    cache_list.sort()

    # 5 second time out
    for i in range(0,5):
        time.sleep(1) # 1 second pause 
        temp_list = get_devices(1)
        temp_list.sort() 

        if temp_list != cache_list:
            #print("found a difference!")
            #print(temp_list)
            invalidate_cache() #reseting the cache
            return
    # 5 second timeout occured            
    return