
# Data Structures and Algorithms Part 3
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


# 17) Extracting a Subset of a Dictionary, line 16
# 18)
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


p1 = dict((key,vlaue) for key,value in prices.items() if value > 200)


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
