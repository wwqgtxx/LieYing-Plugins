# -*- coding: utf-8 -*-
# github.py for lieying_plugin
# o/update/github: gihub.com operations
# version 0.0.8.0 test201507262303

# import

import re
import os
import urllib.request

from . import base

# global vars

RE_LATEST_COMMIT = '>latest commit <span class="sha">([^<]+)</span>'
# css selector to get zip download url from github home page
SS_GET_ZIP_URL = 'div.repository-sidebar div.only-with-full-nav>a.btn'

DL_BUFFER_SIZE = 262144	# 256 KB buffer size

# function

# get latest_commit sha str from github page
def get_latest_commit(html_text):
    m = re.findall(RE_LATEST_COMMIT, html_text)
    try:
        return m[0]
    except IndexError:
        return None	# get latest commit info failed

# get zip url
def get_zip_url(html_text, base_url='https://github.com/'):
    # get raw zip url from html text
    root = base.create_dom(html_text)
    a = root.find(SS_GET_ZIP_URL)
    raw_url = a.attr('href')
    
    # add base_url
    bs = base_url.split('://', 1)
    b_url = bs[0] + '://' + bs[1].split('/', 1)[0]
    
    zip_url = b_url + raw_url
    # done
    return zip_url

# https download for github

# simple download method, just return the content as text
def easy_dl(url):
    r = urllib.request.urlopen(url)
    raw = r.read()
    text = raw.decode('utf-8', 'ignore')
    return text

# save a large file to disk
def file_dl(url, fpath, buffer_size=DL_BUFFER_SIZE):
    
    # request http res
    r = urllib.request.urlopen(url)
    # count size
    count_byte = 0
    # before open, create dir first
    dir_path = os.path.dirname(fpath)
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        pass
    # open file and write content
    with open(fpath, 'wb') as f:
        while True:
            data = r.read(buffer_size)
            if not data:
                break
            f.write(data)
            # count byte
            count_byte += len(data)
    # save file done
    return count_byte

# end github.py


