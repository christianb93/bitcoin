###############################################
# 
# Utility functions 
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
###############################################

import hashlib
import requests

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

###############################################
# Some standard hash function 
###############################################


#
# In the bitcoin terminology, the term hash160 refers to
# a double hash: we apply SHA256 first, then followed by
# RIPEMD160
#
# see hash.h in the reference implementation
#
def hash160(s):
    _sha256 = hashlib.sha256(s).digest()
    return hashlib.new("ripemd160", _sha256).digest()

#
# A double SHA256 hash
#
def hash256(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


###############################################
# Convert to and from base58
###############################################


#
# Encode a sequence of bytes as Base58
# and return the corresponding sequence of characters
#
# see base58.cpp 
#
def base58Encode(s):
    assert(isinstance(s, bytes))
    #
    # Count the number of leading zeros
    #
    zeros = 0
    while (zeros < len(s)) and (s[zeros] == 0):
        zeros = zeros + 1
    #
    # Convert to integer first, using big endian encoding
    #
    value = int.from_bytes(s, 'big')
    #
    # Now convert the integer to base 58
    #
    result= ""
    while value:
        value, digit = divmod(value, 58)
        result = BASE58_ALPHABET[digit] + result
    #
    # Append leading 1's again
    #
    for _ in range(zeros):
        result = '1' + result
    return result

#
# Decode a Base58 encoded string and return a
# sequence of bytes
#
def base58Decode(s):
    #
    # Strip off leading 1's as these represent leading
    # zeros in the original
    #
    zeros = 0
    while (zeros < len(s)) and (s[zeros] == '1'):
        zeros = zeros + 1
    s = s[zeros:]
    #
    # We first turn the string into an integer
    #
    value, power = 0, 1
    for _ in reversed(s):
        value += power * BASE58_ALPHABET.index(_)
        power = power * 58
    #
    # Now convert this integer into a sequence of bytes
    # 
    result = value.to_bytes((value.bit_length() + 7) // 8, byteorder='big')
    #
    # and append the leading zeros again
    #
    for _ in range(zeros):
        result = (0).to_bytes(1, 'big') + result
    return result



###############################################
# DER signatures
###############################################

#
# Validate a DER signature according to the rules
# defined in the reference implementation in 
# script/integer.cpp, IsValidSignatureEncoding
#
def isValidDERSignature(s):
    b = bytes.fromhex(s)
    if len(b) < 9:
        return False
    if len(b) > 73:
        return False
    #
    # A signature is a DER sequence, so it should 
    # start with the type code 0x30
    #    
    if b[0] != 0x30:
        return False
    # 
    # Next field should be the length, not including the
    # last byte (hashtype) and the two initial bytes
    # 
    if b[1] != (len(b) - 3):
        return False
    #
    # R and S are encoded as integers, both starting 
    # with the type code 0x02 followed by the length
    # in bytes
    #
    lenR = b[3]
    lenS = b[5 + lenR]

    if (5 + lenR >= len(b)):
        return False;

    if (lenR + lenS + 7) != len(b):
        return False        

    if b[2] != 0x02:
        return False

    if b[lenR + 4] != 0x02: 
        return False

    #
    # For both R and S, the first byte should not
    # have its most significant bit set (as this
    # would indicate a negative number). Thus the
    # the leading byte should be zero in this case
    # - and in fact only in this case
    #
    if (b[4] & 0x80): 
        return False    
    if lenR > 1:
        if (b[4] == 0x00) and not (b[5] & 0x80):
            return False

    if (b[lenR + 6] & 0x80):
        return False
    if lenS > 1:
        if (b[lenR + 6] == 0x00) and not (b[lenR + 7] & 0x80):
            return False

    return True
    
    
#################################################
#
# Utility function to get a transaction in raw
# format from bitcoin.info
#
#################################################

def getRawTransaction(txid):
    url = 'https://blockchain.info/en/tx/' + txid + '?format=hex'
    r = requests.get(url)
    return r.text

#################################################
#
# Utility function to submit an RPC method call
# to a bitcoin server
#
#################################################

def rpcCall(method, params = None, port=18332, host="localhost", user="user", password="password"):
    #
    # Create request header
    #
    headers = {'content-type': 'application/json'}
    #
    # Build URL from host and port information
    #
    url = "http://" + host + ":" + str(port)
    #
    # Assemble payload as a Python dictionary
    # 
    payload = {"method": method, "params": params, "jsonrpc": "2.0", "id": 1}        
    #
    # Create and send POST request
    #
    r = requests.post(url, json=payload, headers=headers, auth=(user, password))
    #
    # and interpret result
    #
    json = r.json()
    if 'result' in json and json['result'] != None:
        return json['result']
    elif 'error' in json:
        raise ConnectionError("Request failed with RPC error", json['error'])
    else:
        raise ConnectionError("Request failed with HTTP status code ", r.status_code)
        

