#
# Iterators and Generators Part 1
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#
# 1) Iterating in Sorted Order Over Merged Sorted Iterables
# 2) Unpacking a Sequence into Separate Variables
#
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
