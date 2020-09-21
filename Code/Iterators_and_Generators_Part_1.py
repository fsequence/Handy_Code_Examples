#
# Iterators and Generators Part 1
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#
# 1) Iterating in Sorted Order Over Merged Sorted Iterables
# 2)
#
#
#
# ---------------------------------------------------------------------
#
#
# 1) Iterating in Sorted Order Over Merged Sorted Iterables
#
#
# You have a collection of sorted sequences and you want to iterate over a sorted
# sequence of them all merged together, then maybe the following will due:
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
