# -*- coding: utf-8 -*-
# run.py for lieying_plugin/you-get (parse)
# run: lieying_plugin entry file. 
# version 0.0.2.0 test201507151840

# import

import os
import sys
import json

# ready to import plugin.main
sys.path.insert(0, os.path.dirname(__file__))

from plugin import main

# exports functions for lieying_plugin port_version 0.2.0

GetVersion = main.lieying_plugin_GetVersion		# GetVersion()
# StartConfig = main.lieying_plugin_StartConfig		# StartConfig()

Parse = main.lieying_plugin_Parse		# Parse(input_text)
ParseURL = main.lieying_plugin_ParseURL		# ParseURL(url, label, i_min=None, i_max=None)

# NOTE add p() function for DEBUG
def p(o):
    print(json.dumps(json.loads(o), indent=4, sort_keys=True, ensure_ascii=False))

# end run.py


