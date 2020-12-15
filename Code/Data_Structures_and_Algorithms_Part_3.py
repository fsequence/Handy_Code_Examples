
# Data Structures and Algorithms Part 3
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


# 12) Determining the Most Frequently Occurring Items in a Sequence, line 17
# 13) Sorting a List of Dictionaries by a Common Key, line 118
# 14)
# 15)
# 16)
# 17)


# -------------------------------------------------------------------------


# 12) Determining the Most Frequently Occurring Items in a Sequence

# You have a sequence of items, and you'd like to determine the most
# frequently occurring items in the sequence.

# The collections.Counter class is designed for just such a problem. It
# even comes with a handy most_common() method that will give you the
# answer.

# To illustrate, let's say you have a list of words and you want to find
# out which words occur most often. Here's how you would do it:


words = [
    'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes', 'the', 'eyes' 
    'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the', 'eyes', "don't",
    'look', 'around', 'the', 'eyes', 'look', 'into', 'my', 'my', 'eyes',
    "you're", 'under'
]

from collections import Counter

word_counts = Counter(words)
top_three = word_counts.most_common(3)

print(top_three)
# [('eyes', 8), ('the', 5), ('look', 4)]


# As input, Counter objects can be fed any sequence of hashable input items.
# Under the covers, a Counter is a dictionary that maps the items to the
# number of occurrences.


# For example:

word_counts['not']
# 1

word_counts['eyes']
# 8


# If you want to increment the count manually, simply use addition:

morewords = ['why', 'are', 'you', 'not', 'looking', 'in', 'my', 'eyes']

for word in morewords:
    word_counts[word] += 1

word_counts['eyes']
# 9


# Or, alternatively, you could use the update() method:

word_counts.update(morewords)


# A little-known feature of Counter instances is that they can be easily
# combined using various mathematical operations.


# For example:

a = Counter(words)
b = Counter(morewords)

a
# Counter ({'eyes': 8, 'the': 5, 'look': 4, 'into': 3, 'my': 3, 'around': 2,
#           "you're": 1, "don't": 1, 'under': 1, 'not': 1})

b
# Counter ({ 'eyes': 1, 'looking': 1, 'are': 1, 'in': 1, 'not': 1, 'you': 1,
#           'my': 1, 'why': 1})


# Combine counts

c = a + b

c
# Counter({'eyes': 9, 'the': 5, 'look': 4, 'my' 4, 'into': 3, 'not': 2,
#           'around': 2, "you're": 1, "don't": 1, 'in' 1, 'why': 1,
#           'looking': 1, 'are': 1, 'under': 1, 'you': 1})


# Subtract counts

d = a - b

d
# Counter({'eyes': 7, 'the': 5, 'look': 4, 'into': 3, 'my': 2, 'around': 2,
#           "you're": 1, "don't": 1, 'under': 1})


# Needless to say, Counter objects are a tremendously useful tool for almost
# any kind of problem where you need to tabulate and count data. You should
# prefer this over manually written solutions involving dictionaries.


# 13) Sorting a List of Dictionaries by a Common Key


# You have a list of dictionaries and you would like to sort the entries
# according to one or more of the dictionary values.

# Sorting this type of structure is easy using the operator module's
# itemgetter function. Let's say you've queried a database table to get a
# listing of the members on your website and you recieve the following data
# structure in return:


rows = [
    {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
    {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
    {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
    {'fname': 'Big', 'lname': 'Jones', 'uid': 1004},
    ]


# It's fairly easy to output these rows ordered by any of the fields
# common to all of the dictionaries.


# For example:


from operator import itemgetter

rows_by_fname = sorted(rows, key=itemgetter('fname'))
rows_by_uid = sorted(rows, key=itemgetter('uid'))

print(rows_by_fname)
print(rows_by_uid)


# The preceding code would output the following:


[{'fname': 'Big', 'uid': 1004, 'lname': 'Jones'},
 {'fname': 'Brian', 'uid': 1003, 'lname': 'Jones'},
 {'fname': 'David', 'uid': 1002, 'lname': 'Beazley'},
 {'fname': 'John', 'uid': 1001, 'lname': 'Cleese'}]

[{'fname': 'John', 'uid': 1001, 'lname': 'Cleese'},
 {'fname': 'David', 'uid': 1002, 'lname': 'Beazley'},
 {'fname': 'Brian', 'uid': 1003, 'lname': 'Jones'},
 {'fname': 'Big', 'uid': 1004, 'lname': 'Jones'}]


# The itemgetter() function can also accept multiple keys.


# For example, this code


rows_by_lfname = sorted(rows, key=itemgetter('lname','fname'))
print(rows_by_lfname)


# Produces output like this:


[{'fname': 'David', 'uid': 1002, 'lname': 'Beazley'},
 {'fname': 'John', 'uid': 1001, 'lname': 'Cleese'},
 {'fname': 'Big', 'uid': 1004, 'lname': 'Jones'},
 {'fname': 'Brian', 'uid': 1003, 'lname': 'Jones'}]


# In this example, rows is passed to the built-in sorted() function, which
# accepts a keyword argument key. This argument is expected to be a callable
# that accepts a single item from rows as input and returns a value that
# will be used as the basis for sorting. The itemgetter() function creates
# just such a callable.

# The operator.itemgetter() function takes as arguments the lookup indices
# used to extract the desired values from the records in rows. It can be a
# dictionary key name, a numeric list element, or any value that can be fed
# to an object's __getitem__() method. If you give multiple indices to
# itemgetter(), the callable it produces will return a tuple with all of the
# elements in it, and sorted() will order the output according to the sorted
# order of the tuples. This can be useful if you want to simultaneously sort
# on multiple fields (such as last and first name, as shown in the example).

# The functionality of itemgetter() is sometimes replaced by lambda
# expressions.


# For example:


rows_by_fname = sorted(rows, key=lambda r: r['fname'])
rows_by_lfname = sorted(rows, key=lambda r: (r['lname'], r['fname']))


# This solution often works just fine. However, the solution involving
# itemgetter() typically runs a bit faster. Thus, you might prefer it if
# performance is a concern.

# Last, but not least, don't forget that the technique shown in this recipe
# can be applied to functions such as min() and max().


# For example:


min(rows, key=itemgetter('uid'))
# {'fname': 'John', 'lname': 'Cleese', 'uid': 1001}

max(rows, key=itemgetter('uid'))
# {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
