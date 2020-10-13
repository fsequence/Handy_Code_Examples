
# Data Structures and Algorithms Part 2
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


# 6) Mapping Keys to Multiple Values in a Dictionary, line 14
# 7) Keeping Dictionaries in Order, line 105
# 8) Calculating with Dictionaries, line 162
# 9)
# 10)


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
# by the key. This gives you exactyly the behavior that you want and allows
# reductions and sorting to be easily performed on the dictionary contents
# using a single statement.
