#!/usr/bin/python3

# This python file will handle device caching

from egadd import get_devices

# action is used to perform certain things inside this function
# 1 = set the cache
# 2 = check the cache
def cache_func(action):

    cache_list = []
    ####### using encapsulation to make these functions private #######

    ### invalidate_cache ###
    # This function invalidates the cache
    def invalidate_cache():
        print("nothng here yet")

    ### set_cache ###
    # This function iniatially sets the cache
    def set_cache():
        #get_devices() will set the cache list
        print("nothng here yet")

    ### check_cache ###
    # This function checks the cache
    def check_cache():
        print("nothng here yet")


#####################################
    if action == 1:
        print("Gonna set the cache now!")
        #set_cache() #this will run a special instance of get_devices()
    if action == 2:
        print("Gonna check the cache now!")
