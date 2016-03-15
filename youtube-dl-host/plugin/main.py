# -*- coding: utf-8 -*-
# main.py for lieying_plugin/youtube-dl (parse)
# plugin/main: plugin main file. 
# version 0.0.11.1 test201507231058

# import

import json

from . import version
from . import filter as filter0

from . import conf
from . import tinfo
from . import run_sub
from . import cache

from .plist import entry as plist
from .easy import host_make_name

from . import parse_youtube_dl as parse0

# global vars
_PLUGIN_YOUTUBE_DL_FORCE_URL = 'youtube-dl::'

# function

# parse more video
def parse_more(url):
    # parse video list
    vlist = plist.parse_video_list(url)
    
    # make output info
    out = {}
    out['type'] = 'list'
    out['more'] = False
    
    # add title
    out['title'] = vlist['title'] + '_' + vlist['site_name']
    
    # add data, video items, add each item
    out['data'] = []
    for i in range(len(vlist['list'])):
        raw = vlist['list'][i]
        one = {}
        out['data'].append(one)
        
        one['url'] = raw['url']
        one['no'] = raw['no']
        one['subtitle'] = raw['subtitle']
        
        # make name
        name = host_make_name.make_title(
        			title=vlist['title'] + raw['no'], 
        			title_sub=raw['subtitle'], 
        			title_no=(i + 1), 
        			title_short=vlist['title'], 
        			site_name=vlist['site_name'])
        # make name done
        one['name'] = name
    # add items done
    
    out['total'] = len(out['data'])
    # done
    return out

# parse one video
def parse_one(url):
    
    # get encoding first
    get_encoding()
    
    # run youtube-dl with -J option, output single json text
    stdout, stderr = run_sub.run_youtube_dl(['-J', url])
    
    # try to parse raw_text
    try:
        raw_info = parse0.parse_raw(stdout)
    except Exception as e:	# output error
        raise make_error('parse_youtube_dl.parse_raw()', stderr, stdout, e)
    
    # NOTE store raw_info in once cache
    cache.set_cache(url, raw_info)
    
    # try to translate info
    try:
        out = tinfo.t_format(raw_info)
    except Exception as e:	# output error
        raise make_error('tinfo.t_format()', stderr, stdout, e)
    
    # done
    return out

# get encoding
def get_encoding():
    
    # load config first
    conf.load()
    
    # check got_encoding
    if conf.etc['flag_got_encoding']:
        return True	# not get once again
    
    # run tool to get encoding
    etc = conf.etc
    arg = [etc['py_bin'], etc['get_encoding_bin']]
    stdout, stderr = run_sub.run(arg)
    
    raw = stdout.decode('utf-8')
    info = json.loads(raw)
    
    # update info
    etc['encoding']['stdout'] = info['stdout']
    etc['encoding']['stderr'] = info['stderr']
    
    # set flag
    etc['flag_got_encoding'] = True
    # done
    return False

# process youtube-dl force URL, youtube-dl::
def check_force_url(input_text):
    force = _PLUGIN_YOUTUBE_DL_FORCE_URL
    if input_text.startswith(force):
        return input_text.split(force, 1)[1]
    return input_text

# lieying_plugin functions

def lieying_plugin_GetVersion():
    
    # NOTE get encoding first
    get_encoding()
    
    out = {}	# output info obj
    
    out['port_version'] = version.LIEYING_PLUGIN_PORT_VERSION
    out['type'] = version.LIEYING_PLUGIN_TYPE
    out['uuid'] = version.LIEYING_PLUGIN_UUID
    out['version'] = version.LIEYING_PLUGIN_VERSION
    
    out['name'] = version.make_plugin_name()
    out['filter'] = filter0.get_filter()
    
    out['author'] = version.THIS_AUTHOR
    out['license'] = version.THIS_LICENSE
    out['home'] = version.THIS_HOME
    out['note'] = version.THIS_NOTE
    
    # self define info
    out['pack_version'] = version.THIS_PACK_VERSION
    
    # done
    text = json.dumps(out)
    return text

def lieying_plugin_StartConfig():
    raise Exception('lieying_plugin/youtube-dl: ERROR: [StartConfig()] not support config now. ')

def lieying_plugin_Parse(input_text):
    input_text = check_force_url(input_text)
    # check is video list
    if plist.check_is_list_url(input_text):
        info = parse_more(input_text)
    else:	# should use parse_one
        info = parse_one(input_text)
    # done
    text = json.dumps(info)
    return text

def lieying_plugin_ParseURL(url, label, i_min=None, i_max=None):
    
    # NOTE now just ignore i_min, i_max TODO
    
    # process force url youtube-dl::
    url = check_force_url(url)
    
    # NOTE check if cached
    if not cache.check_cached(url):
        
        # NOTE get encoding first
        get_encoding()
        
        # run youtube-dl with -J option, output single json text
        stdout, stderr = run_sub.run_youtube_dl(['-J', url])
        
        # try to parse raw_text
        try:
            raw_info = parse0.parse_raw(stdout)
        except Exception as e:	# output error
            raise make_error('parse_youtube_dl.parse_raw()', stderr, stdout, e)
    else:	# NOTE just get raw_info from cache
        raw_info = cache.get_cache(url)
        # check failed
        if raw_info == None:
            raise Exception('plugin.main: ERROR: cache error, key [' + url + '], data ' + str(raw_info) + ' ', url, raw_info)
    
    # try to translate info
    try:
        out = tinfo.t_url(raw_info, label)
    except Exception as e:	# output error
        raise make_error('tinfo.t_url()', stderr, stdout, e)
    
    # done
    text = json.dumps(out)
    return text

# make error for youtube-dl error, for raise
def make_error(fun_name='unknow', stderr='', stdout='', e=None):
    # make err_text
    err_text = 'plugin.main: ERROR: ['
    err_text += fun_name
    err_text += '] youtube-dl may get errors \n'
    err_text += str(e) + '\n'
    err_text += ' youtube-dl output \n' + stderr + '\n' + stdout + '\n'
    # make Exception obj
    err = Exception(err_text, stderr, stdout, e)
    return err

# end main.py


