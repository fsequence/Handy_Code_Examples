
# Data Structures and Algorithms Part 2
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


# 6) Mapping Keys to Multiple Values in a Dictionary, line 14
# 7) Keeping Dictionaries in Order, line 105
# 8) Calculating with Dictionaries, line 162
# 9) Finding Commonalities in Two Dictionaries, line 287
# 10) Removing Duplicates from a Sequence while Maintaining Order, line 357
# 11) Naming a slice, line 452


# -------------------------------------------------------------------------


# 6) Mapping Keys to Multiple Values in a Dictionary

# You want to make a dictionary that maps keys to more than one value (a
# so-called "multi-dict").

# A dictionary is a mapping where each key is mapped to a single value. If
# you want to map keys to multiply values, you need to store the multiple
# values in another container such as a list or set. For example, you might
# make dictionaries like this:


d = {
    'a' : [1, 2, 3],
    'b' : [4, 5]
}

e = {
    'a' : {1, 2, 3},
    'b' : {4, 5}
}


# The choice of whether or not to use lists or sets depends on intended use.
# Use a list if you want to preserve the insertion order of the items. Use a
# set if you want to eliminate duplicates (and don't care about the order).

# To easily construct such dictionaries, you can use defaultdict in the
# collections module. A feature of defaultdict is that it automatically
# initializes the first value so you can simply focus on adding items.


# For example:


from collections import defaultdict

d = defaultdict(list)
d['a'].append(1)
d['a'].append(2)
d['b'].append(4)


d = defaultdict(set)
d['a'].add(1)
d['a'].add(2)
d['b'].add(4)


# One caution with defaultdict is that it will automatically create
# dictionary entries for keys accessed later on (even if they aren't
# currently found in the dictionary). If you don't want this behavior,
# you might use setdefault() on an ordinary dictionary instead.


# For example:


d = {}      # A regular dictionary
d.setdefault('a', []).append(1)
d.setdefault('a', []).append(2)
d.setdefault('b', []).append(4)


# However, many programmers find setdefault() to be a little unnatural--not
# to mention the fact that it always creates a new instance of the initial
# value on each invocation (the empty list [] in the example).

# In principle, constructing a multivalued dictionary is simple. However,
# initialization of the first value can be messy if you try to do it
# yourself. For example, you might have code that looks like this:


d = {}
for key, value in pairs:
    if key not in d:
        d[key] = []
    d[key].append(value)


# Using a defaultdict simply leads to much cleaner code:


d = defaultdict(list)
for key, value in pairs:
    d[key].append(value)


# This recipe is strongly related to the problem of grouping records
# together in data processing problems.


# 7) Keeping Dictionaries in Order


# Your want to create a dictionary, and you also want to control the order
# of items when iterating or serializing.


# To control the order of items in a dictionary, you can use an OrderedDict
# from the collections module. It exactly preserves the original insertion
# order of data when iterating.


# For example:


from collections import OrderedDict

d = OrderedDict()
d['foo'] = 1
d['bar'] = 2
d['spam'] = 3
d['grok'] = 4


# Outputs "foo 1", "bar 2", "spam 3", "grok 4"
for key in d:
    print(key, d[key])


# An OrderedDict can be particularly useful when you want to build a mapping
# that you may want to later serialize or encode into a different format.
# For example, if you want to precisely control the order of fields appearing
# in a JSON encoding, first building the data in an OrderedDict will do the
# trick:


import json

json.dumps(d)

# '{"foo": 1, "bar": 2, "spam": 3, "grok":4}'


# An OrderedDict internally maintains a doubly linked list that orders the
# keys according to insertion order. When a new item is first inserted, it
# is placed at the end of this list. Subsequent reassignment of an existing
# key doesn't change the order.

# Be aware that the size of an OrderedDict is more than twice as large as a
# normal dictionary due to the extra linked list that's created. Thus, if
# you are going to build a data structure involving a large number of
# OrderedDict instances (e.g., reading 100,000 lines of a CSV file into a
# list of OrderedDict instances), you would need to study the requirements
# of your application to determine if the benefits of using and OrderedDict
# outweighed the extra memory overhead.


# 8) Calculating with Dictionaries


# You want to perform various calculations (e.g., minimum value, maximum
# value, sorting, etc.) on a dictionary of data.

# Consider a dictionary that maps stock names to prices:


prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75

}


