import sys
import re

fn = sys.argv[1]

heading = re.compile(r'([^=]*).*')
code_inline = re.compile(r"''(.*?)''")
escape = re.compile(r"%%(.*?)%%")
emphasis = re.compile(r"//(.*?)//")
code = re.compile(r'<code>')
code_python = re.compile(r'<code python>')
code_myhdl = re.compile(r'<code myhdl>')
code_verilog = re.compile(r'<code verilog>')
code_vhdl = re.compile(r'<code vhdl>')
endcode = re.compile(r'</code>')
wikilink = re.compile(r'\[\[([^|]*)\]\]')
link = re.compile(r'\[\[(.*?)\|(.*?)\]\]')

def wikilinkrepl(match):
    id = match.group(1)
    id = id.replace(r':', r'/')
    return '[' + id + ']'

def linkrepl(match):
    url = match.group(1)
    text = match.group(2) 
    return '[' + text + ']' + '(' + url + ')' 

with open(fn) as f:
    print '---'
    for line in f:
        if line[:6] == '======':
            m = heading.match(line[6:])
            if m: 
                print 'title: ', m.group(1)
                print '---'
        elif line[:5] == '=====':
            m = heading.match(line[5:])
            if m: 
                h = m.group(1).strip()
                print h 
                print '=' * len(h)
        elif line[:4] == '====':
            m = heading.match(line[4:])
            if m: 
                h = m.group(1).strip()
                print h 
                print '-' * len(h)
        else:
            line = line[:-1]
            line = escape.sub(r'\1', line)
            line = emphasis.sub(r'*\1*', line)
            line = code_inline.sub(r'`\1`', line)
            line = code.sub(r'```', line)
            line = code_python.sub(r'```python', line)
            line = code_myhdl.sub(r'```python', line)
            line = code_verilog.sub(r'```verilog', line)
            line = code_vhdl.sub(r'```vhdl', line)
            line = endcode.sub(r'```', line)
            line = wikilink.sub(wikilinkrepl, line)
            line = link.sub(linkrepl, line)
            print line
