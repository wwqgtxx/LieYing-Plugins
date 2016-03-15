# -*- coding: utf-8 -*-
# base.py for lieying_plugin update
# o/update/base: update base utils
# version 0.0.4.0 test201507272237

# import

import os
import sys
import math
import subprocess

from . import make_zip

# global vars
ROOT_PATH = '../../'

# base function
def make_root_path():
    now_path = os.path.dirname(__file__)
    root_path = os.path.join(now_path, ROOT_PATH)
    
    return root_path

# function
def create_dom(html_text):
    return base0.create_dom(html_text)

# text function
def byte2size(size_byte, flag_add_bytes=False):
    
    unit_list = [
        'Byte', 
        'KB', 
        'MB', 
        'GB', 
        'TB', 
        'PB', 
        'EB', 
    ]
    
    # check use Byte
    if size_byte < 1024:
        size = str(size_byte) + ' Byte'
        return size
    
    # get unit
    unit_i = math.floor(math.log(size_byte, 1024))
    unit = unit_list[unit_i]
    size_n = size_byte / pow(1024, unit_i)
    
    size_t = float_len(size_n)
    
    # make final size_str
    size_str = size_t + ' ' + unit
    
    # check and add Byte
    if flag_add_bytes:
        size_str += ' (' + str(size_byte) + ' Byte)'
    # done
    return size_str

def float_len(n, l=2):
    
    f = float(n)
    t = str(f).split('.', 1)
    
    # delete chars
    while len(t[1]) > l:
        t[1] = t[1][:-1]
    
    # add zeros
    while len(t[1]) < l:
        t[1] += '0'
    
    # done
    nt = ('.').join(t)
    return nt

def zero_len(n, l=2):
    t = str(int(n))
    while len(t) < l:
        t = '0' + t
    return t


# path function

# get rel_path from now by default
def rel_path(base_path, start='.'):
    now_path = os.path.abspath(start)
    b_path = os.path.abspath(base_path)
    r_path = os.path.normpath(os.path.relpath(b_path, start=now_path))
    return r_path

# file function

# mv -R, move dir
def mv_R(old, new):
    os.renames(old, new)

# find first dir
def find_first_dir(base_path):
    
    sub_list = os.listdir(base_path)
    for s in sub_list:
        fpath = os.path.join(base_path, s)
        if os.path.isdir(fpath):
            return fpath
    return None

# remove dirs, rm -r
def rm_R(base_path):
    
    # get file list
    finfo = make_zip.gen_file_list(base_path)
    
    # remove each file
    dir_ok_count = 0
    dir_err_count = 0
    file_ok_count = 0
    file_err_count = 0
    byte_ok_count = 0
    byte_err_count = 0
    
    # remove all files
    for f in finfo['list']:
        try:
            fpath = os.path.join(base_path, f['name'])
            os.remove(fpath)
            
            # add count
            file_ok_count += 1
            byte_ok_count += f['size']
        except OSError:	# delete file failed
            # add count
            file_err_count += 1
            byte_err_count += f['size']
    # remove all dirs
    # NOTE from last to first to delete
    dir_count = len(finfo['dir_list'])
    i = dir_count - 1
    while i >= 0:
        d = finfo['dir_list'][i]
        i -= 1
        try:
            fpath = os.path.join(base_path, d['name'])
            os.rmdir(fpath)
            
            # add count
            dir_ok_count += 1
        except OSError:	# remove failed
            dir_err_count += 1
    # output count
    count = {}
    count['ok'] = {}
    count['err'] = {}
    count['ok']['file'] = file_ok_count
    count['ok']['dir'] = dir_ok_count
    count['ok']['byte'] = byte_ok_count
    count['err']['file'] = file_err_count
    count['err']['dir'] = dir_err_count
    count['err']['byte'] = byte_err_count
    return count
    # done

# subprocess function

def easy_run(args, shell=False):
    p = subprocess.Popen(args)
    exit_code = p.wait()
    return exit_code


# import TOO

# NOTE import base from plugin/plist
root_path = make_root_path()
sys.path.append(root_path)

from plugin.plist import base as base0

# end base.py


