---
title: Site info 
layout: page 
---

<strong>MIGRATION GUIDE</strong>
================================

This site is work in progress. It is being migrated from 
[myhdl.org].  This guide is intended for all those who want to
help with the migration.

The site is being migrated from a dokuwiki site to an [urubu] site. Please
consult the [urubu] website to install the software and get an overview of how
it works. As a content contributor, you don't need all the details about
templating and so on: the main task will be editing content in Markdown format.

The site is being developed on BitBucket in the [site-myhdl-repo]. The
orginal code from myhdl.org is checked in under `_ori`. There is a `convert.py`
script that can help to convert the original dokuwiki format to Markdown. It is
far from comprehensive, but should provide a good starting point.

You can contribute through pull requests, or I will consider to give you direct
access to the repository.

Publishing the content is automatic after a push, but it may take up to ten
minutes before the edits are online. The website content is pulled from
the repo, so make sure to commit the built website also.

Purpose
=======

The [myhdl.org] website aims to document all aspects of the development
process of the MyHDL project. MyHDL is a Python library to use
Python as a HDL. The main projects website is [here][myhdl]. 

*[HDL]: Hardware Description Language 

Website development
===================

This website is developed collaboratively by the MyHDL development
community. 

It is developed with the [urubu] software, in a
[mercurial repository][site-myhdl-dev-repo] on [bitbucket].

Theme
=====

The theme of this website uses the [bootstrap] framework.  It is based on the
[Flatly][flatly] theme, provided by [bootswatch].

[flatly]:  http://bootswatch.com/flatly/

License
=======

The content on this website is licensed
under the [content_license].

[terms-of-use]
==============







