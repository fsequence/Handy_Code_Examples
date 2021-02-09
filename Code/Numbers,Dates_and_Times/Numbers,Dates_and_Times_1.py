
# Numbers, Dates and Times 1
# =-=-=-=-=-=-=-=-=-=-=-=-=-=


# 1) Rounding Numerical Values, line 15
# 2) Performing Accurate Decimal Calculations, line 109
# 3) Formatting Numbers for Output, line 244
# 4) Working with Binary, Octal, and Hexadecimal Integers, line 366


# -------------------------------------------------------------------------


# 1) Rounding Numerical Values


# You want to round a floating-point number to a fixed number of decimal
# places.

# For simple rounding, use the built-in round(value, ndigits) function.


# For example:


round(1.23, 1)
# 1.2

round(1.27, 1)
# 1.3

round(-1.27, 1)
# -1.3

round(1.25361, 3)
# 1.254


# When a value is exactly halfway between two choices, the behavior of
# round is to round to the nearest even digit. That is, values such as 1.5
# or 2.5 both get rounded to 2.

# The number of digits given to round() can be negative, in which case
# rounding takes place for tens, hundreds, thousands, and so on.


# For example:


a = 1627731

round(a, -1)
# 1627730

round(a, -2)
# 1627700

round(a, -3)
# 1628000


# Don't confuse rounding with formatting a value for output. If your goal
# is simply to output a numerical value with a certain number of decimal
# places, you don't typically need to use round(). Instead, just specify
# the desired precision when formatting.


# For example:


x = 1.23456

format(x, '0.2f')
# '1.23'

format(x, '0.3f')
'1.235'

'value is {:0.3f}'.format(x)
# 'value is 1.235'


# Also, resist the urge to round floating-point numbers to "fix" perceived
# accuracy problems. For example, you might be inclined to do this:


a = 2.1
b = 4.2
c = a + b

c
# 6.300000000000001

c = round(c, 2)         # "Fix" result (???)

c
# 6.3


# For most applications involving floating point, it's simply not necessary
# (or recommended) to do this. Although there are small errors introduced
# into calculations, the behavior of those errors are understood and
# tolerated. If avoiding such errors is important (e.g., in financial
# applications, perhaps), consider the use of the decimal module, which is
# discussed next in "2)".


# 2) Performing Accurate Decimal Calculations


# You need to perform accurate calculations with decimal numbers, and don't
# want the small errors that naturally occur with floats.

# A well-known issue with floating-point numbers is that they can't
# accurately represent all base-10 decimals. Moreover, even simple
# mathematical calculations introduce small errors.


# For example:


a = 4.2
b = 2.1

a + b
# 6.300000000000001

(a + b) == 6.3
# False


# These errors are a "feature" of the underlying CPU and the IEEE 754
# arithmetic performed by its floating-point unit. Since Python's float
# data type stores data using the native representation, there's nothing
# you can do to avoid such errors if you write your code using float
# instances.

# If you want more accuracy (and are willing to give up some performance),
# you can use the decimal module:


from decimal import Decimal

a = Decimal('4.2')
b = Decimal('2.1')

a + b
# Decimal('6.3')

print(a + b)
# 6.3

(a + b) == Decimal('6.3')
# True


# At first glance, it might look a little weird (i.e., specifying numbers
# as strings). However, Decimal objects work in every way that you would
# expect them to (supporting all of the usual math operations, etc.). If
# you print them or use them in string formatting functions, they look like
# normal numbers.

# A major feature of decimal is that it allows you to control different
# aspects of calculations, including number of digits and rounding. To do
# this, you create a local context and change its settings.


# For example:


from decimal import localcontext

a = Decimal('1.3')
b = Decimal('1.7')

print(a / b)
# 0.7647058823529411764705882353

with localcontext() as ctx:
    ctx.prec = 3
    print(a / b)

# 0.765

with localcontext() as ctx:
    ctx.prec = 50
    print(a / b)

# 0.76470588235294117647058823529411764705882352941176


# The decimal module implements IBM's "General Decimal Arithmetic
# Specification." Needless to say, there are a huge number of configuration
# options that are beyond the scope of this book.

# Newcomers to Python might be inclined to use the decimal module to work
# around perceived accuracy problems with the float data type. However,
# it's really important to understand your application domain. If you're
# working with science or engineering problems, computer graphics, or most
# things of a scientific nature, it's simply more common to use the normal
# floating-point type. For one, very few things in the real world are
# measured to the 17 digits of accuracy that floats provide. Thus, tiny
# errors introduced in calculations just don't matter. Second, the
# performance of native floats is significantly faster--something that's
# important if you're performing a large number of calculations.

# That said, you can't ignore the errors completely. Mathematicians have
# spent a lot of time studying various algorithms, and some handle errors
# better than others. You also have to be a little careful with effects due
# to things such as subtractive cancellation and adding large and small
# numbers together.


