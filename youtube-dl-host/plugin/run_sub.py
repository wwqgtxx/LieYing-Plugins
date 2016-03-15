# -*- coding: utf-8 -*-
# run_sub.py for lieying_plugin/youtube-dl (parse)
# plugin/run_sub: run subprocess
# version 0.0.9.0 test201507221617

# import

import os
import sys
import subprocess

from . import conf

# function

def run(args, shell=False):
    
    PIPE = subprocess.PIPE
    
    p = subprocess.Popen(args, stdout=PIPE, stderr=PIPE, shell=shell)
    
    stdout, stderr = p.communicate()
    
    return stdout, stderr

def check_file(fpath):
    if os.path.isfile(fpath):
        return True
    return False

# run youtube_dl function
def run_youtube_dl(args):
    
    # load config
    conf.load()
    # get you_get_bin
    youtube_dl_main = conf.etc['youtube_dl_main_bin']
    # check file
    _init_file = os.path.join(youtube_dl_main, '__init__.py')
    if not check_file(_init_file):
        raise Exception('plugin.run_sub: ERROR: youtube_dl main __init__.py not exist \"' + _init_file + '\" ')
    
    # get python bin
    py_bin = conf.etc['py_bin']
    
    arg = []
    # check and add http_proxy, TODO NOTE may be not stable
    if conf.etc['http_proxy'] != None:
        arg += ['--proxy', conf.etc['http_proxy']]
    
    # process youtube_dl_main
    dir_host, dir_m = os.path.dirname(youtube_dl_main), os.path.basename(youtube_dl_main)
    
    # before change it, save now dir
    old_path = os.path.abspath(os.curdir)
    # change now dir
    os.chdir(dir_host)
    
    # make final args, NOTE use python -m here
    arg = [py_bin, '-m', dir_m] + arg + args
    
    # just run you_get
    stdout, stderr = run(arg)
    # recovery old_path
    os.chdir(old_path)
    
    # decode as text, NOTE fix encoding here
    encoding = conf.etc['encoding']
    stdout = stdout.decode(encoding['stdout'])
    stderr = stderr.decode(encoding['stderr'])
    
    # NOTE fix \r\n here
    if '\r\n' in stdout:
        stdout = stdout.replace('\r\n', '\n')
    if '\r\n' in stderr:
        stderr = stderr.replace('\r\n', '\n')
    
    # done
    return stdout, stderr

# end run_sub.py


