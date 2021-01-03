
# Strings and Texts Part 1
# =-=-=-=-=-=-=-=-=-=-=-=-=


# 1) Splittings Strings on Any of Multiple Delimiters, line 15
# 2) Matching Text at the Start or End of a String, line 87
# 3) Matching Strings using Shell Wildcard Patterns, line 208
# 4) Matching and Searching for Text Patterns, line 299


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


# This works, but is often overkill for simple matching. Using the examples
# above is simpler and runs faster.

# Last, but not least, the startswith() and endswith() methods look nice
# when combined with other operations, such as common data reductions. For
# example, this statement that checks a directory for the presence of
# certain kinds of files:

if any(name.endswith(('.c', '.h')) for name in listdir(dirname)):
    ...


# 3) Matching Strings using Shell Wildcard Patterns


# You want to match text using the same wildcard patterns as are commonly
# used when working in Unix shells (e.g., *.py, Dat[0-9]*.csv, etc.).

# The fnmatch module provides two functions--fnmatch() and fnmatchcase()--
# that can be used to perform such matching.


# The usage is simple:


from fnmatch import fnmatch, fnmatchcase

fnmatch('foo.txt', '*.txt')
# True

fnmatch('foo.txt', '?oo.txt')
# True

fnmatch('Dat45.csv', 'Dat[0-9]*')
# True

names = ['Dat1.csv', 'Dat2.csv', 'config.ini', 'foo.py']

[name for name in names if fnmatch(name, 'Dat*.csv')]
# ['Dat1.csv', 'Dat2.csv']


# Normally, fnmatch() matches patterns using the same case-sensitivity
# rules as the system's underlying filesystem (which varies based
# on operating system).


# For example:


# On OS X (Mac)

fnmatch('foo.txt', '*.TXT')
# False

# On Windows

fnmatch('foo.txt', '*.TXT')
# True

# If this distinction matters, use fnmatchcase() instead. It matches
# exactly based on the lower- and uppercase conventions that you supply:


fnmatchcase('foo.txt', '*.TXT')
# False


# An often overlooked feature of these functions is their potential use
# with data processing of nonfilename strings. For example, suppose you
# have a list of street addresses like this:


addresses = [
    '5412 N CLARK ST',
    '1060 W ADDISON ST',
    '1039 W GRANVILLE AVE',
    '2122 N CLARK ST',
    '4802 N BROADWAY',
]


# You could write list comprehensions like this:


from fnmatch import fnmatchcase

[addr for addr in addresses if fnmatchcase(addr, '* ST')]
# ['5412 N CLARK ST', '1060 W ADDISON ST', '2122 N CLARK ST']

[addr for addr in addresses if fnmatchcase(addr, '54[0-9][0-9] *CLARK*')]


# The matching performed by fnmatch sits somewhere between the
# functionality of simple string methods and the full power of regular
# expressions. If you're just trying to provide a simple mechanism for
# allowing wildcards in data processing operations, it's often a reasonable
# solution.

# If you're actually trying to write code that matches filenames, use the
# glob module instead.


# 4) Matching and Searching for Text Patterns


# You want to match or search text for a specific pattern.

# If the text you're trying to match is a simple literal, you can often
# just use the basic string methods, such as str.find(), str.endswith(),
# str.startswith(), or similar.


# For example:


text = 'yeah, but no, but yeah, but no, but yeah'

# Exact match

text == 'yeah'
# False

# Match at start or end

text.startswith('yeah')
# True

text.endswith('no')
# False

# Search for the location of the first occurrence

text.find('no')
# 10


# For more complicated matching, use regular expressions and the re module.
# To illustrate the basic mechanics of using regular expressions, suppose
# you want to match dates specified as digits, such as "11/27/2012." Here
# is a sample of how you would do it:


text1 = '11/27/2012'
text2 = 'Nov 27, 2012'

import re
# Simple matching: \d+ means match one or more digits

if re.match(r'\d+/\d+/\d+', text1):
    print('yes')
else:
    print('no')

# yes

if re.match(r'\d+/\d+/\d+', text2)
    print('yes')
else:
    print('no')

# no


# If you're going to perform a lot of matches using the same pattern, it
# usually pays to precompile the regular expression pattern into a pattern
# object first.


# For example:


datepat = re.compile(r'\d+/\d+/\d+')
if datepat.match(text1):
    print('yes')
else:
    print('no')

# yes

if datepat.match(text2)
    print('yes')
else:
    print('no')

# no


# match() always tries to find the match at the start of a string. If you
# want to search text for all occurrences of a pattern, use the findall()
# method instead. For example:


text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'

datepat.findall(text)
# ['11/27/2012', '3/13/2013']


# When defining regular expressions, it is common to introduce capture
# groups by enclosing parts of the pattern in parentheses.


# For example:


datepat = re.compile(r'(\d+)/(\d+)/(\d+)')


# Capture groups often simplify subsequent processing of the matched text
# because the contents of each group can be extracted individually.


# For example:


m = datepat.match('11/27/2012')

m
# <_sre.SRE_Match object at 0x1005d2750>

# Extract the contents of each group
m.group(0)
# '11/27/2012'

m.group(1)
# '11'

m.group(2)
# '27'

m.group(3)
# '2012'

m.groups()
# ('11', '27', '2012')

month, day, year = m.groups()


# Find all matches (notice splitting into tuples)

text
# 'Today is 11/27/2012. PyCon start 3/13/2013.'

datepat.findall(text)
[('11', '27', '2012'), ('3', '13', '2013')]

for month, day, year in datepat.findall(text):
    print('{}-{}-{}'.format(year, month, day))

# 2012-11-27
# 2013-3-13


# The findall() method searches the text and finds all matches, returning
# them as a list. If you want to find matches iteratively, use the
# finditer() method instead.


# For example:


for m in datepat.finditer(text):
    print(m.groups())

# ('11', '27', '2012')
# ('3', '13', '2013')


# A basic tutorial on the theory of regular expressions is beyond the scope
# of this book. However, these examples illustrate the absolute basics of
# using the re module to match and search for text. The essential
# functionality is first compiling a pattern using re.compile() and then
# using methods such as match(), findall(), or finditer().

# When specifying patterns, it is relatively common to use raw strings such
# as r'(\d+)/(\d+)/(\d+)'. Such strings leave the backslash character
# uninterpreted, which can be useful in the context of regular expressions.
# Otherwise, you need to use double backslashes such as
# '(\\d+)/(\\d+)/(\\d+)'.

# Be aware that the match() method only checks the beginning of a string.
# It's possible that it will match things you aren't expecting.


# For example:


m = datepat.match('11/27/2012abcdef')

m
# <_sre.SRE_Match object at 0x1005d27e8>

m.group()
'11/27/2012'


# If you want an exact match, make sure the pattern includes the end-marker
# ($), as in the following:


datepat = re.compile(r'(\d+)/(\d+)/(\d+)$')
datepat.match('11/27/2012abcdef')

datepat.match('11/27/2012')
# <_sre.SRE_Match object at 0x1005d2750>


# Last, if you're just doing a simple text matching/searching operation,
# you can often skip the compilation step and use module-level functions
# in the re module instead.


# For example:


re.findall(r'(\d+)/(\d+)/(\d+)', text)
[('11', '27', '2012'), ('3', '13', '2013')]


# Be aware, though, that if you're going to perform a lot of matching or
# searching, it usually pays to compile the pattern first and use it over
# and over again. The module-level functions keep a cache of recently
# compiled patterns, so there isn't a huge performance hit, but you'll
# save a few lookups and extra processing by using your own compiled
# pattern.
