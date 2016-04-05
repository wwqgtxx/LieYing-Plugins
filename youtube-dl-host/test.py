import sys
import json
import importlib
import tempfile

url = 'https://test.com'

print( url[:url.find(':')] )