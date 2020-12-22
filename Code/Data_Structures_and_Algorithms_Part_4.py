
# Data Structures and Algorithms Part 3
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


# 17) Extracting a Subset of a Dictionary, line 16
# 18) Mapping Names to Sequence Elements, line 73
# 19)
# 20)
# 21)


# -------------------------------------------------------------------------


# 17) Extracting a Subset of a Dictionary


# You want to make a dictionary that is a subset of another dictionary.

# This is easily accomplished using a dictionary comprehension.


# For example:


prices = {
    'ACME': 45.23,
    'APPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}


# Make a dictionary of all prices over 200
p1 = {key:value for key,value in prices.items() if value > 200}

# Make a dictionary of tech stocks
tech_names = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
p2 = {key:value for key,value in prices.items() if key in tech_names}


# Much of what can be accomplished with a dictionary comprehension might
# also be done by creating a sequence of tuples and passing them to the
# dict() function.


# For example:


p1 = dict((key,value) for key,value in prices.items() if value > 200)


# However, the dictionary comprehension solution is a bit clearer and
# actually runs quite a bit faster (over twice as fast when tested on the
# prices dictionary used in the example).

# Sometimes there are multiple ways of accomplishing the same thing. For
# instance, the second example could be rewritten as:


# Make a dictionary of tech stocks
tech_names = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
p2 = {key:prices[key] for key in prices.keys() & tech_names}


# However, a timing study reveals that this solution is almost 1.6 times
# slower than the first solution. If performance matters, it usually pays
# to spend a bit of time studying it.


# 18) Mapping Names to Sequence Elements

# You have code that accesses list or tuple elements by position, but this
# makes the code somewhat difficult to read at times. You'd also like to be
# less dependent on position in the structure, by accessing the elements by
# name.

# collections.namedtuple() provides these benefits, while adding minimal
# overhead over using a normal tuple object. collections.namedtuple() is
# actually a factory method that returns a subclass of the standard Python
# tuple type. You feed it a type name, and the fields it should have, and
# it returns a class that you can instantiate, passing in values for the
# fields you've defined, and so on.


# For example:

from collections import namedtuple
Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
sub = Subscriber('jonesy@example.com', '2012-10-19')

sub
# Subscriber(addr='jonesy@example.com', joined='2012-10-19')

sub.addr
# 'jonesy@example.com'

sub.joined
# '2012-10-19'


# Although an instance of a 'namedtuple' looks like a normal class
# instance, it is interchangeable with a tuple and supports all of the
# usual tuple operations such as indexing and unpacking.


# For example:


len(sub)
# 2

addr, joined = sub

addr
# 'jonesy@example.com'

joined
# '2012-10-19'


# A major use case for named tuples is decoupling your code from the
# position of the elements it manipulates. So, if you get back a large
# list of tuples from a database call, then manipulate them by accessing
# the positional elements, your code could break if, say, you added a new
# column to your table. Not so if you first cast the returned tuples to
# namedtuple.


# To illustrate, here is some code using ordinary tuples:


def compute_cost(records):
    total = 0.0
    for rec in records:
        total += rec[1] * rec[2]
    return total


# References to positional elements often make the code a bit less
# expressive and more dependent on the structure of the records. Here is
# a version that uses a namedtuple:


from collections import namedtuple

Stock = namedtuple('Stock', ['name', 'shares', 'price'])

def compute_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
    return total


# Naturally, you can avoid the explicit conversion to the Stock namedtuple
# if the records sequence in the example already contained such instances.

# One possible use of a namedtuple is as a replacement for a dictionary,
# which requires more space to store. Thus if you are building large data
# structures involving dictionaries, use of a namedtuple will be more
# efficient. However, be aware that unlike a dictionary, a namedtuple is
# immutable.


# For example:


s = Stock('ACME', 100, 100.23)

s
# Stock(name='ACME', shares=100, price=123.45)

s.shares = 75
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# AttributeError: can't set attribute


# If you need to change any of the attributes, it can be done using the
# _replace() method of a namedtuple instance, which makes an entirely new
# namedtuple with specified values replaced.


# For example:

s = s._replace(shares=75)

s
# Stock(name='ACME', shares=75, price=123.45)


# A subtle use of the _replace() method is that it can be a convenient way
# to populate named tuples that have optional or missing fields. To do
# this, you make a prototype tuple containing the default values and then
# use _replace() to create new instances with values replaced.


# For example:


from collections import namedtuple

Stock = namedtuple('Stock', ['name', 'shares', 'price', 'date', 'time'])

# Create a prototype instance
stock_prototype = Stock('', 0, 0.0, None, None)

# Function to convert a dictionary to a Stock
def dict_to_stock(s):
    return stock_prototype._replace(**s)


# Here is an example of how this code would work:


a = {'name': 'ACME', 'shares': 100, 'price': 123.45}

dict_to_stock(a)
# Stock(name='ACME', shares=100, price=123.45, date=None, time=None)

b = {'name': 'ACME', 'shares': 100, 'price': 123.45, 'date': 12/17/2012}

dict_to_stock(b)
# Stock(name='ACME', shares=100, price=123.45, date=12/17/2012, time=None)


# Last, but not least, it should be noted that if your goal is to define an
# efficient data structure where you will be changing various instance
# attributes, using namedtuple is not your best choice. Instead, consider
# defining a class using __slots__ instead.
