# -*- coding: utf-8 -*-
# filter.py for lieying_plugin/youtube-dl (parse)
# plugin/filter: define filter for GetVersion()
# version 0.0.6.0 test201507201920

# import
from . import conf

# global vars

# youtube-dl supported URLs RE, generated from youtube-dl extractor IE _VALID_URL
RE_LIST_YOUTUBE_DL_RAW = ''	# NOTE reserved here

# additional video list support by this plugin, plist
RE_LIST_PLIST = [
    '^http://www.iqiyi.com/a_.+\.html', 
]

# NOTE force to use youtube-dl to parse the URL, start with youtube-dl::
RE_FORCE = ['^youtube-dl::.*']

# function
def get_filter():
    # concat lieying_plugin filter RE list
    lieying_plugin_filter = get_youtube_dl_re() + RE_LIST_PLIST + RE_FORCE
    
    return lieying_plugin_filter

def get_youtube_dl_re():
    # load config file
    conf.load()
    
    return conf.etc['youtube_dl_re_list']

# end filter.py


