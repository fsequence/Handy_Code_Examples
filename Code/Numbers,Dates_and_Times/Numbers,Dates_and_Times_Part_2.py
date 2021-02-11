
# Numbers, Dates and Times Part 2
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


# 5) Packing and Unpacking Large Integers from Bytes
# 6)
# 7)
# 8) Calculating with Fractions
# 9)


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


# 9)
