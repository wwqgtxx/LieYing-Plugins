# -*- coding: utf-8 -*-
# list271.py for lieying_plugin (parse) plist
# plugin/plist/site/list271: parse video list of 271. 
# version 0.0.10.0 test201507251808

# import

import re
import json

from .. import base

# global vars

RE_GET_AID = ' albumId: ([0-9]+),'	# albumId: 202340701,
# http://cache.video.qiyi.com/jp/avlist/202340701/2/
URL_JS_API_PORT = 'http://cache.video.qiyi.com/jp/avlist/'

# function

# plist entry function
def get_list_info(html_text, raw_url=None):
    # get info from web page html
    info = get_info_from_html(html_text)
    # get info from js API port
    info2 = get_info_from_js_port(html_text)
    
    # replace vlist with js port data
    vlist = []
    for i in info2:
        one = {}
        one['no'] = str(i['no'])
        one['subtitle'] = i['subtitle']
        one['url'] = i['url']
        vlist.append(one)
    # done
    info['list'] = vlist
    return info

# get info from 271 javascript API port
def get_info_from_js_port(html_text):
    # get album id
    aid = get_aid(html_text)
    # get info list
    vlist = get_vinfo_list(aid)
    # done
    return vlist

# get album id
def get_aid(html_text):
    m = re.findall(RE_GET_AID, html_text)
    return m[0]

# make js API port URL
def make_port_url(aid, page_n):
    url = URL_JS_API_PORT + str(aid) + '/' + str(page_n) + '/'
    return url

# get vinfo list, get full list from js API port
def get_vinfo_list(aid):
    vlist = []
    # request each page
    page_n = 0
    while True:
        # make request url
        page_n += 1
        url = make_port_url(aid, page_n)
        # get text
        raw_text = base.http_get(url)
        # get list
        sub_list = parse_one_page(raw_text)
        if len(sub_list) > 0:
            vlist += sub_list
        else:	# no more data
            break
    # get full vinfo list done
    return vlist

# parse one page info, parse raw info
def parse_one_page(raw_text):
    # remove 'var tvInfoJs={' before json text, and json just ended with '}'
    json_text = '{' + raw_text.split('{', 1)[1]
    # load as json text
    info = json.loads(json_text)
    
    # check code, '"code":"A00000"' is OK, and '"code":"A00004"' is out of index
    if info['code'] == 'A00004':
        return []	# just return null result
    
    # get and parse video info items
    vlist = info['data']['vlist']
    out = []	# output info
    for v in vlist:
        one = {}
        
        one['no'] = v['pd']
        one['title'] = v['vn']
        one['subtitle'] = v['vt']
        one['url'] = v['vurl']
        
        # get more info
        one['vid'] = v['vid']
        one['time_s'] = v['timeLength']
        one['tvid'] = v['id']
        
        out.append(one)
    # get video info done
    return out


# NOTE a old and bad method, just reserved
# get info from page html
def get_info_from_html(html_text):
    # parse html_text with htmldom
    root = base.create_dom(html_text)
    
    # get block
    blocks = root.find('ul.site-piclist[data-albumlist-elem=cont]')
    block = blocks[0]
    
    # get some list
    a_list = block.find('a.site-piclist_pic_link')
    url_list = []
    title_list = []
    for a in a_list:
        url_list.append(a.attr('href'))
        title_list.append(a.attr('title'))
    
    ns = block.find('p.site-piclist_info_title>a')
    
    # NOTE fix ns here
    ns = ns[::2]
    
    n_list = []
    for n in ns:
        n_list.append(n.text())
    
    # get album name
    album_a = root.find('div.crumb-item a')
    album_name = album_a[-1].text()
    
    # make output info obj
    info = {}
    info['list'] = []
    for i in range(len(url_list)):
        one = {}
        info['list'].append(one)
        
        one['url'] = url_list[i]
        one['subtitle'] = title_list[i]
        one['no'] = n_list[i]
    
    # add album_name
    info['title'] = album_name
    
    # clean album_name
    while info['title'][-1] in '\r\n':
        info['title'] = info['title'][:-1]
    # add site name
    info['site_name'] = '不可说'
    
    # done
    return info

# end list271.py


