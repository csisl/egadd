#!/usr/bin/python3

# This python file will handle device caching
from egadd import get_devices
import time

cache_list = []

### invalidate_cache ###
# This function iniatially sets the cache
def invalidate_cache():
    global cache_list
    cache_list = get_devices(1)

### check_cache ###
# This function compares cache with temporary list
def check_cache():
    global cache_list
    temp_list = []

    cache_list.sort()
    temp_list.sort()

    for i in range(0,5):
        time.sleep(1)
        temp_list = get_devices(1)

        if temp_list != cache_list:
            print("found a difference!")
            print(temp_list)
            invalidate_cache()
            return
    return


