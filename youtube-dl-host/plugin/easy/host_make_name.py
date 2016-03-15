# -*- coding: utf-8 -*-
# host_make_name.py for lieying_plugin/you-get (parse)
# plugin/easy/host_make_name: make_name host. 
# version 0.0.1.0 test201507131206

# import
from . import make_name

# function
def make_title(title='', title_sub='', title_no='', title_short='', site_name=''):
    # just use make_name host to generate name
    t = make_name_host(
    		title=title, 
    		title_sub=title_sub, 
    		title_no=title_no, 
    		title_short=title_short, 
    		site_name=site_name)
    # done
    return t

# make_name host function
def make_name_host(title='', title_sub='', title_no='', title_short='', site_name=''):
    main_name = make_name.make(title, title_sub, title_no, title_short, site_name, make_name_host_num_len)
    # done
    return main_name

def make_name_host_num_len(title_no=-1, num_len=4):
    if title_no < 1:
        return ''
    else:
        return make_num_len(title_no, num_len)
    # done

# make number length
def make_num_len(n, l=4):
    t = str(n)
    while len(t) < l:
        t = '0' + t
    return t

# end host_make_name.py


