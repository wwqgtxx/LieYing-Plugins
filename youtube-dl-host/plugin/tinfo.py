# -*- coding: utf-8 -*-
# tinfo.py for lieying_plugin/youtube-dl (parse)
# plugin/tinfo: translate info to plugin output format. 
# version 0.0.4.0 test201507221715

# import
import math

# global vars

# base functions

def byte2size(size_byte):
    
    unit_list = [
        'Byte', 
        'KB', 
        'MB', 
        'GB', 
        'TB', 
        'PB', 
        'EB', 
    ]
    
    # get unit
    unit_i = math.floor(math.log(size_byte, 1024))
    unit = unit_list[unit_i]
    size_n = size_byte / pow(1024, unit_i)
    
    size_t = float_len(size_n)
    
    # make final size_str
    size_str = size_t + ' ' + unit
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

# function

# translate for Parse() one video output
def t_format(raw_info):
    
    raw = raw_info
    out = {}	# output info
    
    out['type'] = 'formats'
    out['name'] = make_title(raw)
    
    # make each format
    out['data'] = []
    for v in raw['video']:
        label, ext, size = make_label(v)
        # make this format info
        one = {}
        one['label'] = label
        
        # make size text
        one['size'] = byte2size(size)
        # check and add Bytes
        if size >= 1024:
            one['size'] += ' (' + str(size) + ' Byte)'
        # add ext
        one['ext'] = ext
        # add this format
        out['data'].append(one)
    # done
    return out

def make_title(raw):
    title = '爱奇艺' + '-' + raw['title']
    return title

def make_label(video):
    # get info
    f_id = video['f']
    format_ = video['format']
    files_n = len(video['file'])
    
    # make ext list
    ext = []
    for f in video['file']:
        if not f['ext'] in ext:
            ext.append(f['ext'])
    # use first ext
    ext_ = ext[0]
    
    # count size
    size = 0
    for f in video['file']:
        if f['size'] > 0:
            size += f['size']
    
    # make label text
    label = f_id + '_' + format_ + '_' + ext_ + '_' + str(files_n)
    return label, ext_, size

def parse_label(label):
    # get f_id from label text
    f_id = label.split('_', 1)[0]
    return f_id

# translate for ParseURL() output
def t_url(raw_info, label):
    raw = raw_info
    
    # get f_id
    f_id = parse_label(label)
    
    # select this video
    video = None
    for v in raw['video']:
        if v['f'] == f_id:
            video = v
            break
    
    # make url output
    out = []
    # process each url, just add it
    for f in video['file']:
        one = {}
        
        one['protocol'] = 'http'
        # NOTE add http_headers here
        one['args'] = f['http_headers']
        # add URL
        one['value'] = f['url']
        
        out.append(one)
    # done
    return out

# end tinfo.py


