---
title:   Installation 
layout:  article
---

Installation using pip
======================

You can install MyHDL using pip: 

```
pip install myhdl 
```

To upgrade an existing installation to the
latest version, use:

```
pip install --upgrade myhdl 
```

If pip is not yet available on your system, follow the [pip installation
instructions][pip_install].

[pip_install]: http://www.pip-installer.org/en/latest/installing.html

You may want to install MyHDL in an isolated environment using [virtualenv].


Installation using distutils
============================

MyHDL uses the standard Python [distutils] package for distribution and
installation. This page contains detailed instructions for installing MyHDL on
a typical Linux or Unix system. For other platforms, you have to follow an
equivalent procedure. Remember that MyHDL can be installed on any platform that
supports Python. For more information about installing on non-Linux platforms
such as Windows, read about [Installing Python
Modules](http://docs.python.org/inst/standard-install.html ).

[distutils]: http://docs.python.org/2/library/distutils.html

To install MyHDL on your system,
[download](http://sourceforge.net/project/showfiles.php?group_id=91207) the
latest release. Untar and unzip the downloaded file:

    > tar xvf myhdl-0.8.tar.gz
    > gunzip myhdl-0.8.tar

Go into the release directory:

    > cd myhdl-0.8

If you have superuser power, you can install MyHDL as follows:

    > python setup.py install

This will install the package in the appropriate site-wide Python
package location.  

Otherwise, you can install it in a personal directory, e.g. as
follows:

    > python setup.py install --home=$HOME
 
In this case, be sure to add the appropriate install dir to the
`$PYTHONPATH`.
 
If necessary, consult the [distutils] documentation in the standard
Python library for more details.
 
You can test the proper installation as follows:

    > cd myhdl/test/core
    > python test_all.py

Co-simulation
=============

Co-simulation requires an additional installation step.
 
To install co-simulation support:
 
Go to the directory `co-simulation/<platform>` for your target platform
and following the instructions in the `README.txt` file.
 


