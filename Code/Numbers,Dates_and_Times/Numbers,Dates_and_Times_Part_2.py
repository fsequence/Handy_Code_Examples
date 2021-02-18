
# Numbers, Dates and Times Part 2
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


# 5) Packing and Unpacking Large Integers from Bytes
# 6)
# 7)
# 8) Calculating with Fractions
# 9) Calculating with Large Numerical Arrays
# 10)


# -------------------------------------------------------------------------


# 5) Packing and Unpacking Large Integers from Bytes


# You have a byte string and you need to unpack it into an integer value.
# Alternatively, you need to convert a large integer back into a byte
# string.

# Suppose your program needs to work with a 16-element byte string that
# holds a 128-bit integer value.


# For example:


data = b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'


# To interpret the bytes as an integer, use int, from_bytes(), and specify
# the byte ordering like this:


len(data)
# 16

int.from_bytes(data, 'little')
# 69120565665751139577663547927094891008

int.from_bytes(data, 'big')
# 94522842520747284487117727783387188


# To convert a large integer value back into a byte string, use the
# int.to_bytes() method, specifying the number of bytes and the byte order.


# For example:


x = 94522842520747284487117727783387188

x.to_bytes(16, 'big')
# b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'

x.to_bytes(16, 'little')
# b'4\x00#\x00\x01\xef\xcd\x00\xab\x90x\x00V4\x12\x00'


# Converting large integer values to and from byte strings is not a common
# operation. However, it sometimes arises in certain application domains,
# such as cryptography or networking. For instance, IPv6 network addresses
# are represented as 128-bit integers. If you are writing code that needs
# to pull such values out of a data record, you might face this problem.

# As an alternative to the previous example, you might be inclined to
# unpack values using the struct module, as described in "11)" of "Data
# Encoding and Processing". This works, but the size of integers that can
# be unpacked with struct is limited. Thus, you would need to unpack
# multiple values and combine them to create the final value.


# For example:


data
# b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'

import struct

hi, lo = struct.unpack('>QQ', data)

(hi << 64) + lo
# 94522842520747284487117727783387188


# The specification of the byte order (little or big) just indicates
# whether the bytes that make up the integer value are listed from the
# least to most significant or the other way around. This is easy to view
# using a carefully crafted hexadecimal value:


x = 0x01020304

x.to_bytes(4, 'big')
# b'\x01\x02\x03\x04'

x.to_bytes(4, 'little')
# b'\x04\x03\x02\x01'

# If you try to pack an integer into a byte string, but it won't fit,
# you'll get an error. You can use the int.bit_length() method to determine
# how many bits are required to store a value if needed:


x = 523 ** 23

x
# 335381300113661875107536852714019056160355655333978849017944067

x.to_bytes(16, 'little')
# Traceback (most recent call last):
#   File "<stdin>", in line 1, in <module>
# OverflowError: int too big to convert

x.bit_length()
# 208

nbytes, rem = divmod(x.bit_length(), 8)

if rem:
    nbytes += 1

x.to_bytes(nbytes, 'little')
# b'\x03x\xf1\x82iT\x96\xac\xc7c\x16\xf3\xb9\xcf...\xd0'


# 6)


# 7)


# 8) Calculating with Fractions


# You have entered a time machine and suddenly find yourself working on
# elementary-level homework problems involving fractions. Or perhaps
# you're writing code to make calculations involving measurements made
# in your wood shop.

# The fractions module can be used to perform mathematical calculations
# involving fractions.


# For example:


from fractions import Fraction

a = Fraction(5, 4)
b = Fraction(7, 16)

print(a + b)
# 27/16

print(a * b)
# 35/64

# Getting numerator/denominator
c = a * b

c.numerator
# 35

c.denominator
# 64

# Converting to a float
float(c)
# 0.546875

# Limiting the denominator of a value
print(c.limit_denominator(8))
# 4/7

# Converting a float to a fraction
x = 3.75
y = Fraction(*x.as_integer_ratio())

y
# Fraction(15, 4)


# Calculating with fractions doesn't arise often in most programs, but
# there are situations where it might make sense to use them. For example,
# allowing a program to accept units of measurement in fractions and
# performing calculations with them in that form might alleviate the need
# for a user to manually make conversions to decimals or floats.


# 9) Calculating with Large Numerical Arrays


# You need to perform calculations on large numerical datasets, such as
# arrays or grids.

# For any heavy computation involving arrays, use the NumPy library
# (http://www.numpy.org). The major feature of NumPy is that it gives
# Python an array object that is much more efficient and better suited for
# mathematical calculation than a standard Python list. Here is a short
# example illustrating important behavioral differences between lists and
# NumPy arrays:


# Python lists
x = [1, 2, 3, 4]
y = [5, 6, 7, 8]

x * 2
# [1, 2, 3, 4, 1, 2, 3, 4]

x + 10
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# TypeError: can only concatenate list (not "int") to list

x + y
# [1, 2, 3, 4, 5, 6, 7, 8]

# Numpy arrays
import numpy as np
ax = np.array([1, 2, 3, 4])
ay = np.array([5, 6, 7, 8])

ax * 2
# array([2, 4, 6, 8])

