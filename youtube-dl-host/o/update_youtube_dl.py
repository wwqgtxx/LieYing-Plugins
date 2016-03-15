#!/usr/bin/env python
# -*- coding: utf-8 -*-
# update_youtube_dl.py for lieying_plugin
# o/update_youtube_dl: plugin update function, 
#     auto download youtube-dl from github and 
#     auto re-pack plugin zip bag
# version 0.0.18.0 test201507272238

# NOTE supported command line args
#	--no-pack	not pack a AUTO-PACK zip file in tmp/
#	--pack-only	not check latest commit on github and 
#			not download zip file from github
#			just pack a AUTO-PACK zip file in tmp/
#	--force		force download zip file from github
#			even if latest commit is same

# import

import os
import sys
import datetime

from update import main as update
from update import make_zip
from update import base

# global vars

PLUGIN_UPDATE_TOOL_VERSION = 'lieying_plugin update_tool version 0.0.5.1 test201507271528'

etc = {}	# global config info

# flags to support command line args
etc['flag_dl_github'] = True
etc['flag_pack_zip'] = True
etc['flag_force'] = False	# NOTE default value should be False

# function

def main():
    
    # init info
    print('update: INFO: start update youtube-dl ')
    
    # get and process command line args
    get_args()
    
    # load config file
    update.load_config()
    # process config content
    root_path = update.etc['root_path']
    conf = update.etc['conf']
    
    tmp_path = os.path.join(root_path, conf['local']['tmp_path'])
    etc['tmp_path'] = tmp_path
    
    conf_file = os.path.join(root_path, update.CONFIG_FILE)
    print('update: [ OK ] load config file \"' + base.rel_path(conf_file) + '\"')
    
    # check flags
    if etc['flag_dl_github']:
        # check latest commit
        if not check_latest_commit():
            # no need to update
            print('update: done')
            return
        
        # start real update
        zip_url = etc['g_zip_url']
        print('update: INFO: download youtube-dl zip file from \"' + zip_url + '\" ')
        
        # make zip file path
        zip_file = os.path.join(tmp_path, os.path.basename(zip_url))
        if not (zip_file.endswith('.zip')):
            zip_file += '.zip'
        # do download
        ed_byte = update.dl_file(zip_url, zip_file)
        # download info
        print('update: [ OK ] saved ' + base.byte2size(ed_byte, True) + ' to \"' + base.rel_path(zip_file) + '\"')
        
        etc['zip_file'] = zip_file
        
        # extract zip file
        extract_pack()
        # move files
        mv_file()
    # check and download from github, done
    
    # check flag
    if etc['flag_pack_zip']:
        # re-pack
        re_pack()
    
    # check flag
    if etc['flag_dl_github']:
        latest_commit_file = conf['local']['youtube_dl_latest_commit']
        latest_commit_file = os.path.join(root_path, latest_commit_file)
        g_latest_commit = etc['g_latest_commit']
        # update latest commit
        print('update: INFO: save latest commit [' + g_latest_commit + '] to \"' + base.rel_path(latest_commit_file) + '\" ')
        with open(latest_commit_file, 'w') as f:
            f.write(g_latest_commit)
    # done
    print('update: [ OK ] done. All works finished. ')

# process command line args
def get_args():
    args = sys.argv
    arg = args[1:]
    # process each arg
    rest = arg
    while len(rest) > 0:
        one = rest[0]
        rest = rest[1:]
        # check this arg
        if one == '--no-pack':
            # set global flag
            etc['flag_pack_zip'] = False
            # info
            print('update: INFO: got [' + one + '], not pack zip file. ')
        elif one == '--pack-only':
            # set flag
            etc['flag_dl_github'] = False
            # info
            print('update: INFO: got [' + one + '], not check and download from github. ')
        elif one == '--force':
            etc['flag_force'] = True
            
            print('update: INFO: got [' + one + '], ignore latest commit check result. ')
        else:	# unknow option
            print('update: WARNING: unknow option [' + one + '] ')
    # process args done


