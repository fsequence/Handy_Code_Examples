
# Data Structures and Algorithms Part 1
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


# 1) Unpacking a Sequence into Separate Variables, line 14
# 2) Unpacking Elements from Iterables of Arbitrary Length, line 116
# 3) Keeping the Last Nth Items, line 259
# 4) Finding the Largest or Smallest N Items, line 360
# 5) Implementing a Priority Queue, line 454


# -------------------------------------------------------------------------


# 1) Unpacking a Sequence into Separate Variables


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


# 2) Unpacking Elements from Iterables of Arbitrary Length


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


# 3) Keeping the Last Nth Items


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


# 4) Finding the Largest or Smallest N Items


# You want to make a list of the largest or smallest N items in a
# collection.

# The heapq module has two functions--nlargest() and nsmallest()-- that
# do exactly what you want.

# For example:


import heapq

nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]

print(heapq.nlargest(3, nums))
# [42, 37, 23]

print(heapq.nsmallest(3, nums))
# [-4, 1, 2]


# Both functions also accept a key parameter that allows them to be used
# with more complicated data structures.

# For example:


portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1}
    {'name': 'AAPL', 'shares': 50, 'price': 543.22}
    {'name': 'FB', 'shares': 200, 'price': 21.09}
    {'name': 'HPQ', 'shares': 35, 'price': 31.75}
    {'name': 'YHOO', 'shares': 45, 'price': 16.35}
    {'name': 'ACME', 'shares': 75, 'price': 115.65}
]

cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])


# If you are looking for the N smallest or largest items and N is small
# compared to the overall size of the collection, these functions provide
# superior performance. Underneath the covers, they work by first
# converting the data into a list where items are ordered as a heap.

# For example:


nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
import heapq
heap = list(nums)
heapq.heapify(heap)

heap
# [-4, 2, 1, 23, 7, 2, 18, 23, 42, 37, 8]


# The most important feature of a heap is that heap[0] is always the
# smallest item. Moreover, subsequent items can be easily found using the
# heapq.heappop() method, which pops off the first item and replaces it
# with the next smallest item (an operation that requires O(log N)
# operations where N is the size of the heap).

# For example:


heapq.heappop(heap)
# -4

heapq.heappop(heap)
# 1

heapq.heappop(heap)
# 2


# The nlargest() and nsmallest() functions are most appropriate if you are
# trying to find a relatively small number of items. If you are simply
# trying to find the single smallest or largest item (N=1), it is faster
# to use min() and max(). Similarly, if N is about the use sorted(items)[:N]
# or sorted(items)[-N:]). It should be noted that the actual implementation
# of nlargest() and nsmallest() is adaptive in how it operates and will
# carry out some of these optimizations on your behalf(e.g., using sorting
# if N is close to the same size as the input).

# Although it's not necessary to use this recipe, the implementation of a
# heap is an interesting and worthwhile subject of study. This can usually
# be found in any decent book on algorithms and data structures. The
# documentation for the heapq module also discusses the underlying
# implementation details.


# 5) Implementing a Priority Queue


# You want to implement a queue that sorts items by a given priority and
# always returns the item with the highest priority on each pop operation.

# The following class uses the heapq module to implement a simple priority
# queue:


import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]


# Here is an example of how it might be used:

class Item:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return 'Item({!r})'.format(self.name)


q = PriorityQueue()
q.push(Item('foo'), 1)
q.push(Item('bar'), 5)
q.push(Item('spam'), 4)
q.push(Item('grok'), 1)


q.pop()
# Item('bar')

q.pop()
# Item('spam')

q.pop()
# Item('foo')

q.pop()
# Item('grok')


# Observe how the first pop() operation returned the item with the highest
# priority. Also observe how the two items with the same priority (foo and
# grok) were returned in the same order in which they were inserted into
# the queue.

# The core of this recipe concerns the use of the heapq module. The
# functions heapq.heappush() and heapq.heappop() insert and remove items
# from a list _queue in a way such that the first item in the list has the
# smallest priority. The heappop() method always returns the "smallest"
# item, so that is the key to making the queue pop the correct items.
# Moreover, since the push and pop operations have O(log N) complexity
# where N is the number of items in the heap, they are fairly efficient
# even for fairly large values of N.

# In this recipe, the queue consists of tuples of the form (-priority,
# index, item). The priority value is negated to get the queue to sort
# items from highest priority to lowest priority. This is opposite of the
# normal heap ordering, which sorts from lowest to highest value.

# The role of the index variable is to properly order items with the same
# priority level. By keeping a constantly increasing index, the items will
# be sorted according to the order in which they were inserted. However,
# the index also serves an important role in making the comparison
# operations work for items that have the same priority level.

# To elaborate on that, instances of Item in the example can't be ordered.


# For example:


a = Item('foo')
b = Item('bar')

a < b
# Traceback (most recent call last):
#     File"<stdin>", line 1, in <module>
# TypeError: unorderable types: Item() < Item()


# If you make (priority, item) tuples, they can be compared as long as the
# priorities are different. However, if two tuples with equal priorities
# are compared, the comparison fails as before.


# For example:


a = (1, Item('foo'))
b = (5, Item('bar'))

a < b
# True

c = (1, Item('grok'))

a < c
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# TypeError: unorderable types: Item() < Item()


# By introducing the extra index and making(priority, index, item) tuples,
# you avoid this problem entirely since no two tuples will ever have the
# same value for index (and Python never bothers to compare the remaining
# tuple values once the result of comparison can be determined):


a = (1, 0, Item('foo'))
b = (5, 1, Item('bar'))
c = (1, 2, Item('grok'))

a < b
# True

a < c
# True


# If you want to use this queue for communication between threads, you need
# to add appropriate locking and signaling.