ax + 10
# array([11, 12, 13, 14])

ax + ay
# array([ 6, 8, 10, 12])

ax * ay
# array([ 5, 12, 21, 32])


# As you can see, basic mathematical operations involving arrays behave
# differently. Specifically, scalar operations (e.g., ax * 2 or ax + 10)
# apply the operation on an element-by-element basis. In addition,
# performing math operations when both operands are arrays applies the
# operation to all elements and produces a new array.

# The fact that math operations apply to all of the elements simultaneously
# makes it very easy and fast to compute functions across an entire array.
# For example, if you want to compute the value of a polynomial:


def f(x):
    return 3*x**2 - 2*x + 7

f(ax)
# array([ 8, 15, 28, 47])


# NumPy provides a collection of "universal functions" that allow for array
# operations. These are replacements for similar functions normally found
# in the math module.


# For example:


np.sqrt(ax)
# array([ 1.        ,   1.41421356,   1.73205081,   2.      ])

np.cos(ax)
array([ 0.54030231, -0.41614684, -0.9899925, -0.65364362])


# Using universal functions can be hundreds of times faster than looping
# over the array elements one at a time and performing calculations using
# functions in the math module. Thus, you should prefer their use whenever
# possible.

# Under the covers, NumPy arrays are allocated in the same manner as in C
# or Fortran. Namely, they are large, contiguous memory regions consisting
# of a homogenous data type. Because of this, it's possible to make arrays
# much larger than anything you would normally put into a Python list. For
# example, if you want to make a two-dimensional grid of 10,000 by 10,000
# floats, it's not an issue:


grid = np.zeros(shape=(10000,10000), dtype=float)

grid
# array([[ 0.,  0.,  0., ..., 0., 0., 0.],
#       [ 0.,  0.,  0., ..., 0., 0., 0.],
#       [ 0.,  0.,  0., ..., 0., 0., 0.],
#       ...,
#       [ 0.,  0.,  0., ..., 0., 0., 0.],
#       [ 0.,  0.,  0., ..., 0., 0., 0.],
#       [ 0.,  0.,  0., ..., 0., 0., 0.]])


# All of the usual operations still apply to all of the elements
# simultaneously:


grid += 10

grid
# array([[ 10., 10., 10., ..., 10., 10., 10.,],
#       [ 10., 10., 10., ..., 10., 10., 10.,],
#       [ 10., 10., 10., ..., 10., 10., 10.,],
#       ...,
#       [ 10., 10., 10., ..., 10., 10., 10.,],
#       [ 10., 10., 10., ..., 10., 10., 10.,],
#       [ 10., 10., 10., ..., 10., 10., 10.,]])

np.sin(grid)
# array([[-0.54402111, -0.54402111, -0.54402111, ..., -0.54402111,
#         -0.54402111, -0.54402111],
#       [-0.54402111, -0.54402111, -0.54402111, ..., -0.54402111,
#         -0.54402111, -0.54402111],
#       [-0.54402111, -0.54402111, -0.54402111, ..., -0.54402111,
#         -0.54402111, -0.54402111],
#       ...,
#       [-0.54402111, -0.54402111, -0.54402111, ..., -0.54402111,
#         -0.54402111, -0.54402111],
#       [-0.54402111, -0.54402111, -0.54402111, ..., -0.54402111,
#         -0.54402111, -0.54402111],
#       [-0.54402111, -0.54402111, -0.54402111, ..., -0.54402111,
#         -0.54402111, -0.54402111]]])


# One extremely notable aspect of NumPy is the manner in which it extends
# Python's list indexing functionality--especially with multidimensional
# arrays. To illustrate, make a simple two-dimensional array and try some
# experiments:


a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])

# array([[ 1, 2, 3, 4],
#         [ 5, 6, 7, 8],
#         [9, 10, 11, 12]])

# Select row 1
a[1]
# array([5, 6, 7, 8])

# Select column 1
a[:,1]
# array([2, 6, 10])

# Select a subregion and change it
a[1:3, 1:3]
# array([[ 6, 7],
#       [10, 11]])

a[1:3, 1:3] += 10

a
# array([[ 1, 2, 3, 4],
#       [ 5, 16, 17, 8],
#       [ 9, 20, 21, 12]])

# Broadcast a row vector across an operation on all rows
a + [100, 101, 102, 103]
# array([[101, 103, 105, 107],
#       [105, 117, 119, 111],
#       [109, 121, 123, 115]])

a
# array([[ 1, 2, 3, 4],
#       [5, 16, 17, 8],
#       [9, 20, 21, 12]])

# Conditional assignment on an array
np.where(a < 10, a, 10)
# array([[ 1, 2, 3, 4],
#       [ 5, 10, 10, 8],
#       [ 9, 10, 10, 10]])


# NumPy is the foundation for a huge number of science and engineering
# libraries in Python. It is also one of the largest and most complicated
# modules in widespread use. That said, it's still possible to accomplish
# useful things with NumPy by starting with simple examples and playing
# around.

# One note about usage is that it is relatively common to use the statement
# import numpy as np, as shown in the solution. This simply shortens the
# name to something that's more convenient to type over and over again in
# your program.

# For more in, go to http://www.numpy.org


# 10)
