###################################################################
# 
# Playing with bitcoin keys
#
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


import binascii
import btc.utils
import hashlib

def hash256(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


#
# The WIF encoded private key
#
wif = "cVDUgUEahS1swavidSk1zdSHQpCy1Ac9XSQHkaxmZKcTTfEA5vTY"
print("WIF:       ", wif)
#
# Convert into a sequence of bytes
#
b = btc.utils.base58_decode(wif)
#
# and into hex
#
h = binascii.hexlify(b).decode('ascii')
print("Hex:       ", h)
#
# Strip off checksum
#
chk = h[-8:]
print("Checksum:  ", chk)
h = h[:-8]
#
# and verify it
#
_chk = hash256(bytes.fromhex(h))[:4]
assert(_chk == bytes.fromhex(chk))
#
# Strip off version byte
#
print("Version:   ", int(h[:2], 16))
h = h[2:]
#
# and compression flag
#
h = h[:-2]

d = int.from_bytes(bytes.fromhex(h), "big")
print("Secret:    ", d)

