
# Strings and Texts Part 3
# =-=-=-=-=-=-=-=-=-=-=-=-=


# 12) Sanitizing and Cleaning Up Text, line 15
# 13) Aligning Text Strings, line 160
# 14) Combining and Concatenating Strings, line 268
# 15) Interpolating Variables in Strings, line 462


# -------------------------------------------------------------------------


# 12) Sanitizing and Cleaning Up Text


# Some bored script kiddie has entered the text "python" (characters have
# various different accents above them, will indicate future occurrences
# with the word 'accents' in a comment) into a form on your web page and
# you'd like to clean it up somehow.

# The problem of sanitizing and cleaning up text applies to a wide variety
# of problems involving text parsing and data handling. At a very simple
# level, you might use basic string functions (e.g., str.upper() and
# str.lower()) to convert text to a standard case. Simple replacements
# using str.replace() or re.sub() can focus on removing or changing very
# specific character sequences. You can also normalize text using unicode
# data.normalize(), as shown in '9)'.

# However, you might want to take the sanitation process a step further.
# Perhaps, for example, you want to eliminate whole ranges of characters or
# strip diacritical marks. To do so, you can turn to the often overlooked
# str.translate() method. To illustrate, suppose you've got a messy string
# such as the following:

s = 'python\fis\tawesome\r\n'           # accents

s
# 'python\x0cis\tawesome\r\n'           accents

# The first step is to clean up the whitespace. To do this, make a small
# translation table and use translate():


remap = {
    ord('\t') : ' ',
    ord('\f') : ' ',
    ord('\r') : None                    # Deleted
}
a = s.translate(remap)

a
# 'python is awesome\n'                 accent


# As you can see here, whitespace characters such as \t and \f have been
# remapped to a single space. The carriage return \r has been deleted
# entirely.

# You can take this remapping idea a step further and build much bigger
# tables. For example, let's remove all combining characters:


import unicodedata
import sys

cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode)
                         if unicodedata.combining(chr(c)))

b = unicodedata.normalize('NFD', a)

b
# python is awesome\n'                  accent

b.translate(cmb_chrs)
# 'python is awesome/n'                 no accent


# In this last example, a dictionary mapping every Unicode combining
# character to None is created using the dict.fromkeys().

# The original input is then normalized into a decomposed form using
# unicodedata.normalize(). From there, the translate function is used to
# delete all of the accents. Similar techniques can be used to remove other
# kinds of characters (e.g., control characters, etc.).

# As another example, here is a translation table that maps all Unicode
# decimal digit characters to their equivalent in ASCII:


digitmap = { c:ord('0') + unicodedata.digit(chr(c))
             for c in range(sys.maxunicode)
             if unicodedata.category(chr(c)) == 'Nd' }

len(digitmap)
# 460

# Arabic digits
x = '\u0661\u0662\u0663'

x.translate(digitmap)
# '123'


# Yet another technique for cleaning up text involves I/O decoding and
# encoding functions. The idea here is to first do some preliminary cleanup
# of the text, and then run it through a combination of encode() or
# decode() operations to strip or alter it.


# For example:


a
# 'python is awesome\n'                 accent
b = unicodedata.normalize('NFD', a)

b.encode('ascii', 'ignore').decode('ascii')
# 'python is awesome\n'                 no accent


# Here the normalization process decomposed the original text into
# characters along with separate combining characters. The subsequent ASCII
# encoding/decoding simply discarded all of those characters in one fell
# swoop. Naturally, this would only work if getting an ASCII representation
# was the final goal.

# A major issue with sanitizing text can be runtime performance. As a
# general rule, the simpler it is, the faster it will run. For simple
# replacements, the str.replace() method is often the fastest approach --
# even if you have to call it multiple times. For instance, to clean up
# whitespace, you could use code like this:


def clean_spaces(s):
    s = s.replace('\r', '')
    s = s.replace('\t', ' ')
    s = s.replace('\f', ' ')
    return s


# If you try it, you'll find that it's quite a bit faster than using
# translate() or an approach using a regular expression.

# On the other hand, the translate() method is very fast if you need to
# perform any kind of nontrivial character-to-character remapping or
# deletion.

# In the big picture, performance is something you will have to study
# further in your particular application. Unfortunately, it's impossible
# to suggest one specific technique that works best for all cases, so try
# different approaches and measure it.

# Although the focus of the above examples has been text, similar
# techniques can be applied to bytes, including simple replacements,
# translation, and regular expressions.


# 13) Aligning Text Strings


# You need to format text with some sort of alignment applied.

# For basic alignment of strings, the ljust(), rjust(), and center()
# methods of strings can be used.


# For example:


text = 'Hello World'

