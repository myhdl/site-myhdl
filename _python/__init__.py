from .filters import filters

from distutils.version import StrictVersion
import urubu

urubu_version_required = "1.2"

urubu_version_error = """\
Urubu version should be >= {}
Upgrade with: "pip install --upgrade urubu"
""".format(urubu_version_required)

if StrictVersion(urubu.__version__) < StrictVersion(urubu_version_required):
    raise AssertionError(urubu_version_error) 
