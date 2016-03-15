#!/usr/bin/env python
# -*- coding: utf-8 -*-
# update_plugin.py for lieying_plugin update_tool
# o/update_plugin: plugin update function, 
#     auto download lieying_plugin from github and 
#     auto re-pack plugin zip bag
# version 0.0.3.0 test201507272310

# import

import os
import sys

from update import main as update
from update import make_zip
from update import base

# global vars

etc = {}	# global config info obj

BIN_UPDATE_SUB = 'o/update_youtube_dl.py'

# function

def main():
    
    # init info
    print('update: INFO: start update plugin ')
    
    # load config file
    update.load_config()
    # process config content
    root_path = update.etc['root_path']
    conf = update.etc['conf']
    
    tmp_path = os.path.join(root_path, conf['local']['tmp_path'])
    etc['tmp_path'] = tmp_path
    
    conf_file = os.path.join(root_path, update.CONFIG_FILE)
    print('update: [ OK ] load config file \"' + base.rel_path(conf_file) + '\"')
    
    # update youtube_dl first
    exit_code = update_sub()
    if exit_code != 0:
        print('update: ERROR: update sub failed. ')
        exit(1)	# exit with an error
        return True
    else:	# update youtube_dl OK
        print('update: [ OK ] update sub done. ')
    
    # do not check, just download and pack
    zip_url = conf['remote']['plugin_zip']
    print('\nupdate: INFO: download lieying_plugin zip file from \"' + zip_url + '\" ')
    
    # make zip file path
    zip_file = os.path.join(tmp_path, os.path.basename(zip_url))
    if not (zip_file.endswith('.zip')):
        zip_file += '.zip'
    # do download
    ed_byte = update.dl_file(zip_url, zip_file)
    # download info
    print('update: [ OK ] saved ' + base.byte2size(ed_byte, True) + ' to \"' + base.rel_path(zip_file) + '\"')
    
    etc['zip_file'] = zip_file
    
    # extract pack
    print('')
    extract_pack()
    # make plugin zip bag
    # TODO should auto-gen file name here
    pack_zip('lieying_plugin_youtube-dl-AUTO_PACK--.zip')
    
    # done
    print('\nupdate: done')


# run o/update_youtube_dl.py to update sub
def update_sub(bin_sub=BIN_UPDATE_SUB):
    py_bin = sys.executable
    root_path = update.etc['root_path']
    sub_bin = os.path.join(root_path, bin_sub)
    # make subprocess arg
    arg = [py_bin, sub_bin, '--no-pack']
    # info
    print('\nupdate: ---> update-sub :: run ' + str(arg) + ' \n')
    # get exit_code
    exit_code = base.easy_run(arg)
    # done
    print('update: ---> update-sub :: exit_code ' + str(exit_code) + ' ')
    return exit_code

# extract lieying_plugin zip file
def extract_pack():
    zip_file = etc['zip_file']
    conf = update.etc['conf']
    tmp_path = etc['tmp_path']
    
    # make extract path
    extract_path = os.path.join(tmp_path, conf['local']['extract_path'])
    etc['extract_path'] = extract_path
    
    # extract file
    update.extract_pack(zip_file, extract_path, msg='lieying_plugin')

# make plugin zip bag
def pack_zip(zip_file_name):
    root_path = update.etc['root_path']
    conf = update.etc['conf']
    tmp_path = etc['tmp_path']
    
    # find plugin files, and get sub path
    extract_path = etc['extract_path']
    extracted_path = base.find_first_dir(extract_path)
    sub_path0 = conf['local']['youtube_dl_path']
    sub_path = os.path.join(root_path, sub_path0)
    
    # make zip name
    zip_file = os.path.join(tmp_path, zip_file_name)
    
    print('\nupdate: INFO: start pack plugin zip file \"' + base.rel_path(zip_file) + '\" ')
    
    # add lieying_plugin files
    add_files_to_zip(zip_file, extracted_path)
    # add sub files
    add_files_to_zip(zip_file, sub_path, path_before=sub_path0, mode='a')
    
    # done
    print('update: [ OK ] create plugin zip file done. ')

# add files to zip file
def add_files_to_zip(zip_file, base_path, path_before=None, mode='w'):
    
    # get file list
    finfo = make_zip.gen_file_list(base_path)
    
    flist = finfo['list']
    # count something
    fsize = 0
    for f in flist:
        fsize += f['size']
    # print info
    print('update: add ' + str(len(flist)) + ' files, ' + base.byte2size(fsize, True) + ' from \"' + base.rel_path(base_path) + '\" ')
    
    # do create zip file
    import zipfile
    make_zip.make_zip_file(zip_file, flist, base_path, compress=zipfile.ZIP_STORED, path_before=path_before, mode=mode)
    # add files done


# start from main
if __name__ == '__main__':
    main()

# end update_plugin.py


