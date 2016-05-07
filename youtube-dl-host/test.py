import sys
import json
import importlib
import tempfile
from . import run

r = run.Parse('http://www.le.com/ptv/vplay/25168450.html')
print(r)
