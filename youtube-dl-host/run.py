from . import convert
import subprocess
import json
import sys
import os

def GetVersion():
    return {
        'port_version' : "0.4.0",
        'type' : "parse",
        'uuid' : '8F610370-C3CF-4AD9-A657-C4D6CAEED870',
        'version' : '0.0.1',
        'name' : 'A demo Plugin base on youtube-dl',
        'home' : 'https://github.com/bjlewo/LieYing-Plugins'
        }

def Parse( url ):
    folder = os.path.split(os.path.realpath(__file__))[0] 
    p = subprocess.Popen([sys.executable,  folder + "\\main.py", url], stdout=subprocess.PIPE ) 
    blob = p.stdout.read()
    info = blob.decode('utf-8')
    all = json.loads(info)
    return convert.Convert( all )
#    return None

def ParseURL( url, label, min=None, max=None):
    return []