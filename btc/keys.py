#################################################################
# 
# Deal with private and public keys
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

from . import utils
import base64
import binascii
import hashlib

#
# Convert Base58Check encoded key to 
# a byte sequence representing the 32 byte 
# payload (the secret)
# 
# See base58.cpp for details on the encoding
#
#
def wif_to_payload_bytes(wif):
    #
    # Decode
    #
    decoded = utils.base58_decode(wif)
    assert(utils.base58_encode(decoded) == wif)
    #
    # The last four bytes are the checksum
    #
    checksum = decoded[-4:]
    msg = decoded[:-4]
    #
    # Verify the checksum - this should be the first
    # four bytes of the double sha256 hash
    #
    chk = utils.hash256(msg)[:4]
    if (chk != checksum):
        raise ValueError("Checksum not correct")
    #
    # The first byte is the version number - see
    # chainparams.h for allowed values
    #
    if (decoded[0] == 128):
        # Mainnet
        pass
    elif (decoded[0] == 239):
        # Testnet3 or regtest
        pass
    else:
        raise ValueError("Not a valid prefix: ", decoded[0])        
    #
    # If we use compression, the total length should be
    # 1 byte for the prefix
    # 32 bytes for the payload
    # 1 byte 0x01
    # 4 bytes checksum
    #
    if (len(decoded) != 38):
        raise ValueError("Unexpected length")
    payload = decoded[1:33] 
    return payload


#
# Convert WIF encoded private key to a number
# (the actual secret)
#
def wif_to_payload(wif):
    b = wif_to_payload_bytes(wif)
    d = int.from_bytes(b, byteorder ="big")
    return d
    


#
# Convert a private key stored as a number to a WIF
#
def payload_value_to_wif(v, version):
    #
    # First convert the private key to a byte sequence
    # using big endian encoding
    #
    s = v.to_bytes(32, byteorder='big')
    #
    # Now add the version number 
    #
    s = version.to_bytes(1, 'big') + s
    #
    # and 0x01 (compression) at the end
    # 
    s = s + bytes.fromhex("01")
    #
    # Get the first four bytes of the checksum
    #
    chk = utils.hash256(s)[:4]
    #
    # and append them
    #
    s = s + chk
    return utils.base58_encode(s)

#
# Extract the public points (x,y) from a
# PEM and return them as byte sequences
# We assume that the PEM contains the public
# key in the compressed format
# Input: the PEM as byte sequence
# Outputs: X and Y as byte sequences
# 
def public_point_from_pem(pem):
    #
    # Remove the first and last line and all
    # line breaks to extract the DER encoded part
    #
    der_end = pem.index(b'\n-----END')
    der_start = pem.index(b'\n') + 1
    der = pem[der_start : der_end]
    der = der.replace(b'\n',b'')
    der = base64.b64decode(der)
    # 
    # The result will be a DER / ASN.1 encoded sequence
    # according to X.208).
    # RFC5480 specifies this as follows:
    # SubjectPublicKeyInfo = [[algorithm_OID, curve_OID], subjectPublicKey]
    # where subjectPublicKey is a bit string
    # Thus the first byte is 0x30 for a sequence
    # and the second byte is the length of the sequence
    #
    slen = len(der) - 2
    assert(der[0] == 0x30)
    assert(der[1] == slen)
    #
    # Remove this part
    #
    der = der[2:]
    #
    # There is one more sequence of length 16
    #
    assert(der[0] == 0x30)
    assert(der[1] == 16)
    der = der[2:]

    #
    # The next 12 bytes are the OID of the 
    # algorithm. From RFC5480
    # id-ecPublicKey OBJECT IDENTIFIER ::= {
    #  so(1) member-body(2) us(840) ansi-X9-62(10045) keyType(2) 1 }
    # Use an encoder like
    # https://misc.daniel-marschall.de/asn.1/oid-converter/online.php
    # to convert this
    if der[0:9] != b'\x06\x07\x2a\x86\x48\xce\x3d\x02\x01':
        raise ValueError("OID is not ECDSA")
    #
    # and the next 6 bytes are the OID of the curve
    # This should be the OID SECP256k1
    #
    der = der[9:]
    if der[0:7] != b'\x06\x05\x2b\x81\x04\x00\n':
        raise ValueError("Curve is not SECP256k1")
    der=der[7:]
    #
    # Next we have a bit string (the subjectPublicKey)
    # with length 66. A bit string
    # is marked by 0x3, followed by
    # the length and the padding count which is the first
    # content octet. As the bit string 
    # in this case is the result of a conversion from an 
    # octet string, the padding is zero
    #
    if der[0] != 0x3:
        raise ValueError("Should have a bitstring at this point")
    if der[1] != (len(der) - 2):
        raise ValueError("Wrong number of content octets")
    if der[2] != 0:
        raise ValueError("Padding should be zero")
    der = der[3:]
    #
    # According to RFC5480, the first byte specifies whether compression
    # is used - we expect no compression
    #
    if der[0] != 0x04:
        raise ValueError("Did not expect compression")
    points = der[1:]
    assert(len(points) == 64)
    X = points[0:32]
    Y = points[32:]
    return X, Y

#
# Given a non-compressed hex representation of a point on 
# the curve, (65 bytes string), extract
# the points X and Y as integers
#
def ec_point_hex_to_values(point):
    # 
    # Convert to bytes
    #
    _point = bytes.fromhex(point)
    if (_point[0] != 0x4):
        raise ValueError("Expected uncompressed value")
    _point = _point[1:]
    assert(64 == len(_point))
    _x = _point[:32]
    _y = _point[32:]
    x = int.from_bytes(_x, 'big')
    y = int.from_bytes(_y, 'big')
    return x,y


#
# Given a point with coordinates (X,Y) as integers,
# convert to a compressed representation as bytes
#
def ec_point_compress(X,Y):
    _X = X.to_bytes(32, 'big')
    if (Y % 2) == 1:
        _X = b'\x03' + _X
    else:
        _X = b'\x02' + _X
    return _X


#
# Given a point with coordinates (X,Y) as integers,
# convert to a compressed representation as hex
#
def ec_point_compress_hex(X,Y):
    return binascii.hexlify(ec_point_compress(X,Y)).decode('ascii')
    
#
# Given a hex representation of a public key,
# determine the address in base58 check encoding
#
def ec_address(hex_key, version):
    s = bytes.fromhex(hex_key)
    adr = utils.hash160(s)
    #
    # Add prefix 0x0 for a bitcoin address in mainnet
    # and prefix b'o' in testnet3 and regtest
    #
    if version == 239:
        #Testnet
        adr = b'o'  + adr
    elif version == 180:
        # Mainnet
        adr = (0).to_bytes(1, 'big')  + adr
    else:
        raise ValueError("Unknown version: ", version)
    #
    # Now we have the address as a sequence of bytes. We now do
    # base58check encoding
    # 
    chk = utils.hash256(adr)[:4]
    adr = adr + chk
    return utils.base58_encode(adr)

#
# Given a bitcoin address, get a hash160 of the
# public key 
#
def ec_address_to_pkh(address):
    #
    # First decode and strip off the checksum
    #
    decoded = utils.base58_decode(address)
    checksum = decoded[-4:]
    msg = decoded[:-4]
    #
    # Verify the checksum - this should be the first
    # four bytes of the double sha256 hash
    #
    chk = utils.hash256(msg)[:4]
    if (chk != checksum):
        raise ValueError("Checksum not correct")
    #
    # Remove address prefix
    #
    return msg[1:]
