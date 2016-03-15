# -*- coding: utf-8 -*-
# make_zip.py for lieying_plugin
# o/update/make_zip: read and write zip files. 
# version 0.0.9.0 test201507272237

# import
import os
import zipfile

# function

# make file list of a given path, file list to add to the zip file
def gen_file_list(base_path):
    
    # get raw_list
    raw_list, dir_list = gen_file_list_base(base_path)
    # count something
    
    count_size = 0
    for f in raw_list:
        count_size += f['size']
        # remove base_path in file name
        f['name'] = os.path.relpath(f['name'], base_path)
    # make output info
    out = {}
    out['list'] = raw_list
    out['count'] = len(raw_list)
    out['size'] = count_size
    # remove dir_list base_path like raw_list
    for d in dir_list:
        d['name'] = os.path.relpath(d['name'], base_path)
    out['dir_list'] = dir_list
    out['dir_count'] = len(dir_list)
    # done
    return out

def gen_file_list_base(base_path):
    out = []
    dir_list = []
    if not os.path.isdir(base_path):
        return out, dir_list
    # list sub
    sub_list = os.listdir(base_path)
    for s in sub_list:
        fpath = os.path.join(base_path, s)
        if os.path.islink(fpath):
            continue	# ignore link files
        elif os.path.isfile(fpath):
            # get file info and add this
            fsize = os.path.getsize(fpath)
            
            one = {}
            one['name'] = fpath
            one['size'] = fsize
            
            out.append(one)
        elif os.path.isdir(fpath):
            # add it to dir_list
            one = {}
            one['name'] = fpath
            
            dir_list.append(one)
            
            # re-call gen_file_list_base to get sub info
            sub_info, sub_dir = gen_file_list_base(fpath)
            out += sub_info
            dir_list += sub_dir
    # process get list all sub info done
    return out, dir_list

# add files of a list to a zip file
def make_zip_file(output_file, file_list=[], base_path='.', compress=zipfile.ZIP_DEFLATED, mode='w', path_before=None):
    
    with zipfile.ZipFile(output_file, mode=mode, compression=compress, allowZip64=True) as z:
        for f in file_list:
            fpath = os.path.join(base_path, f['name'])
            # check and add path_before
            to_path = f['name']
            if path_before and (path_before != None) and (path_before != ''):
                to_path = os.path.join(path_before, to_path)
            z.write(fpath, arcname=to_path)
    # create zip file done

# get file list in a zip file
def get_file_list(zip_file):
    out = {}
    out['list'] = []
    flist = out['list']
    
    count_size = 0
    count_zsize = 0
    
    with zipfile.ZipFile(zip_file) as z:
        ilist = z.infolist()	# info list
        for i in ilist:
            one = {}
            # file name
            one['name'] = i.filename
            # file size
            one['size'] = i.file_size
            # compressed size
            one['zsize'] = i.compress_size
            # count size
            count_size += one['size']
            count_zsize += one['zsize']
            
            flist.append(one)
    # get file list done
    out['count'] = len(flist)
    out['size'] = count_size
    out['zsize'] = count_zsize
    # done
    return out

# extract a zip file to a given path with a file list
def extract_zip_file(zip_file, file_list=[], base_path='.'):
    
    with zipfile.ZipFile(zip_file) as z:
        for f in file_list:
            z.extract(f['name'], path=base_path)
    # extract zip file done

# end make_zip.py


