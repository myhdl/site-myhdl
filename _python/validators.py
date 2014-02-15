import re
from distutils.version import StrictVersion
import urubu

urubu_version_required = "0.2.1"

urubu_version_error = """\
Urubu version should be >= {}
Upgrade with: "pip install --upgrade urubu"
""".format(urubu_version_required)

if StrictVersion(urubu.__version__) < StrictVersion(urubu_version_required):
    raise AssertionError(urubu_version_error) 

hglib_import_error = """\
The layout validators for this site require hglib.
Install with: "pip install python-hglib"
"""

undefined_key = "'{}' not defined in '{}'"

# avoid raising ImportError as Urubu uses this to
# detect the _python module or package
try:
    import hglib
except ImportError:
    raise AssertionError(hglib_import_error)

def check_keys(item, keys):
    for key in keys:    
        if key not in item:
            raise KeyError(undefined_key.format(key, item['id']))

mailinfo = re.compile(r'<.*>') 

# open hg interface
hg = hglib.open('.')

def infer_lastedit(item):
    fn = item['fn']
    log = hg.log(files=[fn], limit=1)
    # keep 'lastedit' undefined if no log info
    if log:
        log = log[0]
        # convert date to readable format
        dateformat="%d-%b-%Y"
        date = log.date.strftime(dateformat)
        # remove mailinfo from author info
        author = mailinfo.sub('', log.author).strip() 
        item['lastedit'] = "Last edit on {} by {}".format(date, author)

def validate_default(item):
    infer_lastedit(item)
        
def validate_article(item):
    # check_keys(item, ['date'])
    infer_lastedit(item)

status_error = "Invalid status '{}' in '{}'"
defined_statusses = ('Draft', 'Final', 'Rejected', 'Replaced', 'Active')
def validate_mep(item):
    check_keys(item, ['author', 'date', 'mep'])
    infer_lastedit(item)
    if 'status' in item:
        if item['status'] not in defined_statusses:
            raise ValueError(status_error.format(item['status'], item['id']))
    else:
        item['status'] = 'Draft'

validators= {}

validators['article'] = validate_article 
validators['mep'] = validate_mep
for pn in ('page', 'simple_page'):
    validators[pn] = validate_default

