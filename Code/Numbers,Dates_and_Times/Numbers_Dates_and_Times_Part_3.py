
# Numbers, Dates and Times Part 3
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


# 12) Converting Days to Seconds, and Other Basic Time Conversions
# 13)
# 14)
# 15)
# 16)

# -------------------------------------------------------------------------


# 12) Converting Days to Seconds, and Other Basic Time Conversions


# You have code that needs to perform simple time conversion, like days to
# seconds, hours to minutes, and so on.

# To perform conversions and arithmetic involving different units of time,
# use the data time module. For example, to represent an interval of time,
# create a timedelta instance, like this:


from datetime import timedelta

a = timedelta(days=2, hours=6)
b = timedelta(hours=4.5)

c = a + b

c.days
# 2

c.seconds / 3600
# 10.5

c.total_seconds() / 3600
# 58.5


# If you need to represent specific dates and times, create datetime
# instances and use the standard mathematical operations to manipulate
# them.


# For example:


from datetime import datetime

a = datetime(2012, 9, 23)
print(a + timedelta(days=10))
# 2012-10-03 00:00:00

b = datetime(2012, 12, 21)
d = b - a

d.days
# 89

now = datetime.today()

print(now)
# 2012-12-21 14:54:43.094063

print(now + timedelta(minutes=10))
# 2012-12-21 15:04:43.094063


# When making calculations, it should be noted that datetime is aware of
# leap years.


# For example:


a = datetime(2012, 3, 1)
b = datetime(2012, 2, 28)

a - b
# datetime.timedelta(2)

(a - b).days
# 2

c = datetime(2013, 3, 1)
d = datetime(2013, 2, 28)

(c - d).days
# 1


# For most basic date and time manipulation problems, the datetime module
# will suffice. If you need to perform more complex date manipulations,
# such as dealing with time zones, fuzzy time ranges, calculating the dates
# of holidays, and so forth, look at the dateutil module
# (http://pypi.python.org/pypi/python-dateutil).[

# To illustrate, many similar time calculations can be performed with
# dateutil.relativedelta() function. However, one notable feature is that
# it fills in some gaps pertaining to the handling of months (and their
# differing number of days).


# For instance:


a = datetime(2012, 9, 23)

a + timedelta(months=1)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# TypeError: 'months' is an invalid keyword argument for this function

from dateutil.relativedelta import relativedelta

a + relativedelta(months=+1)
# datetime.datetime(2012, 10, 23, 0, 0)

a + relativedelta(months=+4)
# datetime.datetime(2013, 1, 23, 0, 0)

# Time between two dates
b = datetime(2012, 12, 21)
d = b - a

d
# datetime.timedelta(89)

d = relativedelta(b, a)

d
# relativedelta(months=+2, days=+28)

d.months
# 2

d.days
# 28


# 13)
