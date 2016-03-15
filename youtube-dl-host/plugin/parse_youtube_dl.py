# -*- coding: utf-8 -*-
# parse_youtube_dl.py for lieying_plugin/youtube-dl (parse)
# plugin/parse_youtube_dl: parse output json info of youtube-dl
# version 0.0.3.1 test201507252051

# import
import json

# function

# base parse, parse youtube-dl output json text with option -J
def parse_raw(raw_text):
    
    # load as json
    raw = json.loads(raw_text)
    
    out = {}	# output info obj
    
    # add video info
    out['title'] = raw['title']
    out['site'] = raw['extractor']
    out['raw_url'] = raw['webpage_url']	# NOTE for DEBUG
    
    flist = {}	# formats list
    
    # NOTE check for single file video or mutile file video, FIX BUG here
    if 'entries' in raw:
        es = raw['entries']
    else:	# NOTE single file video
        es = [raw]
    
    # add video formats, process entries
    for e in es:
        # process formats
        for f in e['formats']:
            # make one item info
            one = {}
            
            one['ext'] = f['ext']
            one['size'] = f['filesize']
            one['url'] = f['url']
            one['http_headers'] = f['http_headers']
            
            f_id = f['format_id']
            f_format = f['format']
            
            # add one item
            if not f_id in flist:
                # create one format video
                v = {}
                
                v['f'] = f_id
                v['format'] = f_format
                v['file'] = []
                
                flist[f_id] = v
            # just add this file
            flist[f_id]['file'].append(one)
    # add formats and file info done
    
    # sort formats by h1, h2, ...
    flist2 = []
    for f in flist:
        flist2.append(flist[f])
    flist2.sort(key=lambda x: x['f'], reverse=False)
    
    out['video'] = flist2
    # done
    return out

# end parse_youtube_dl.py


