###################################################################
# 
# Elliptic curves
#
# Some code snippets to play with
# elliptic curves
# 
# MIT license
#
# Copyright (c) 2018 christianb93
# Permission is hereby granted, free of charge, to 
# any person obtaining a copy of this software and 
# associated documentation files (the "Software"), 
# to deal in the Software without restriction, 
# including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, 
# sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice 
# shall be included in all copies or substantial 
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY 
# OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS 
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
##################################################################

import math
import matplotlib.pyplot as plt 
import numpy as np


import ecdsa


#################################################
#
# Some utility functions to work with elliptic
# curves
#
#################################################


#
# Compute the inverse mod p using the extend 
# euclidian algorithm. 
# See O. Forster, Algorithmische Zahlentheorie
#
def inv_mod_p(x, p):
    if 1 != math.gcd(x, p):
        raise ValueError("Arguments not prime")
    q11 = 1
    q22 = 1
    q12 = 0
    q21 = 0
    while p != 0:
        temp = p
        q = x // p
        p = x % p
        x = temp
        t21 = q21
        t22 = q22
        q21 = q11 - q*q21
        q22 = q12 - q*q22
        q11 = t21
        q12 = t22
    return q11



#
# A class representing a point on the curve
#
class CurvePoint:
    
    def __init__(self, x, y, infinity = False):
        self.x = x
        self.y = y
        self.infinity = infinity
        self.p = p
        
    def __add__(self, other):
        #
        # Capture trivial cases - one of the points is infinity
        #
        if self.infinity:
            return other
        if other.infinity:
            return self
        #
        # First check whether we are adding or doubling
        #
        x1 = self.x
        x2 = other.x
        y1 = self.y
        y2 = other.y
        infinity = False
        if (x1 - x2) % p == 0:
            #
            # Are we talking about doubling or addition 
            # of the inverse?
            # 
            if (y1 + y2) % p == 0:
                infinity = True
                x3 = 0
                y3 = 0
            else:
                inv = inv_mod_p(2*y1, p)
                x3 = (inv*(3*x1**2 + a))**2 - 2*x1
                y3 = (inv*(3*x1**2 + a))*(x1 - x3) - y1
        else:
            #
            # Standard case
            #
            inv = inv_mod_p(x2 - x1, p)
            x3 = ((y2 - y1)*inv)**2 - x1 - x2
            y3 = (y2 - y1)*inv*(x1 - x3) - y1
        
        return CurvePoint(x3 % p, y3 % p, infinity)
        



#################################################
#
# Main
#
#################################################


#
# Define curve parameters 
#

p = 29
a = 4
b = 20
#
# and add a few points
#
A = CurvePoint(5,22)
B = CurvePoint(16, 27)
O = CurvePoint(0,0,infinity=True)
C = A + B
assert(C.x == 13)
assert(C.y == 6)
assert(C.infinity == False)
C = A + A
assert(C.x == 14)
assert(C.y == 6)
assert(C.infinity == False)
A = CurvePoint(17,19)
B = CurvePoint(17,10)
C = A + B
assert(C.infinity == True)
A = B + O
assert(A.x == B.x)
assert(A.y == B.y)
assert(A.infinity == B.infinity)
A = O + B
assert(A.x == B.x)
assert(A.y == B.y)
assert(A.infinity == B.infinity)



#
# Create a curve with parameters p,a and b
# with the ECDSA library
#
curve = ecdsa.ellipticcurve.CurveFp(p,a,b)
#
# Define two points and add them
#
A = ecdsa.ellipticcurve.Point(curve, 5, 22)
B = ecdsa.ellipticcurve.Point(curve, 16, 27)
C = A + B
assert(C.x() == 13)
assert(C.y() == 6)
assert(C != ecdsa.ellipticcurve.INFINITY)


#
# Two more points
#
A = ecdsa.ellipticcurve.Point(curve, 17, 19)
B = ecdsa.ellipticcurve.Point(curve, 17, 10)
C = A + B
assert(C == ecdsa.ellipticcurve.INFINITY)


#
# Next we play with signatures. First we get the standard curve
# and its parameters
#
curve = ecdsa.curves.SECP256k1
G = curve.generator
p = curve.curve.p()
a = curve.curve.a()
b = curve.curve.b()
n = G.order()
print("p = ", p)
print("n = ", n)

#
# Determine a private key and a public key
# 
d = ecdsa.util.randrange(n-1)
Q = d*G
pKey = ecdsa.ecdsa.Public_key(G, Q)
sKey = ecdsa.ecdsa.Private_key(pKey, d)


#
# Next we simulate a hash value
# and sign it
# 
h = ecdsa.util.randrange(n-1)
k = ecdsa.util.randrange(n-1)
signature = sKey.sign(h, k)
r = signature.r
s = signature.s


#
# Calculate this manually
#
_r = (k*G).x() % n
assert(_r == r)

w = inv_mod_p(k, n)
_s = ((h+d*r)*w) % n
assert(_s == s)

#
# Now we manually verify the signature
#
w = inv_mod_p(s, n)
assert(1 == (w*s % n))
u1 = w * h % n
u2 = w * r % n
X = u1*G + u2*Q
assert(X.x() == r)

#
# Finally we verify the signature using the
# lib
# 
assert(pKey.verifies(h, signature) == True)
