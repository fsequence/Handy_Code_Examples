#
# Iterators and Generators Part 1
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#
# 1) Iterating in Sorted Order Over Merged Sorted Iterables, line 13
# 2) Unpacking a Sequence into Separate Variables, line 60
# 3) Unpacking Elements from Iterables of Arbitrary Length, line 162
# 4) Keeping the Last Nth Items, line 306
# 5)
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


# 4) Keeping the Last Nth Items


# You want to keep a limited history of the last few items seen during
# iteration or during some other kind of processing

# Keeping a limited history is perfect use for a collection.deque. For
# example, the following code performs a simple text match on a sequence
# of lines and yields the matching line along with the previous N lines
# of context when found:


from collections import deque

def search(lines, pattern, history=5):
    previous_lines = deque(maxlen=history)
    for line in lines:
        if pattern in line:
            yield  line, previous_lines
        previous_lines.append(line)


# Example use on a file


if __name__ == '__main__':
    with open('somefile.txt') as f:
        for line, prevlines in search(f, 'python', 5):
            for pline in prevlines:
                print(pline, end='')
            print(line, end='')
            print('-'*20)


# When writing code to search for items, it is common to use a generator
# function involving yield, as shown in this recipe's solution. This
# decouples the process of searching from the code that uses the results.

# Using deque(maxlen=N) creates a fixed-sized queue. When new items are
# added and the queue is full, the oldest item is automatically removed.
# For example:


q = deque(maxlen=3)
q.append(1)
q.append(2)
q.append(3)

q
# deque([1, 2, 3], maxlen=3)

q.append(4)

q
# deque([2, 3, 4], maxlen=3)

q.append(5)

q
# deque([3, 4, 5], maxlen=3)


# Although you could manually perform such operations on a list (e.g.,
# appending, deleting, etc.), the queue solution is far more elegant and
# runs a lot faster.

# More generally, a deque can be used whenever you need a simple queue
# structure. If you don't give it a maximum size, you get an unbounded
# queue that lets you append and pop items on either end.

# For example:


q = deque()
q.append(1)
q.append(2)
q.append(3)

q
# deque[(1, 2, 3])

q.appendleft(4)

q
# deque([4, 1, 2, 3])

q.pop()
# 3

q
# deque([4, 1, 2])

q.popleft()
# 4


# Adding or popping items from either end of a queue has O(1) complexity.
# This is unlike a list where inserting or removing items from the front
# of the list is O(N).
