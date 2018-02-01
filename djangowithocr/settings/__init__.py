from .base import *

from .production import *

try:
   from djangowithocr.settings.local2 import *
except:
   pass