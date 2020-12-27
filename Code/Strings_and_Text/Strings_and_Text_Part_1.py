
# Strings and Texts Part 1
# =-=-=-=-=-=-=-=-=-=-=-=-=


# 1) Splittings Strings on Any of Multiple Delimiters, line 15
# 2) Matching Text at the Start or End of a String, line 87
# 3)
# 4)


# -------------------------------------------------------------------------


# 1) Splittings Strings on Any of Multiple Delimiters


# You need to split a string into fields, but the delimiters (and spacing
# around them) aren't consistent throughout the string.

# The split() method of string objects is really meant for very simple
# cases, and does not allow for multiple delimiters or account for possible
# whitespace around the delimiters. In cases when you need a bit more
# flexibility, use the re.split() method:


line = 'asdf fjdk; afed, fjek,asdf,          foo'
import re
re.split(r'[;,\s]\s*', line)
['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']


# The re.split() function is useful because you can specify multiple
# patterns for the separator. For example, as shown in the solution, the
# separator is either a comma (,), semicolon(;), or whitespace followed by
# any amount of extra whitespace. Whenever that pattern is found, the
# entire match becomes the delimiter between whatever fields lie on either
# side of the match. The result is a list of fields, just as with
# str.split().

# When using re.split(), you need to be a bit careful should the regular
# expression pattern involve a capture group enclosed in parentheses. If
# capture groups are used, then the matched text is also included in the
# result.


# For example, watch what happens here:


fields = re.split(r'(;|,|\s)\s*', line)

fields
# ['asdf', ' ', 'fjdk', ';', 'afed', ',', 'fjek', ',', 'asdf', ',', 'foo']


# Getting the split characters might be used in certain contexts. For
# example, maybe you need the split characters later on to reform an output
# string:


values = fields[::2]
delimiters = fields[1::2] + ['']

values
# ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

delimiters
# [' ', ';', ',', ',', ',', '']

# Reform the line using the same delimiters
''.join(v+d for v,d in zip(values, delimiters))
# 'asdf fjdk;afed,fjek,asdf,foo'


# If you don't want the separator characters in the result, but still need
# to use parentheses to group parts of the regular expression pattern, make
# sure you use a noncapture group, specified as (?:...).


# For example:


re.split(r'(?:,|;|\s)\s*', line)
# ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']


# 2) Matching Text at the Start or End of a String


# You need to check the start or end of a string for specific text
# patterns, such as filename extensions, URL schemes, and so on.

# A simple way to check the beginning or end of a string is to use the
# str.startswith() or str.endswith() methods.


# For example


filename = 'spam.txt'

filename.endswith('.txt')
# True

filename.startswith('file:')
# False

url = 'http://www.python.org'

url.startswith('http:')
# True


# If you need to check against multiple choices, simply provide a tuple of
# possibilities to startswith() or endswith():


import os
filenames = os.listdir('.')

filenames
# ['Makefile', 'foo.c', 'bar.py', 'spam.c', 'spam.h']

[name for name in filenames if name.endswith(('.c', '.h'))]
# ['foo.c', 'spam.c', 'spam.h' ]

# any(name.endswith('.py') for name in filenames)
# True


# Here is another example:


from urllib.request import urlopen

def read_data(name):
    if name.startswith(('http:', 'https:', 'ftp:')):
        return urlopen(name).read()
    else:
        with open(name) as f:
            return f.read()


# Oddly, this is one part of Python where a tuple is actually required as
# input. If you happen to have the choices specified in a list or set, just
# make sure you convert them using tuple() first.


# For example:


choices = ['http:', 'ftp:']
url = 'http://www.python.org'

url.startswith(choices)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# TypeError: startswith first arg must be str or a tuple of str, not list

url.startswith(tuple(choices))
# True


# The startswith() and endswith() methods provide a very convenient way to
# perform basic prefix and suffix checking. Similar operations can be
# performed with slices, but are far less elegant.


# For example:


filename = 'spam.txt'

filename[-4:] == '.txt'
# True

url = 'http://www.python.org'

url[:5] == 'http:' or url[:6] == 'https:' or url[:4] == 'ftp:'
# True


# You might also be inclined to use regular expressions as an alternative.


# For example:


import re
url = 'http://www.python.org'

re.match('http:|https:|ftp:', url)
# <_sre.SRE_Match object at 0x101253098>


# This works, but is often overkill for simple matching. Using this example
# is simpler and runs faster.

# Last, but not least, the startswith() and endswith() methods look nice
# when combined with other operations, such as common data reductions. For
# example, this statement that checks a directory for the presence of
# certain kinds of files:

if any(name.endswith(('.c', '.h')) for name in listdir(dirname)):
    ...