# check lastest commit
def check_latest_commit():
    print('update: INFO: checking latest commit ')
    
    conf = update.etc['conf']
    # get github latest commit
    page_url = conf['remote']['youtube_dl_home']
    
    print('update: INFO: load github page \"' + page_url + '\" ')
    g_latest_commit, g_zip_url = update.check_github_latest_commit(page_url)
    print('update: [ OK ] got latest commit [' + g_latest_commit + ']')
    
    # save g_zip_url
    etc['g_zip_url'] = g_zip_url
    
    # save latest_commit
    etc['g_latest_commit'] = g_latest_commit
    
    # get local latest commit
    l_latest_commit = ''
    local_file = conf['local']['youtube_dl_latest_commit']
    root_path = update.etc['root_path']
    fpath = os.path.join(root_path, local_file)
    try:
        with open(fpath) as f:
            l_latest_commit = f.read().split('\n')[0].split('\r')[0]
    except OSError:
        print('update: ERROR: can not open local commit info file \"' + base.rel_path(fpath) + '\" ')
        return True
    # got local latest commit
    print('update: [ OK ] local commit [' + l_latest_commit + ']')
    
    # check match
    if l_latest_commit == g_latest_commit:
        # check force flag
        if etc['flag_force']:
            print('update: INFO: ignore latest commit check result. ')
        else:
            print('update: INFO: no need to update. ')
            return False
    else:	# should update
        print('update: INFO: start real update')
    return True


# extract youtube-dl
def extract_pack():
    
    zip_file = etc['zip_file']
    conf = update.etc['conf']
    tmp_path = etc['tmp_path']
    
    # make extract path
    extract_path = os.path.join(tmp_path, conf['local']['youtube_dl_extract_path'])
    etc['extract_path'] = extract_path
    
    # extract file
    update.extract_pack(zip_file, extract_path, msg='youtube-dl')

# moving files
def mv_file():
    extract_path = etc['extract_path']
    root_path = update.etc['root_path']
    conf = update.etc['conf']
    
    # moving files
    youtube_dl_path = os.path.join(root_path, conf['local']['youtube_dl_path'])
    # got extracted youtube-dl path
    extracted_path = base.find_first_dir(extract_path)
    
    # use command move function
    update.mv_file(extracted_path, youtube_dl_path)

# re-packing plugin zip bag
def re_pack():
    
    root_path = update.etc['root_path']
    conf = update.etc['conf']
    tmp_path = conf['local']['tmp_path']
    
    # start re-pack
    print('update: INFO: start re-pack plugin zip bag file ')
    
    # get file list
    finfo = make_zip.gen_file_list(root_path)
    
    # ignore some from flist
    flist = []	# keep file list
    ilist = []	# ignored file list
    for f in finfo['list']:
        # ignore .git
        if f['name'].startswith('.git'):
            ilist.append(f)
        # ignore __pycache__
        elif '__pycache__' in f['name']:
            ilist.append(f)
        # ignore tmp path
        elif f['name'].startswith(tmp_path):
            ilist.append(f)
        else:	# should keep this file
            flist.append(f)
    # count something
    isize = 0
    fsize = 0
    for f in ilist:
        isize += f['size']
    for f in flist:
        fsize += f['size']
    # print info
    t = 'update: [ OK ] make file list done, ' + str(len(flist)) + ' files, '
    t += base.byte2size(fsize, True) + '; '
    t += 'ignored ' + str(len(ilist)) + ' files, ' + base.byte2size(isize) + '. '
    print(t)
    
    tmp_path2 = etc['tmp_path']
    # create zip file
    zip_file = conf['local']['re_pack_file'] + make_re_pack_name() + '.zip'
    zip_path = os.path.join(tmp_path2, zip_file)
    print('update: INFO: create zip file \"' + base.rel_path(zip_path) + '\" ')
    
    import zipfile
    make_zip.make_zip_file(zip_path, flist, root_path, compress=zipfile.ZIP_DEFLATED)
    
    # compress done
    print('update: [ OK ] compress files done. ')

# make auto-pack zip file name
def make_re_pack_name():
    zero_len = base.zero_len
    now = datetime.datetime.now()
    t = zero_len(now.year, 4) + '-'
    t += zero_len(now.month, 2) + '-'
    t += zero_len(now.day, 2) + '_'
    t += zero_len(now.hour, 2) + '-'
    t += zero_len(now.minute, 2) + '-'
    t += zero_len(now.second, 2)
    return t


# start from main
if __name__ == '__main__':
    main()

# end update_youtube_dl.py


