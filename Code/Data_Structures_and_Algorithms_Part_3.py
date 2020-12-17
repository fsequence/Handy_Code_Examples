
# Data Structures and Algorithms Part 3
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


# 12) Determining the Most Frequently Occurring Items in a Sequence, line 17
# 13) Sorting a List of Dictionaries by a Common Key, line 118
# 14) Sorting Objects Without Native Comparison Support, line 231
# 15) Grouping Records Together based on a Field, line 301
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
# listing of the members on your website and you receive the following data
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


rows_by_lfname = sorted(rows, key=itemgetter('lname', 'fname'))
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


# 14) Sorting Objects Without Native Comparison Support


# You want to sort objects of the same class, but they don't natively
# support comparison operations.

# The built-in sorted() function takes a key argument that can be passed a
# callable that will return some value in the object that sorted will use to
# compare the objects. For example, if you have a sequence of User instances
# in your application, and you want to sort them by their user_id attribute,
# you would supply a callable that takes a User instance as input and returns
# the user_id.


# For example:


class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return 'User({})'.format(self.user_id)


users = [User(23), User(3), User(99)]


users
# [User(23), User(3), User(99)]

sorted(users, key=lambda u: u.user_id)
# [User(3), User(23), User(99)]


# Instead of using lambda, an alternative approach is to use
# operator.attrgetter():


from operator import attrgetter

sorted(users, key=attrgetter('user_id'))
# [User(3), User(23), User(99)]


# The choice of whether or not to use lambda or attrgetter() may be one of
# personal preference. However, attrgetter() is often a tad bit faster and
# also has the added feature of allowing multiple fields to be extracted
# simultaneously. This is analogous to the use of operator.itemgetter() for
# dictionaries. For example, if User instances also had a first_name and
# last_name attribute, you could perform a sort like this:


by_name = sorted(users, key=attrgetter('last_name', 'first_name'))


# It is also worth nothing that the technique used in this recipe can be
# applied to functions such as min() and max().


# For example:


min(users, key=attrgetter('user_id'))
# User(3)

max(users, key=attrgetter('user_id'))
# User(99)


# 15) Grouping Records Together based on a Field


# You have a sequence of dictionaries or instances and you want to iterate
# over the data in groups based on the value of a particular field, such as
# date.

# The itertools.groupby() function is particularly useful for grouping data
# together like this. To illustrate, suppose you have the following list of
# dictionaries:


rows= [
    {'address': '5412 N CLARK', 'date': '07/01/2012'},
    {'address': '5148 N CLARK', 'date': '07/04/2012'},
    {'address': '5800 N 58TH', 'date': '07/02/2012'},
    {'address': '2122 N CLARK', 'date': '07/03/2012'},
    {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
    {'address': '1060 N ADDISON', 'date': '07/02/2012'},
    {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
    {'address': '1039 N GRANVILLE', 'date': '07/04/2012'},
]


# Now suppose you want to iterate over the data in chunks grouped by date.
# To do it, first sort by the desired field (in this case, date) and then
# use itertools.groupby():


from operator import itemgetter
from itertools import groupby

# Sort by the desired field first
rows.sort(key=itemgetter('date'))

# Iterate in groups
for date, items in groupby(rows, key=itemgetter('date')):
    print(date)
    for i in items:
        print('   ', i)


# This produces the following output:

# 07/01/2012
#   {'date': '07/01/2012', 'address': '5412 N CLARK'}
#   {'date': '07/01/2012', 'address': '4801 N BROADWAY'}

# 07/02/2012
#   {'date': '07/02/2012', 'address': '5800 E 58TH'}
#   {'date': '07/02/2012', 'address': '5645 N RAVENSWOOD'}
#   {'date': '07/02/2012', 'address': '1060 W ADDISON'}

# 07/03/2012
#   {'date': '07/03/2012', 'address': '2122 N CLARK'}

# 07/04/2012
#   {'date': '07/04/2012', 'address': '5148 N CLARK'}
#   {'date': '07/04/2012', 'address': '1039 W GRANVILLE'}


# The groupby() function works by scanning a sequence and finding sequential
# "runs" of identical values (or values returned by the given key function).
# On each iteration, it returns the value along with an iterator that
# produces all of the items in a group with the same value.

# An important preliminary step is sorting the data according to the field
# of interest. Since groupby() only examines consecutive items, failing to
# sort first won't group the records as you want.

# If your goal is to simply group the data together by dates into a large
# data structure that allows random access, you may have better luck using
# defaultdict() to build a multidict.


# For example:


from collections import defaultdict

rows_by_date = defaultdict(list)
for row in rows:
    rows_by_date[row['date']].append(row)


# This allows the records for each date to be accessed easily like this:


for r in rows_by_date['07/01/2012']:
    print(r)

# {'date': '07/01/2012', 'address': '5412 N CLARK'}
# {'date': '07/01/2012', 'address': '4801 N BROADWAY'}


# For this latter example, it's not necessary to sort the records first.
# Thus, if memory is no concern, it may be faster to do this than to first
# sort the records and iterate using groupby().
