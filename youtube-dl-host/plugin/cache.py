# -*- coding: utf-8 -*-
# cache.py for lieying_plugin/youtube-dl (parse)
# plugin/cache: once cache for youtube-dl parse result, to speed up ParseURL(). 
# version 0.0.1.0 test201507230939

# TODO auto clean cache after given time

# import

# global vars
_cache_list = {}	# where cache data stored

# function

def check_cached(key):
    return key in _cache_list

def set_cache(key, data=None):
    # just store the data
    _cache_list[key] = data
    # done

def get_cache(key):
    # return cache data or none, and then clean it only after once get
    try:
        return _cache_list.pop(key)
    except KeyError:
        return None

# end cache.py


