
# Strings and Texts Part 1
# =-=-=-=-=-=-=-=-=-=-=-=-=


# 5) Searching and Replacing Text, line 15
# 6) Searching and Replacing Case-Insensitive Text, line 109
# 7)
# 8)


# -------------------------------------------------------------------------


# 5) Searching and Replacing Text, line 15


# You want to search for and replace a text pattern in a string.

# For simple literal patterns, use the str.replace() method.


# For example:


text = 'yeah, but no, but yeah, but no, but yeah'

text.replace('yeah', 'yep')
# 'yep, but no, but yep, but no, but yep'


# For more complicated patterns, use the sub() functions/methods in the re
# module. To illustrate, suppose you want to rewrite dates of the form
# "11/27/2012" as "2012-11-27."


# Here is a sample of how to do it:


text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
import re

re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text)
# 'Today is 2012-11-27. PyCon starts 2013-3-13.'


# The first argument to sub() is the pattern to match and the second
# argument is the replacement pattern. Backslashed digits such as \3 refer
# to capture group numbers in the pattern.

# If you're going to perform repeated substitutions of the same pattern,
# consider compiling it first for better performance.


# For example:


import re
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')

datepat.sub(r'\3-\1-\2', text)
# 'Today is 2012-11-27. PyCon starts 2013-3-13.'


# For more complicated substitutions, it's possible to specify a
# substitution callback function instead.


# For example:


from calendar import month_abbr

def change_date(m):
    mon_name = month_abbr[int(m.group(1))]
    return '{} {} {}'.format(m.group(2), mon_name, m.group(3))

datepat.sub(change_date, text)
# 'Today is 27 Nov 2012. PyCon starts 13 Mar 2013.'


# As input, the argument to the substitution callback is a match object, as
# returned by match() or find(). Use the .group() method to extract
# specific parts of the match. The function should return the replacement
# text.


# If you want to know how many substitutions were made in addition to
# getting the replacement text, use re.subn() instead.


# For example:


newtext, n = datepat.subn(r'\3-\1-\2', text)

newtext
# 'Today is 2012-11-27. PyCon starts 2013-3-13.'

n
# 2


# There isn't much more to regular expression search and replace than the
# sub() method shown. The trickiest part is specifying the regular
# expression pattern -- nothing a little practice can't fix.


# 6) Searching and Replacing Case-Insensitive Text


# You need to search for and possibly replace text in a case-insensitive
# manner.

# To perform case-insensitive text operations, you need to use the re
# module and supply the re.IGNORECASE flag to various operations.


# For example:


text = 'UPPER PYTHON, lower python, Mixed Python'

re.findall('python', text, flags=re.IGNORECASE)
# ['Python', 'python', 'Python']

re.sub('python', 'snake', text, flags=re.IGNORECASE)
# 'UPPER snake, lower snake, Mixed snake'


# The last example reveals a limitation that replacing text won't match the
# case of the matched text. If you need to fix this, you might have to use
# a support function, as in the following:


def matchcase(word):
    def replace(m):
        text = m.group()
        if text.isupper():
            return word.upper()
        elif text.islower():
            return word.lower()
        elif text[0].isupper():
            return word.capitalize()
        else:
            return word
    return replace


# Here is an example of using this last function:


re.sub('python', matchcase('snake'), text, flags=re.IGNORECASE)
# 'UPPER SNAKE, lower snake, Mixed Snake'


# For simple use cases, simply providing the re.IGNORECASE is enough to
# perform case-insensitive matching. However, be aware that this may not
# be enough for certain kinds of Unicode matching involving case folding.
# Look into working with Unicode characters in regular expressions.
