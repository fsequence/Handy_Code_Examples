
# Strings and Text Part 4
# =-=-=-=-=-=-=-=-=-=-=-=-


# 16) Reformatting Text to a Fixed Number of Columns, line 15
# 17) Handling HTML and XML Entities in Text, line 82
# 18)
# 19)


# -------------------------------------------------------------------------


# 16) Reformatting Text to a Fixed Number of Columns


# You have long strings that you want to reformat so that they fill a
# user-specified number of columns.

# Use the textwrap module to reformat text for output. For example, suppose
# you have the following long string:


s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
    the eyes, not around the eyes, don't look around the eyes, \
    look into my eyes, you're under."


# Here's how you can use the textwrap module to reformat it in various
# ways:


import textwrap

print(textwrap.fill(s, 70))
# Look into my eyes, look into my eyes, the eyes, the eyes, the eyes,
# not around the eyes, don't look around the eyes, look into my eyes,
# you're under.

print(textwrap.fill(s, 40))
# Look into my eyes, look into my eyes,
# the eyes, the eyes, the eyes, not around
# the eyes, don't look around the eyes,
# look into my eyes, you're under.

print(textwrap.fill(s, 40, initial_indent='    '))
    # Look into my eyes, look into my
# eyes, the eyes, the eyes, the eyes, not
# around the eyes, don't look around the
# eyes, look into my eyes, you're under.

print(textwrap.fill(s, 40, subsequent_indent='    '))
# Look into my eyes, look into my eyes,
#     the eyes, the eyes, the eyes, not
#     around the eyes, don't look around
#     the eyes, look into my eyes, you're
#     under.


# The textwrap module is a straightforward way to clean up text for
# printing--especially if you want the output to fit nicely on the
# terminal. On the subject of the terminal size, you can obtain it using
# os.get_terminal_size().


# For example:


import os
os.get_terminal_size().columns
# 80


# The fill() method has a few additional options that control how it
# handles tabs, sentence endings, and so on. Look at the documentation for
# the textwrap.TextWrapper class
# (http://docs.python.org/3.3/library/textwrap.html#textwrap.TextWrapper)
# for further details.


# 17) Handling HTML and XML Entities in Text


# You want to replace HTML or XML entities such as &entity; or &#code; with
# their corresponding text. Alternatively, you need to produce text, but
# escape certain characters ( e.g., <, >, or &).

# If you are producing text, replacing special characters such as < or > is
# relatively easy if you use the html.escape() function.


# For example:


s = 'Elements are written as "<tag>text</tag>".'
import html

print(s)
# Elements are written as "<tag>text</tag>".
print(html.escape(s))
# Elements are written as &quot;&lt;tag&gt;text&lt;/tag&gt;&quot;.

# Disable escaping of quotes
print(html.escape(s, quote=False))
# Elements are written as "&lt;tag&gt;text&lt;/tag&gt;".


# If you're trying to emit text as ASCII and want to embed character code
# entities for non-ASCII characters, you can use the
# errors='xmlcharrefreplace' argument to various I\O related functions to
# do it.


# For example:


s = 'Spicy Jalapeno'        # the n has an accent

s.encode('ascii', errors='xmlcharrefreplace')
# b'Spicy Jalape&#241;o'


# To replace entities in text, a different approach is needed. If you're
# actually processing HTML or XML, try using a proper HTML or XML parser
# first. Normally, these tools will automatically take care of replacing
# the values for you during parsing and you don't need to worry about it.

# If, for some reason, you've received bare text with some entities in it
# and you want them replaced manually, you can usually do it using various
# utility functions\methods associated with HTML or XML parsers.


# For example:


s = 'Spicy &quot;Jalape&#241;o&quot.'
from html.parser import HTMLParser
p = HTMLParser()

p.unescape(s)
'Spicy "Jalapeno".'         # n has accent

t = 'The prompt is &gt;&gt;&gt;'
from xml.sax.saxutils import unescape

unescape(t)
'The prompt is >>>'


# Proper escaping of special characters is an easily overlooked detail of
# generating HTML or XML. This is especially true if you're generating such
# output yourself using print() or other basic string formatting features.
# Using a utility function such as html.escape() is an easy solution.

# If you need to process text in the other direction, various utility
# functions, such as xml.sax.saxutils.unescape(), can help. However, you
# really need to investigate the use of a proper parser. For example, if
# processing HTML or XML, using a parsing module such as html.parser or
# xml.etree.ElementTree should already take care of details related to
# replacing entities in the input text for you.
