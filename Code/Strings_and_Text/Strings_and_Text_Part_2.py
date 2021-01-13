
# Strings and Text Part 2
# =-=-=-=-=-=-=-=-=-=-=-=-


# 5) Searching and Replacing Text, line 17
# 6) Searching and Replacing Case-Insensitive Text, line 112
# 7) Specifying a Regular Expression for the Shortest Match, line 166
# 8) Writing a Regular Expression for Multiline Patterns, line 220
# 9) Normalizing Unicode Text to a Standard Representation, line 282
# 10) Working with Unicode Characters in Regular Expressions, line 396
# 11) Stripping Unwanted Characters from Strings, line 456


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


# 7) Specifying a Regular Expression for the Shortest Match


# You're trying to match a text pattern using regular expressions, but it
# is identifying the longest possible matches of a pattern. Instead, you
# would like to change it to find the shortest possible match.

# This problem often arises in patterns that try to match text enclosed
# inside a pair of starting and ending delimiters (e.g., a quoted string).
# To illustrate, consider this example:


str_pat = re.compile(r'\"(.*)\"')
text1 = 'Computer says "no."'

str_pat.findall(text1)
# ['no.']

text2 = 'Computer says "no." Phone says "yes."'

str_pat.findall(text2)
# ['no." Phone says "yes.']


# In this example, the pattern r'\"(.*)\"' is attempting to match text
# enclosed inside quotes. However, the * operator in a regular expression
# is greedy, so matching is based on finding the longest possible match.
# Thus, in the second example involving text2, it incorrectly matches the
# two quoted strings.

# To fix this, add the ? modifier after the * operator in the pattern, like
# this:


str_pat = re.compile(r'\"(.*?)\"')

str_pat.findall(text2)
# ['no.', 'yes.']


# This makes the matching nongreedy, and produces the shortest match
# instead.

# The examples above addresses one of the more common problems encountered
# when writing regular expressions involving the dot (.) character. In a
# pattern, the dot matches any character except a newline. However, if you
# bracket the dot with starting and ending text (such as a quote), matching
# will try to find the longest possible match to the pattern. This causes
# multiple occurrences of the starting or ending text to be skipped
# altogether and included in the results of the longer match. Adding the ?
# right after operators such as * or + forces the matching algorithm to
# look for the shortest possible match instead.


# 8) Writing a Regular Expression for Multiline Patterns


# You're trying to match a block of text using a regular expression, but
# you need the match to span multiple lines.

# This problem typically arises in patterns that use the dot(.) to match
# any character but forget to account for the fact that it doesn't match
# newlines. For example, suppose you are trying to match C-style comments:


comment = re.compile(r'/\*(.*?)\*/')
text1 = '/* this is a comment */'
text2 = '''/* this is a
                multiline comment */
'''

comment.findall(text1)
# [' this is a comment ']

comment.findall(text2)
# []


# To fix the problem, you can add support for newlines.


# For example:


comment = re.compile(r'/\*((?:.|\n)*?)\*/')

comment.findall(text2)
# [' this is a/n            multiline comment ']


# In this pattern, (?:.|\n) specifies a noncapture group (i.e., it defines
# a group for the purposes of matching, but that group is not captured
# separately or numbered).

# The re.compile() function accepts a flag, re.DOTALL, which is useful
# here. It makes the . in a regular expression match all characters,
# including newlines.


# For example:


comment = re.compile(r'/\*(.*?)\*/', re.DOTALL)

comment.findall(text2)
# [' this is a\n                multiline comment ']


# Using the re.DOTALL flag works fine for simple cases, but might be
# problematic if you're working with extremely complicated patterns or a
# mix of separate regular expressions that have been combined together for
# the purpose of tokenizing, as described in '18)'. If given a choice, it's
# usually better to define your regular expression pattern so that it works
# correctly without the need for extra flags.


# 9) Normalizing Unicode Text to a Standard Representation


# You're working with Unicode strings, but need to make sure that all of
# the strings have the same underlying representation.

# In Unicode, certain characters can be represented by more than one valid
# sequence of code points. To illustrate, consider the following example:


s1 = 'Spicy Jalape\u00f1o'
s2 = 'Spicy Jalapen\u0303o'

s1
# 'Spicy Jalapeno' (the n is supposed to have a ~ accent over it)

s2
# 'Spicy Jalapeno' (the n is supposed to have a ~ accent over it)

s1 == s2
# False

len(s1)
# 14

len(s2)
# 15


# Here the text "Spicy Jalapeno" (n with the ~ accent) has been presented in
# two forms. The first uses the fully composed 'n' (n with the ~ accent)
# character (U+00F1). The second uses the Latin letter 'n' followed by a
# '~' combining character (U+0303).

# Having multiple representations is a problem for programs that compare
# strings. In order to fix this, you should first normalize the text into a
# standard representation using the unicodedata module:


import unicodedata

t1 = unicodedata.normalize('NFC', s1)
t2 = unicodedata.normalize('NFC', s2)

t1 == t2
# True

print(ascii(t1))
# 'Spicy Jalape\xf1o'

