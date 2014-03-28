---
title:  How to add user info 
layout: simple_page 
---

To add user info, please first read the [/site-development].

MyHDL users can add their info under the `/users` directory.  If a single page
is sufficient, put the info in a `<username>.md` file. Otherwise, create a
directory `<username>` and add an `index.md` and other pages there. 
In the latter case, use `index.md` as the main entry point
for your info, it works best for nice urls.

File and directory names map to urls, so avoid whitespace and use
all lowercase names.

There are some placeholder files and directories to show how it works. You can
start by picking a placeholder and rename it. 

A typical layout for your content pages would be `article`. If you don't need a
sidebar, use `simple_article`. If you need a wider area for the text, use
`wide_article`.

Be sure to add the page or folder name as a list item entry in the `content`
field of the `users/index`.