text.ljust(20)
'Hello World           '

text.rjust(20)
# '         Hello World'

text.center(20)
# '     Hello World     '


# All of these methods accept an optional fill character as well.


# For example:


text.rjust(20, '=')
# '=========Hello World'

text.center(20, '*')
# '****Hello World*****'


# The format() function can also be used to easily align things. All you
# need to do is use the <, >, or ^ characters along with a desired width.


# For example:


format(text, '>20')
# '         'Hello World'

format(text, '<20')
'Hello World          '

format(text, '^20')
# '     Hello World     '


# If you want to include a fill character other than a space, specify it
# before the alignment character:


format(text, '=>20s')
# '=========Hello World'

format(text, '*^20s')
# '****Hello World*****'


# These format codes can also be used in the format() method when
# formatting multiple values.


# For example:


'{:>10s} {:>10s}'.format('Hello', 'World')
# '     Hello       World'


# One benefit of format() is that it is not specific to strings. It works
# with any value, making it more general purpose. For instance, you can use
# it with numbers:

x = 1.2345

format(x, '>10')
'   1.2345'

format(x, '^10.2f')
'   1.23    '


# In older code, you will also see the % operator used to format text.


# For example:

'%-20s' % text
# 'Hello World      '

'%20s' % text
# '       Hello World'


# However, in new code, you should probably prefer the use of the format()
# function or method. format() is a lot more powerful than what is provided
# with the % operator. Moreover, format() is more general purpose than
# using the ljust(), rjust(), or center() method of strings in that it
# works with any kind of object.


# 14) Combining and Concatenating Strings


# You want to combine many small strings together into a larger string.

# If the strings you wish to combine are found in a sequence or iterable,
# the fastest way to combine them is to use the join() method.


# For example:


parts = ['Is', 'Chicago', 'Not', 'Chicago?']

' '.join(parts)
'Is Chicago Not Chicago?'

','.join(parts)
# 'Is,Chicago,Not,Chicago?'

''.join(parts)
# 'IsChicagoNotChicago?'


# At first glance, this syntax might look really odd, but the join()
# operation is specified as a method on strings. Partly this is because
# the objects you want to join could come from any number of different data
# sequences (e.g., lists, tuples, dicts, files, sets, or generators), and
# it would be redundant to have join() implemented as a method on all of
# those objects separately. So you just specify the separator string that
# you want and use the join() method on it to glue text fragments together.


# If you're only combining a few strings, using + usually works well
# enough:

a = 'Is Chicago'
b = 'Not Chicago?'

a + ' ' + b
# 'Is Chicago Not Chicago?'


# The + operator also works fine as a substitute for more complicated
# string formatting operations.


# For example:


print('{} {}'.format(a,b))
# Is Chicago Not Chicago?

print(a + ' ' + b)
# Is Chicago Not Chicago?


# If you're trying to combine string literals together in source code, you
# can simply place them adjacent to each other with no + operator.


# For example:


a = 'Hello' 'World'

a
# 'HelloWorld'


# Joining strings together might not seem advanced enough to warrant
# more in depth examples but it's often an area where programmers make
# programming choices that severely impact the performance of their code.

# The most important thing to know is that using the + operator to join
# a lot of strings together is grossly inefficient due to the memory copies
# and garbage collection that occurs. In particular, you never want to
# write code that joins strings together like this:


s = ''
for p in parts:
    s += p


# This runs quite a bit slower than using the join() method, mainly because
# each += operation creates a new string object. You're better off just
# collecting all of the parts first and then joining them together at the
# end.


# One related (and pretty neat) trick is the conversion of data to strings
# and concatenation at the same time using a generator expression, as
# described in '19)' of 'Data Structures and Algorithms Part 4'.


# For example:


data = ['ACME', 50, 91.1]

','.join(str(d) for d in data)
# 'ACME,50,91.1'


# Also be on the lookout for unnecessary string concatenations. Sometimes
# programmers get carried away with concatenation when it's really not
# technically necessary.


# For example, when printing:


print(a + ':' + b + ':' + c)        # Ugly
print(':'.join([a, b, c]))          # Still ugly

print(a, b, c, sep=':')             # Better


# Mixing I/O operations and string concatenation is something that might
# require study in your application. For example, consider the following
# two code fragments:


# Version 1 (string concatenation)
f.write(chunk1 + chunk2)

# Version 2 (separate I/O operations)
f.write(chunk1)
f.write(chunk2)


# If the two strings are small, the first version might offer much better
# performance due to the inherent expense of carrying out an I/O system
# call. On the other hand, if the two strings are large, the second version
# may be more efficient, since it avoids making a large temporary result
# and copying large blocks of memory around. Again, it must be stressed
# that this is something you would have to study in relation to your own
# data in order to determine which performs best.