# In order to perform useful calculations on the dictionary contents, it is
# often useful to invert the keys and values of the dictionary using zip().
# For example, here is how to find the minimum and maximum price and stock
# name:


min_price = min(zip(prices.values(), prices.keys()))

# min_price is (10.75, 'FB')

max_price = max(zip(prices.values(), prices.keys()))

# max_price is (612.78, 'AAPL')


# Similarly, to rank the data, use zip() with sorted(), as in the
# following:


prices_sorted = sorted(zip(prices.values(), prices.keys()))

# prices_sorted is [(10.75, 'FB'), (37.2, 'HPQ'),
#                   (45.23, 'ACME'), (205.55, 'IBM'),
#                   (612.78, 'AAPL')]


# When doing these calculations, be aware that zip() creates an iterator
# that can only be consumed once. For example, the following code is an
# error:


prices_and_names = zip(prices.values(), prices.keys())

print(min(prices_and_names))    # OK
print(max(prices_and_names))    # ValueError: max() arg is an empty sequence


# If you try to perform common data reductions on a dictionary, you'll find
# that they only process the keys not the values.

# For example:


min(prices)     # Returns 'AAPL'
max(prices)     # Returns 'IBM'


# This is probably not what you want because you're actually trying to
# perform a calculation involving the dictionary values. You might try to
# fix this using the values() method of a dictionary:


min(prices.values())    # Returns 10.75
max(prices.values())    # Returns 612.78


# Unfortunately, this is often not exactly what you want either. For example,
# you may want to know information about the corresponding keys (e.g. which
# stock has the lowest price?).

# You can get the key corresponding to the min or max value if you supply a
# key function to min() and max().

# For example:


min(prices, key=lambda k: prices[k])    # Returns 'FB'
max(prices, key=lambda k: prices[k])    # Returns 'AAPL'


# However, to get the minimum value, you'll need to perform an extra lookup
# step.

# For example:


min_value = prices[min(prices, key=lambda k: prices[k])]


# The solution involving zip() solves the problem by "inverting" the
# dictionary into a sequence of (value, key) pairs. When performing
# comparisons on such tuples, the value element is compared first, followed
# by the key. This gives you exactly the behavior that you want and allows
# reductions and sorting to be easily performed on the dictionary contents
# using a single statement.

# It should be noted that in calculations involving (value, key) pairs, the
# key will be used to determine the result in instances where multiple
# entries happen to have the same value. For instance, in calculations such
# as min() and max(), the entry with the smallest or largest key will be
# returned if there happen to be duplicate values.

# For example:


prices = { 'AAA' : 45.23, 'ZZZ': 45.23 }

min(zip(prices.values(), prices.keys()))
# (45.23, 'AAA')

max(zip(prices.values()), prices.keys())
# (45.23, 'ZZZ')


# 9) Finding Commonalities in Two Dictionaries


# You have two dictionaries and want to find out what they might have in
# common (same keys, same values, etc.).

# Consider two dictionaries:


a = {
    'x' : 1,
    'y' : 2,
    'z' : 3,
}

b = {
    'w' : 10,
    'x' : 11,
    'y' : 2
}


# To find out what two dictionaries have in common, simply perform common
# set operations using the keys() or items() methods.

# For example:


# Find keys in common
a.keys() & b.keys()     # { 'x', 'y'}

# Find keys in a that are not in b
a.keys() - b.keys()     # { 'z' }

# Find (key, value) pairs in common
a.items() & b.items()   # { ('y', 2) }


# These kinds of operations can also be used to alter or filter dictionary
# contents. For example, suppose you want to make a new dictionary with
# selected keys removed. Here is some sample code using a dictionary
# comprehension:


# Make a new dictionary with certain keys removed
c = {key: a[key] for key in a.keys() - {'z', 'w'}}
# c is {'x': 1, 'y': 2}


# A dictionary is a mapping between a set of keys and values. The keys()
# method of a dictionary returns a keys-view object that exposes the keys.
# A little-known feature of keys views is that they also support common set
# operations such as unions, intersections, and differences. Thus, if you
# need to perform common set operations with dictionary keys, you can often
# just use the keys-view objects directly without first converting them
# into a set.

# The items() method of a dictionary returns an items-view object consisting
# of (key, value) pairs. This object supports similar set operations and can
# be used to perform operations such as finding out which key-value pairs two
# dictionaries have in common.

