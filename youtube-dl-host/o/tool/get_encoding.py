#!/usr/bin/env python
# -*- coding: utf-8 -*-
# get_encoding.py for lieying_plugin/you-get (parse)
# get stdout and stderr encoding for systems not support utf-8 well
# version 0.0.1.0 test201507151539

# import
import sys
import json

# function
def main():
    # get encodings
    stdout_encoding = sys.stdout.encoding
    stderr_encoding = sys.stderr.encoding
    # output info
    out = {}
    out['stdout'] = stdout_encoding
    out['stderr'] = stderr_encoding
    # done
    text = json.dumps(out)
    print(text)

# start from main
if __name__ == '__main__':
    main()

# end get_encoding.py