# For example:


nums = [1.23e+18, 1, -1.23e+18]

sum(nums)       # Notice how 1 disappears
0.0


# This latter example can be addressed by using a more accurate
# implementation in math.fsum():


import math
math.fsum(nums)
# 1.0


# However, for other algorithms, you really need to study the algorithm
# and understand its error propagation properties.

# All of this said, the main use of the decimal module is in programs
# involving things such as finance. In such programs, it is extremely
# annoying to have small errors creep into the calculation. Thus, decimal
# provides a way to avoid that. It is also common to encounter Decimal
# objects when Python interfaces with databases--again, especially when
# accessing financial data.


# 3) Formatting Numbers for Output


# You need to format a number for output, controlling the number of digits,
# alignment, inclusion of a thousands separator, and other details.

# To format a single number for output, use the built-in format() function.


# For example:


x = 1234.56789

# Two decimal places of accuracy
format(x, '0.2f')
# '1234.57'

# Right justified in 10 chars, one-digit accuracy
format(x, '>10.1f')
'    1234.6'

# Left justified
format(x, '<10.1f')
'1234.6    '

# Centered
format(x, '^10.1f')
'    1234.6    '

# Inclusion of thousands separator
format(x, ',')
'1,234.56789'

format(x, '0,.1f')
'1,234.6'


# If you want to use exponential notation, change the f to an e or E,
# depending on the case you want used for the exponential specifier.


# For example:


format(x, 'e')
'1.234568e+03'

format(x, '0.2E')
'1.23E+03'


# The general form of the width and precision in both cases is
# '[<>^]?width[,]?(.digits)?' where width and digits are integers and ?
# signifies optional parts. The same format codes are also used in the
# .format() method of strings.


# For example:


'The value is {:0.2f}'.format(x)
# 'The value is 1,234.57'


# Formatting numbers for output is usually straightforward. The technique
# shown works for both floating-point numbers and Decimal numbers in the
# decimal module.

# When the number of digits is restricted, values are rounded away
# according to the same rules of the round() function.


# For example:


x
# 1234.56789

format(x, '0.1f')
'1234.6'

format(-x, '0.1f')
'-1234.6'


# Formatting of values with a thousands separator is not locale aware. If
# you need to take that into account, you might investigate functions in
# the locale module. You can also swap separator characters using the
# translate() method of strings.


# For example:


swap_separators = { ord('.'):',', ord(','):'.'}

format(x, ',').translate(swap_separators)
# '1.234,56789'

# In a lot of Python code, numbers are formatted using the % operator.


# For example:


'%0.2f' % x
# '1234.57'

'%10.1f' % x
'    1234.6'

'%-10.1f' % x
'1234.6    '


# This formatting is still acceptable, but less powerful than the more
# modern format() method. For example, some features (e.g., adding
# thousands separators) aren't supported when using the % operator to
# format numbers.


# 4) Working with Binary, Octal, and Hexadecimal Integers


# You need to convert or output integers represented by binary, octal, or
# hexadecimal digits.

# To convert an integer into a binary, octal, or hexadecimal text string,
# use the bin(), oct(), or hex() functions, respectively:


x = 1234

bin(x)
# '0b10011010010'

oct(x)
# '0o2322'

hex(x)
# '0x4d2'


# Alternatively, you can use the format() function if you don't want the
# 0b, 0o, or 0x prefixes to appear.


# For example:


format(x, 'b')
# '10011010010'

format(x, 'o')
# '2322'

format(x, 'x')
# '4d2'


# Integers are signed, so if you are working with negative numbers, the
# output will also include a sign.


# For example:


x = -1234

format(x, 'b')
# '-10011010010'

format(x, 'x')
# '-4d2'


# If you need to produce an unsigned value instead, you'll need to add in
# the maximum value to set the bit length. For example, to show a 32-bit
# value, use the following:


x = -1234

format(2**32 + x, 'b')
# '11111111111111111111101100101110'

format(2**32 + x, 'x')
# 'fffffb2e'


# To convert integer strings in different bases, simply use the int()
# function with as appropriate base.


# For example:


int('4d2', 16)
# 1234

int('10011010010', 2)
# 1234


# For the most part, working with binary, octal, and hexadecimal integers
# is straightforward. Just remember that these conversions only pertain to
# the conversion of integers to and from a textual representation. Under
# the covers, there's just one integer type.

# Finally, there is one caution for programmers who use octal. The Python
# syntax for specifying octal values is slightly different than many other
# languages. For example, if you try something like this, you'll get a
# syntax error:


import os

os.chmod('script.py', 0755)
File "<stdin>", line 1
    os.chmod('script.py', 0755)

SyntaxError: invalid token


# Make sure you prefix the octal value with 0o, as shown here:


os.chmod('script.py', 0o755)