# Although similar, the values() method of a dictionary does not support the
# set operations described in this recipe. In part, this is due to the fact
# that unlike keys, the items contained in a values view aren't guaranteed
# to be unique. This alone makes certain set operations of questionable
# utility. However, if you must perform such calculations, they can be
# accomplished by simply converting the values to a set first.


# 10) Removing Duplicates from a Sequence while Maintaining Order


# You want to eliminate the duplicate values in a sequence, but preserve
# the order of the remaining items.

# If the values in the sequence are hashable, the problem can be easily
# solved using a set and a generator.


# For example:


def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)


# Here is an example of how to use your function:


a = [1, 5, 2, 1, 9, 1, 5, 10]

list(dedupe(a))
# [1, 5, 2, 9, 10]


# This only works if the items in the sequence are hashable. If you are
# trying to eliminate duplicates in a sequence of unhashable types (such
# as dicts), you can make a slight change to this recipe, as follows:


def dedupe(items, ke=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


# Here, the purpose of the key argument is to specify a function that
# converts sequence items into a hashable type for the purposes of duplicate
# detection. Here's how it works:


a = [{'x':1, 'y':2}, {'x':1, 'y':3}, {'x':1, 'y':2}, {'x':2, 'y':4}]

list(dedupe(a, key=lambda d: (d['x'],d['y'])))
# [{'x':1, 'y':2}, {'x':1, 'y':3}, {'x':2, 'y':4}]

list(dedupe(a, key=lambda d: d['x']))
# [{'x':1, 'y':2}, {'x':2, 'y':4}]


# This latter solution also works nicely if you want to eliminate duplicates
# based on the value of a single field or attribute or a larger data structure.

# If all you want to do is eliminate duplicates, it is often easy enough
# to make a set.


# For example:


a
# [1, 5, 2, 1, 9, 1, 5, 10]

set(a)
{1, 2, 10, 5, 9}


# However, this approach doesn't preserve any kind of ordering. So, the
# resulting data will be scrambled afterward. The solution shown avoids
# this.

# The use of a generator function in this recipe reflects the fact that you
#  might want the function to be extremely general purpose - not necessarily
# tied directly to list processing. For example, if you want to read a file,
# eliminating duplicate lines, you could simple do this:


with open(somefile, 'r') as f:
    for line in dedupe(f):
        ...


# The specification of a key function mimics similiar functionality in
# built-in functions such as sorted(), min() and max().


# 11) Naming a Slice


# Your program has become an unreadable mess of hardcoded slice indices and
# you want to clean it up.

# Suppose you have some code that is pulling specific data fields out of a
# record string with fixed fields (e.g., from a flat file or similar
# format):


# ######## 2908217348907230489020982734897239847987234987239487'
record = '....................100         ........513.25     ............'
cost = int(record[20:32]) * float(record[40:48])


# Instead of doing that, why not name the slices like this?


SHARES = slice(20,32)
PRICE = slice(40,48)

cost = int(record[SHARES]) * float(record[PRICE])


# In the latter version, you avoid having a lot of mysterious hardcoded
# indices, and what you're doing becomes much clearer.

# As a general rule, writing code with a lot of hardcoded index values
# leads to a readability and maintenance mess. For example, if you come
# back to the code a year later, you'll look at it and wonder what you were
# thinking when you wrote it. The solution shown is simply a way of more
# clearly stating what your code is actually doing.

# In general, the built-in slice() creates a slice object that can be used
# anywhere a slice is allowed.


# For example:


items = [0, 1, 2, 3, 4, 5, 6]
a = slice(2, 4)

items[2:4]
# [2,3]

items[a]
# [2,3]

items[a] = [10, 11]
# items = [0, 1, 10, 11, 4, 5, 6]

del items[a]

items
# [0, 1, 4, 5, 6]


# If you have a slice instance s, you can get more information about it by
# looking at its s.start, s.stop and s.step attributes, respectfully.


# For example:


a = slice(5, 50, 2)

a.start
# 5

a.stop
# 50

a.step
# 2


# In addition, you can map a slice onto a sequence of a specific size by
# using its indices(size) method. This returns a tuple (start, stop, step)
# where all values have been suitably limited to fit within bounds (as to
# avoid IndexError exceptions when indexing).


# For example:


s = 'HelloWorld'

a.indices(len(s))
# (5, 10, 2)

for i in range(*a.indices(len(s))):
    print(s[i])

# W
# r
# d
