####################################################
# 
# Bitcoin blocks
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
####################################################

from . import serialize
from . import script
from . import utils
from . import txn
import binascii

class blockHeader:
    
    def __init__(self, version = 0x20000000, prevBlockId = None, merkleRoot = None, creationTime = 0, bits = 0, nonce=0):
        self.version = version
        self.prevBlockId = prevBlockId
        self.merkleRoot = merkleRoot
        self.creationTime = creationTime
        self.bits = bits
        self.nonce = nonce
        
    
    def getVersion(self):
        return self.version
        
    def getPrevBlockId(self):
        return self.prevBlockId
        
    def getMerkleRoot(self):
        return self.merkleRoot
        
    def getCreationTime(self):
        return self.creationTime
        
    def getNonce(self):
        return self.nonce
        
    def getBits(self):
        return self.bits
        
    #
    # Deserialize a block header from the raw representation
    # Fields:
    # version number
    # hash value of previous block
    # Merkle root 
    # creation time in seconds since the epoch
    # bits - encoding the difficulty
    # nonce
    # see primitives/block.h
    #
    def deserialize(self,raw):
        self.version, raw = serialize.deserializeUint32(raw)
        self.prevBlockId, raw = serialize.deserializeString(raw, 32)
        self.merkleRoot, raw = serialize.deserializeString(raw, 32)
        self.creationTime, raw = serialize.deserializeUint32(raw)
        self.bits, raw = serialize.deserializeUint32(raw)
        self.nonce, raw = serialize.deserializeUint32(raw)
        return raw
        
    
    
    