t3 = unicodedata.normalize('NFD', s1)
t4 = unicodedata.normalize('NFD', s2)

t3 == t4
# True

print(ascii(t3))
# 'Spicy Jalapen\u0303o'


# The first argument to normalize() specifies how you want the string
# normalized. NFC means that characters should be fully composed (i.e., use
# a single code point if possible). NFD means that characters should be
# fully decomposed with the use of combining characters.

# Python also supports the normalization forms NFKC and NFKD, which add
# extra compatibility features for dealing with certain kinds of
# characters.


# For example:


s = '\ufb01'        # A single character

s
# 'fi'

unicodedata.normalize('NFD', s)
# 'fi'

# Notice how the combined letters are broken apart here. The two 'fi'
# above are/would be different than the two 'fi' below.

unicodedata.normalize('NFKD', s)
# 'fi'

unicodedata.normalize('NFKC', s)
# 'fi'


# Normalization is an important part of any code that needs to ensure that
# it processes Unicode text in a sane and consistent way. This is
# especially true when processing strings received as part of user input
# where you have little control of the encoding.

# Normalization can also be an important part of sanitizing and filtering
# text. For example, suppose you want to remove all diacritical marks from
# some text (possibly for the purposes of searching or matching):


t1 = unicodedata.normalize('NFD', s1)

''.join(c for c in t1 if not unicodedata.combining(c))
# 'Spicy Jalapeno' (this should have a plain old 'n')


# This last example shows another important aspect of the unicodedata
# module - namely, utility functions for testing characters against
# character classes. The combining() function tests a character to see if
# it is a combining character. There are other functions in the module for
# finding character categories, testing digits, and so forth.


# 10) Working with Unicode Characters in Regular Expressions


# You are using regular expressions to process text, but are concerned
# about the handling of Unicode characters.

# By default, the re module is already programmed with rudimentary
# knowledge of certain Unicode character classes. For example, \d already
# matches any unicode digit character:


import re
num = re.compile('\d+')

# ASCII digits
num.match('123')
# <_sre.SRE_Match object at 0x1007d9ed0>

# Arabic digits

num.match('\u0661\u0662\u0663')
# <_sre.SRE_Match object at 0x101234030>


# If you need to include specific Unicode characters in patterns, you can
# use the usual escape sequence for Unicode characters (e.g., \uFFFF or
# \UFFFFFFF). For example, here is a regex that matches all characters in a
# few different Arabic code pages:


arabic = re.compile('[\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff]+')


# When performing matching and searching operations, it's a good idea to
# normalize and possibly sanitize all text to a standard form first, see
# '9)'. However, it's also important to be aware of special cases. For
# example, consider the behavior of case-insensitive matching combined with
# case folding:


pat = re.complie('stra\u00dfe', re.IGNORECASE)
s = 'straβe'                # I got the beta symbol from an internet search

pat.match(s)                # Matches
# <_sre.SRE_Match object at 0x10069d370>

pat.match(s.upper())        # Doesn't match

s.upper()                   # Case folds
# 'STRASSE'


# Mixing Unicode and regular expressions is often a good way to make your
# head explode. If you're going to do it seriously, you should consider
# installing the third-party regex library
# (http://pypi.python.org/pypi/regex), which provides full support for
# Unicode case folding, as well as a variety of other interesting features,
# including approximate matching.


# 11) Stripping Unwanted Characters from Strings


# You want to strip unwanted characters, such as whitespace, from the
# beginning, end, or middle of a text string.

# The strip() method can be used to strip characters from the beginning or
# end of a string, lstrip() and rstrip() perform stripping from the left or
# right side, respectively. By default, these methods strip whitespace, but
# other characters can be given.


# For example:


# Whitespace stripping
s = '   hello world    \n'

s.strip()
# 'hello world'

s.lstrip()
# 'hello world  \n'

s.rstrip()
# '    hello world'

# Character stripping
t = '-----hello====='

t.lstrip('-')
# 'hello====='

t.strip('-=')
# 'hello'


# The various strip() methods are commonly used when reading and cleaning
# up data for later processing. For example, you can use them to get rid of
# whitespace, remove quotations, and other tasks.

# Be aware that stripping does not apply to any text in the middle of a
# string.


# For example:


s = '   hello       world   \n'
s = s.strip()

s
# 'hello        world'


# If you needed to do something to the inner space, you would need to use
# another technique, such as using the replace() method or a regular
# expression substitution.


# For example:


s.replace(' ', '')
# 'helloworld'
import re

re.sub('\s+', ' ', s)
# 'hello world'


# It is often the case that you want to combine string stripping operations
# with some other kind of iterative processing, such as reading lines of
# data from a file. If so, this is one area where a generator expression
# can be useful.


# For example:


with open(filename) as f:
    lines = (line.strip() for line in f)
    for line in lines:
        ...


# Here, the expression lines = (line.strip() for line in f) acts as a kind
# of data transform. It's efficient because it doesn't actually read the
# data into any kind of temporary list first. It just creates an iterator
# where all of the lines produced have the stripping operation applied to
# them.

# For even more advanced stripping, you might turn to the translate()
# method. See '12)' on sanitizing strings for further details.
