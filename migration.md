---
title: Migration guide 
layout: simple_page 
---

This site is being migrated from 
[myhdl.org].  This guide is intended for all those who want to
help with the migration.

The site is being migrated from a dokuwiki site to an [urubu] site. Please
consult the [urubu] website to install the software and get an overview of how
it works. As a content contributor, you don't need all the details about
templating and so on: the main task will be editing content in Markdown format.

The site is being developed on BitBucket in the [site_myhdl_repo]. The
orginal code from myhdl.org is checked in under `_ori`. There is a `convert.py`
script that can help to convert the original dokuwiki format to Markdown. It is
far from comprehensive, but should provide a good starting point.

You can contribute through pull requests, or I will consider to give you direct
access to the repository.

Publishing the content is automatic after a push, but it may take up to ten
minutes before the edits are online. The website content is pulled from
the repo, so make sure to commit the built website also.
