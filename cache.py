#!/usr/bin/python3

# This python file will handle device caching
from enum import Enum
from egadd import get_devices
import time

# from cache import Cache

class Cache(Enum):

    cache_list = []
    ####### using encapsulation to make these functions private #######

    
    ### invalidate_cache ###
    # This function invalidates the cache
    def invalidate_cache(cls):
        print("im here")
        set_cache()

    ### set_cache ###
    # This function iniatially sets the cache
    def set_cache():
        global cache_list
        cache_list = get_devices(1)

    ### check_cache ###
    # This function checks the cache
    def check_cache():
        global cache_list
        temp_list = []
        for i in range(0,5):
            time.sleep(1)
            temp_list = get_devices(1)

            if temp_list != cache_list:
                print("found a difference!")
                print(temp_list)
                #invalidate_cache() 

                return


