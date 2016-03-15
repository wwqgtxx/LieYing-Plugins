# -*- coding: utf-8 -*-
# version.py for lieying_plugin/youtube-dl (parse)
# plugin/version: define info for GetVersion()
# version 0.1.8.0 test201507272313

# import
from . import conf
from . import run_sub

# global vars

THIS_PACK_VERSION = '11'

LIEYING_PLUGIN_PORT_VERSION = '0.2.1'
LIEYING_PLUGIN_TYPE = 'parse'

LIEYING_PLUGIN_UUID = '88e47809-089c-45a9-b097-5087c260588f'
LIEYING_PLUGIN_VERSION = '0.4.2'

THIS_AUTHOR = 'sceext <sceext@foxmail.com>'
THIS_LICENSE = 'unlicense <http://unlicense.org> and FreeBSD License'
THIS_HOME = 'https://github.com/sceext2/lieying_plugin/tree/plugin-youtube-dl'
THIS_NOTE = 'A lieying plugin (parse) with parse support of youtube-dl <https://github.com/rg3/youtube-dl>. '

THIS_RAW_NAME = [
    'lieying_plugin_youtube-dl ', 
    ' (plugin version ', 
    ', youtube-dl version ', 
    ') ', 
]

# function

# get youtube-dl version
def get_youtube_dl_version():
    
    try:	# run youtube-dl may get errors
        stdout, stderr = run_sub.run_youtube_dl(['--version'])
        
        # parse returned text to get youtube-dl version
        ver = stdout.split('\n', 1)[0]
    except Exception:	# just use [unknow]
        ver = '[unknow]'
    
    # done
    return ver

# make plugin name
def make_plugin_name():
    name = ''	# plugin name
    raw = THIS_RAW_NAME
    
    name += raw[0] + THIS_PACK_VERSION
    name += raw[1] + LIEYING_PLUGIN_VERSION
    name += raw[2] + get_youtube_dl_version() + raw[3]
    
    name += THIS_LICENSE
    
    # done
    return name

# end version.py


