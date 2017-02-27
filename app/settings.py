# all settings in a file
# because I don't need a local settings

import os

TEMPLATES_DIR = os.path\
    .join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
          'templates/')
