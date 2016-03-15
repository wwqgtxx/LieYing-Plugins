# -*- coding: utf-8 -*-
# base.py for lieying_plugin (parse) plist
# plugin/plist/base: parse video plist base utils
# version 0.0.1.0 test201507251729

# import

import urllib.request

from ..tool.htmldom import htmldom

# function

# network function
def http_get(url):
    
    # make header
    header = {}
    header['Connection'] = 'close'
    
    req = urllib.request.Request(url, headers=header)
    res = urllib.request.urlopen(req)
    
    data = res.read()
    # just decode as utf-8
    t = data.decode('utf-8', 'ignore')
    # done
    return t

# html parse function
def create_dom(html_text):
    dom = htmldom.HtmlDom()
    root = dom.createDom(html_text)
    return root

# end base.py


