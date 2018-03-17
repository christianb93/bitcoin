####################################################
# 
# Some routines supporting serialization and 
# deserialization
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

####################################################

import binascii

#
# Decode a number and return the stream with 
# the number removed
#
def deserializeNumber(s, l):
    if len(s) < 2*l:
        raise TypeError("Input string too short")
    i = int.from_bytes(bytes.fromhex(s[0:2*l]), 'little') 
    s = s[2*l:]
    return i,s


#
# Decode a varInt. Returns:
# - the value
# - the remaining string
#    
def deserializeVarInt(s):
    #
    # See ReadCompactSize in serialize.h for the logic
    #
    if len(s) < 2:
        raise TypeError("Input string too short")
    i, s = deserializeNumber(s, 1)
    if i < 253:
        return i, s
    if i == 253:
        #
        # Read two extra bytes
        #
        b, s = deserializeNumber(s, 2)
    elif i == 254:
        b, s = deserializeNumber(s,4)
    elif i == 255:
        b, s = deserializeNumber(s, 8)
    else:
        raise TypeError("Invalid first byte (",i,") for varInt")
    return b, s


#
# Decode a char
# Returns:
# - the value
# - the remaining string
#
def deserializeChar(s):
    return deserializeNumber(s, 1)

#
# Decode a long int
# Returns:
# - the value
# - the remaining string
#
def deserializeUint32(s):
    return deserializeNumber(s, 4)

#
# Decode a long long
# Returns:
# - the value
# - the remaining string
#
def deserializeUint64(s):
    return deserializeNumber(s, 8)

#
# Decode a hex string of len bytes
# Returns:
# - the value as a hex string
# - the remaining string
#
def deserializeString(s, len):
    r = ""
    for _ in range(len):
        r = s[0:2] + r
        s = s[2:]
    return r, s
    
    
    
#
# Serialize a number
#
def serializeNumber(n, l = None, order="little"):
    if l == None:
        l = (n.bit_length() + 7) // 8
    n = n.to_bytes(l, order)
    return binascii.hexlify(n).decode('ascii')
    
    
#
# Encode a hex string of len bytes
#
def serializeString(s, len):
    r = ""
    for _ in range(len):
        r = s[0:2] + r
        s = s[2:]
    return r

#
# Serialize a varInt
#
def serializeVarInt(x):
    if x < 253:
        return serializeNumber(x, 1)
    else:
        if x > (2**16 - 1):
            #
            # Need at least four bytes. Find out whether
            # four bytes will do
            #
            if x > (2**32 - 1):
                if (x > (2**64 - 1)):
                    raise ValueError("Out of range for a varInt")
                #
                # No - need all eight bytes
                #
                s = "ff" + serializeNumber(x,8)    
            #
            # Can do it with four bytes
            # 
            else:
                s = "fe" + serializeNumber(x,4)
        else:
            # can do it with two bytes
            s = "fd" + serializeNumber(x,2)
        return s

#
# Encode a char
#
def serializeChar(x):
    return serializeNumber(x, 1)

#
# Encode a long int
#
def serializeUint32(x):
    return serializeNumber(x, 4)

#
# Encode a long long
#
def serializeUint64(x):
    return serializeNumber(x, 8)


