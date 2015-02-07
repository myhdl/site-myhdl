from __future__ import unicode_literals

import re
from distutils.version import StrictVersion
import urubu

urubu_version_required = "0.3"

urubu_version_error = """\
Urubu version should be >= {}
Upgrade with: "pip install --upgrade urubu"
""".format(urubu_version_required)

if StrictVersion(urubu.__version__) < StrictVersion(urubu_version_required):
    raise AssertionError(urubu_version_error) 

undefined_key = "'{}' not defined in '{}'"

def check_keys(item, keys):
    for key in keys:    
        if key not in item:
            raise KeyError(undefined_key.format(key, item['id']))

def validate_default(item):
    pass
        
def validate_article(item):
    pass

status_error = "Invalid status '{}' in '{}'"
defined_statusses = ('Draft', 'Final', 'Rejected', 'Replaced', 'Active')
def validate_mep(item):
    check_keys(item, ['author', 'date', 'mep'])
    if 'status' in item:
        if item['status'] not in defined_statusses:
            raise ValueError(status_error.format(item['status'], item['id']))
    else:
        item['status'] = 'Draft'

validators= {}

validators['article'] = validate_article 
validators['simple_article'] = validate_article 
for pn in ('page', 'simple_page', 'home'):
    validators[pn] = validate_default

