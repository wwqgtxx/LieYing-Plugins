# -*- coding: utf-8 -*-
# main.py for lieying_plugin
# o/update/main: plugin update function, main file
# version 0.0.11.0 test201507272237

# import

import os
import json

from . import base
from . import github
from . import make_zip

# global vars
etc = {}	# global config info

etc['conf'] = {}	# loaded from config file
etc['conf_loaded'] = False	# prevent reload flag
etc['root_path'] = ''	# plugin root path

CONFIG_FILE = 'etc/update_config.json'

PLUGIN_ROOT_PATH = '../../'
PLUGIN_UPDATE_PATH = 'o/update'

# function

# read given config file (json) and put info in etc
def load_config(fpath=CONFIG_FILE, force_reload=False):
    # check loaded flag
    if etc['conf_loaded'] and (not force_reload):
        return True	# not reload by default
    
    # add plugin root path
    now_path = os.path.dirname(__file__)
    root_path = os.path.join(now_path, PLUGIN_ROOT_PATH)
    etc['root_path'] = root_path
    
    # fpath is from plugin root_path
    conf_file = os.path.join(root_path, fpath)
    # read file
    with open(conf_file) as f:
        raw_text = f.read()
    
    # parse json
    info = json.loads(raw_text)
    # load config file done
    etc['conf'] = info
    
    # update loaded flag
    etc['conf_loaded'] = True
    # done
    return False

# network function

# check github latest commit
def check_github_latest_commit(github_page_url):
    # download page html_text
    html_text = github.easy_dl(github_page_url)
    # get latest commit str
    latest_commit = github.get_latest_commit(html_text)
    
    # get archive zip url from github page html
    zip_url = github.get_zip_url(html_text, github_page_url)
    
    # done
    return latest_commit, zip_url

# dl file
def dl_file(url, fpath):
    return github.file_dl(url, fpath)

# clean dir path
def clean_dir(base_path):
    cinfo = base.rm_R(base_path)	# count info
    cleaned_count = cinfo['ok']['file'] + cinfo['err']['file']
    real_count = cleaned_count + cinfo['ok']['dir'] + cinfo['err']['dir']
    if real_count > 0:
        t = 'update: [ OK ] clean ' + str(cleaned_count) + ' exists files from \"' + base.rel_path(base_path) + '\" \n'
        t += '      OK ' + str(cinfo['ok']['file']) + ' files, '
        t += str(cinfo['ok']['dir']) + ' dirs, '
        t += base.byte2size(cinfo['ok']['byte']) + ' \n'
        t += '  FAILED ' + str(cinfo['err']['file']) + ' files, '
        t += str(cinfo['err']['dir']) + ' dirs, '
        t += base.byte2size(cinfo['err']['byte']) + ' '
        print(t)
    else:
        print('update: INFO: no need to clean \"' + base.rel_path(base_path) + '\"')
    # done
    return real_count


# extract zip file to a path
def extract_pack(zip_file, extract_path, msg=''):
    
    print('update: INFO: extract ' + msg + ' to \"' + base.rel_path(extract_path) + '\" ')
    # get file list
    finfo = make_zip.get_file_list(zip_file)
    t = 'update: [ OK ] got file list, '
    t += str(finfo['count']) + ' files, '
    t += base.byte2size(finfo['size'], True)
    t += ' (' + base.byte2size(finfo['zsize']) + ') '
    print(t)
    
    # delete exist files
    if clean_dir(extract_path) > 0:
        clean_dir(extract_path)	# NOTE clean 2 times
    
    # do extract zip file
    make_zip.extract_zip_file(zip_file, finfo['list'], extract_path)
    print('update: [ OK ] extract zip file done')
    # done

# moving files
def mv_file(path_from, path_to):
    
    # before move, delete exist files
    if clean_dir(path_to) > 0:
        clean_dir(path_to)	# NOTE clean 2 times
    
    # NOTE before move files, delete to dir, FIX BUG on windows
    try:
        os.rmdir(path_to)
    except OSError:
        print('update: WARNING: delete dir failed \"' + path_to + '\" ')
    
    # move files
    print('update: INFO: move files from \"' + base.rel_path(path_from) + '\" to \"' + base.rel_path(path_to) + '\" ')
    base.mv_R(path_from, path_to)
    # done


# end main.py