# Last, but not least, if you're writing code that is building output from
# lots of small strings, you might consider writing that code as a
# generator function, using yield to emit fragments.


# For example:


def sample():
    yield 'Is'
    yield 'Chicago'
    yield 'Not'
    yield 'Chicago?'


# The interesting thing about this approach is that it makes no assumption
# about how the fragments are to be assembled together. For example, you
# could simply join the fragments using join():


text = ''.join(sample())


# Or you could redirect the fragments to I/O:


for part in sample():
    f.write(part)


# Or you could come up with some kind of hybrid scheme that's smart about
# combining I/O operations:


def combine(source, maxsize):
    parts = []
    size = 0
    for part in source:
        parts.append(part)
        size += len(part)
        if size > maxsize:
            yield ''.join(parts)
            parts = []
            size = 0
    yield ''.join(parts)

for part in combine(sample(), 32768):
    f.write(part)


# The key point is that the original generator function doesn't have to
# know the precise details. It just yields the parts.


# 15) Interpolating Variables in Strings


# You want to create a string in which embedded variable names are
# substituted with a string representation of a variable's value.

# Python has no direct support for simply substituting variable values in
# strings. However, this feature can be approximated using the format()
# method of strings.


# For example:


s = '{name} has {n} messages.'

s.format(name='Guido', n=37)
'Guido has 37 messages.'


# Alternatively, if the values to be substituted are truly found in
# variables, you can use the combination of format_map() and vars(), as in
# the following:


name = 'Guido'
n = 37

s.format_map(vars())
'Guido has 37 messages.'


# One subtle feature of vars() is that it also works with instances.


# For example:


class Info:
    def __init__(self, name, n):
        self.name = name
        self.n = n

a = Info('Guido',37)
s.format_map(vars(a))
'Guido has 37 messages.'


# One downside of format() and format_map() is that they do not deal
# gracefully with missing values.


# For example:


s.format(name='Guido')
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# KeyError: 'n'


# One way to avoid this is to define an alternative dictionary class with a
# __missing__() method, as in the following:

class safesub(dict):
    def __missing__(self, key):
        return '{' + key + '}'


# Now use this class to wrap the inputs to format_map():


del n       # Make sure n is undefined

s.format_map(safesub(vars()))
# 'Guido has {n} messages.'


# If you find yourself frequently performing these steps in your code, you
# could hide the variable substitution process behind a small utility
# function that employs a so-called "frame hack."


# For example:


# If you find yourself frequently performing these steps in your code, you
# could hide the variable substitution process behind a small utility
# function that employs a so-called "frame hack."


# For example:


import sys

def sub(text):
    return text.format_map(safesub(sys._getframe(1).f_locals))


# Now you can type things like this:


name = 'Guido'
n = 37

print(sub('Hellow {name}'))
# Hello Guido

print(sub('You have {n} messages.'))
# You have 37 messages.

print(sub('Your favorite color is {color}'))
# Your favorite color is {color}


# The lack of true variable interpolation in Python has led to a variety of
# solutions over the years. As an alternative to the solution presented in
# these examples, you will sometimes see string formatting like this:


name = 'Guido'
n= 37

'%(name) has %(n) messages.' % vars()
# 'Guido has 37 messages.'


# You may also see the use of template strings:

import string
s = string.Template('$name has $n messages.')
s.substitute(vars())
'Guido has 37 messages.'


# However, the format() and format_map() methods are more modern than either
# of these alternative, and should be preferred. One benefit of using
# format() is that you also get all of the features related to string
# formatting (alignment, padding, numerical formatting, etc.), which is
# simply not possible with alternatives such as Template string objects.

# Parts of this recipe also illustrate a few interesting advanced features.
# The little-known __missing__() method of mapping/dict classes is a method
# that you can define to handle missing values. In the safesub class, this
# method has been defined to return missing values back as a placeholder.
# Instead of getting a KeyError exception, you would see the missing values
# appearing in the resulting string (potentially useful for debugging).

# The sub() function uses sys._getframe(1) to return the stack frame of the
# caller. From that, the f_locals attribute is accessed to get the local
# variables. It goes without saying that messing around with stack frames
# should probably be avoided in most code. However, for utility functions
# such as a string substitution feature, it can be useful. As an aside,
# it's probably worth noting that f_locals is a dictionary that is a copy
# of the local variables in the calling function. Although you can modify
# the contents of f_locals, the modifications don't actually have any
# lasting effect. Thus, even though accessing a different stack frame
# might look evil, it's not possible to accidentally overwrite variables
# or change the local environment of the caller.
