#
# Iterators and Generators Part 1
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#
# 1) Iterating in Sorted Order Over Merged Sorted Iterables
# 2) Unpacking a Sequence into Separate Variables
# 3) Unpacking Elements from Iterables of Arbitrary Length
#
#
# -------------------------------------------------------------------------
#
#
# 1) Iterating in Sorted Order Over Merged Sorted Iterables
#
#
# You have a collection of sorted sequences and you want to iterate over a
# sorted sequence of them all merged together, then maybe the following will due:
#
# Input:

import heapq
a = [ 1, 4, 7, 10 ]
b = [ 2, 5, 6, 11 ]
for c in heapq.merge(a,b):
    print(c)


# Output:
#
# 1
# 2
# 4
# 5
# 6
# 7
# 10
# 11


# heapq can be very useful with large files. It iterates over 1 item from each
# sequence then spits out the smallest one first, then the second one after that
# and so on. If you want both sequences inputed to be sorted then you must sort
# that yourself beforehand because the heapq will just read the next item in line
# from each sequence and give the sorted(smallest to largest) from that.


# Example for use with files:


import heapq

with open('sorted_file_1', 'rt') as file1, \
    open('sorted_file_2' 'rt') as file2, \
    open('merged_file', 'wt') as outf:

    for line in heapq.merge(file1, file2):
        outf.write(line)


# 2) Unpacking a Sequence into Separate Variables


# You have an N-element tuple or sequence that you would like to unpack into
# a collection of N variables

# Any sequence (or iterable) can be unpacked into variables using a simple
# assignment operation. The only requirement is that the number of variables
# and structure match the sequence.

# For example:

# Input:

p = (4, 5)
x, y = p

# Output:

# x
# 4

# y
# 5


data = ['ACME', 50, 91.1, (2012, 12, 21)]
name, shares, price, date = data

name
# 'ACME'

date
# (2012, 12, 21)

name, shares, price, (year, mon, day) = data

name
# 'ACME'

year
# 2012

mon
# 12

day
# 21

# If there is a mismatch in the number of elements, you'll get an error.

# For example:

p = (4, 5)
x, y, z = p

# Traceback (most recent call last):
#     File "<stdin>", line 1, in <module>
# ValueError: need more than 2 values to unpack


# Also consider this:


# Unpacking actually works with any object that happens to be iterable, not
# just tuples or lists. This includes strings, files, iterators, and
# generators.

# For example

s = 'Hello'
a, b, c, d, e = s

a
# 'H'

b
# 'e'

e
# 'o'


# When unpacking, you may sometimes want to discard certain values. Python
# has no special syntax for this, but you can often just pick a throwaway
# variable name for it.

# For example:

data = ['ACME', 50, 91.1, (2012, 12, 21)]
_, shares, price, _ = data

shares
# 50

price
# 91.1

# Remember to make sure that the variable name you pick isn't being used for
# something else already.


# 3) Unpacking Elements from Iterables of Arbitrary Length


# You need to unpack N elements from an iterable, but the iterable may be
# longer than N elements, causing a "too many values to unpack" exception.

# Python "star expressions" can be used to address this problem. For
# example, suppose you run a course and decide at the end of the semester
# that you're going to drop the first and last homework grades, and only
# average the rest of them. If there are only four assignments, maybe you
# simply unpack all four, but what if there are 24? A star expression makes
# it easy:


def drop_first_last(grades):
    first, *middle, last = grades
    return avg(middle)


# As another use case, suppose you have user records that consist of a name
# and email address, followed by an arbitrary number of phone numbers. You
# could unpack the records like this:


record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *phone_numbers = record

name
# 'Dave'

email
# 'dave@example.com'

phone_numbers
# ['773-555-1212', '847-555-1212']


# It's worth noting that the phone_numbers variable will always be a list,
# regardless of how many phone numbers are unpacked (including none). Thus,
# any code that uses phone_numbers won't have to account for the
# possibility that it might not be a list or perform any kind of additional
# type checking.

# The starred variable can also be the first one in the list. For example,
# say you have a sequence of values representing your company's sales
# figures for the last eight quarters. If you want to see how the most
# recent quarter stacks up to the average of the first seven, you could do
# something like this:


*trailing_qtrs, current_qtr = sales_record
trailing_avg = sum(trailing_qtrs) / len(trailing_qtrs)
return avg_comparison(trailing_avg / current_qtr)


# Here's a view of the operation(just part of if) from the Python
# Interpreter:


*trailing, current = [10, 8, 7, 1, 9, 5, 10, 3]

trailing
# [10, 8, 7, 1, 9, 5, 10]

current
# 3


# It is worth noting that the star syntax can be especially useful when
# iterating over a sequence of tuples of varying length. For example,
# perhaps a sequence of tagged tuples:


records = [
    ('foo', 1, 2),
    ('bar', 'hello')
    ('foo', 3, 4),
]

def do_foo(x, y):
    print('foo', x, y)

def do_bar(s):
    print('bar', s)

for tag, *args in records:
    if tag == 'foo':
        do_foo(*args)
    elif tag == 'bar':
        do_bar(*args)


# Star unpacking can also be useful when combined with certain kinds of
# string processing operations, such as splitting.
#
# For example:


line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/user/bin/false'
uname, *fields, homedir, sh = line.split(':')

uname
# 'nobody'

homedir
# '/var/empty'

sh
# '/usr/bin/false'


# Sometimes you might want to unpack values and throw them away. You can't
# just specify a bare * when unpacking, but you could use a common
# throwaway variable name, such as _ or ign(ignored).

# For example:


record = ('ACME', 50, 123.45, (12, 18, 2012))
name, *_, (*_, year) = record

name
# 'ACME'

year
# 2012


# There is a certain similarity between star unpacking and list-processing
# features of various functional languages. For example, if you have a list,
# you can easily split it into head and tail components like this:


items = [1, 10, 7, 4, 5, 9]
head, *tail = items

head
# 1

tail
# [10, 7, 4, 5, 9]

