# -*- coding: utf-8 -*-
# entry.py for lieying_plugin (parse) plist
# plugin/plist/entry: parse video plist entry file. 
# version 0.0.4.0 test201507251728

# import

import re

from . import base

from .site import list271

# global vars

URL_TO_SITE_LIST = {
    '^http://www.iqiyi.com/a_.+\.html' : list271, 
}

# base functions

def get_site_module(url):
    m = None
    ulist = URL_TO_SITE_LIST
    for r in ulist:
        if re.match(r, url):
            m = ulist[r]
            break
    # done
    return m

# function

# check a input url is a list url
def check_is_list_url(url):
    rlist = URL_TO_SITE_LIST
    for r in rlist:
        if re.match(r, url):
            return True
    return False

# do parse video list
def parse_video_list(url):
    
    # get sub module
    list_entry = get_site_module(url)
    
    # load html_text
    html_text = base.http_get(url)
    # parse html_text and get info
    info = list_entry.get_list_info(html_text, url)
    
    # done
    return info

# end entry.py


