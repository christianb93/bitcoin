####################################################
# 
# Bitcoin transactions
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
import binascii

#
# A transaction input. This is the part of a transaction that
# links back to a previous transaction
#
# see primitives/transaction.h in the reference implementation
#
class txin:
	
    def __init__(self, prevTxid = None, vout = 0, scriptSig = None, sequence = 0xfffffffe):
        self.prevTxid = prevTxid
        self.vout = vout
        self.scriptSigHex = None
        self.scriptSig = scriptSig
        self.sequence = sequence	
        #
        # if possible fill the hex representation 
        # 	
        if scriptSig != None:
            if scriptSig.getScriptType() != script.SCRIPTTYPE_OTHER:
                self.scriptSigHex = scriptSig.serialize()
    
    #
    # Get the id (hash value) of the previous transaction
    #
    def getPrevTxId(self):
        return self.prevTxid
    
    #
    # Get the index of the previous transaction output
    # 
    def getVout(self):
        return self.vout
    
    #
    # Get the signature script as a hex string
    #
    def getScriptSigHex(self):
        return self.scriptSigHex

    #
    # Get the signature script as an object
    #
    def getScriptSig(self):
        return self.scriptSig


    #
    # Get the sequence number
    #
    def getSequence(self):
        return self.sequence
    
    
    #
    # Deserialize a string and initalize the
    # transaction input accordingly
    #
    # see TxIn::SerializeOp in the reference implementation
    #
    def deserialize(self, s):
        #
        # Read the previous transaction ID first. The transaction
        # ID is a 32 byte hex string
        #
        self.prevTxid, s = serialize.deserializeString(s, 32)
        #
        #
        # Next there is the index of the txout in the
        # previous transaction that we refer to
        #  
        self.vout, s = serialize.deserializeUint32(s)   
        #
        #
        # Then there is the signature script, first
        # the length in bytes, then the hex representation
        # of the script itself
        #
        script_len, s = serialize.deserializeVarInt(s)
        self.scriptSigHex = s[0:2*script_len]
        self.scriptSig = script.scriptSig()
        self.scriptSig.deserialize(self.scriptSigHex)
        s = s[2*script_len:]   
        #
        # finally the sequence field
        #
        self.sequence, s = serialize.deserializeUint32(s)
        return s
        
        
    # 
    # Is this a coinbase transaction?
    #
    def isCoinbase(self):
        for _ in range(32):
            if self.prevTxid[_] != '0':
                return False
        return True
        
    #
    # Serialize the transaction input
    #
    # see TxIn::SerializeOp in the reference implementation
    #
    def serialize(self):
        if self.prevTxid == None:
            return ""
        if len(self.prevTxid) != 64:
            raise ValueError("Invalid previous transaction id - wrong length")
        s = ""
        #
        #  Previous transaction id
        #
        s = s + serialize.serializeString(self.prevTxid, 32)
        #
        # and its index
        # 
        s = s + serialize.serializeUint32(self.vout)
        #
        #  
        # Then there is the signature script, first
        # the length in bytes, then the hex representation
        # of the script itself
        if self.scriptSig == None:
            return ""
        if self.scriptSig.getScriptType() != script.SCRIPTTYPE_OTHER:
            scriptSigHex = self.scriptSig.serialize()
        elif self.scriptSigHex != None:
            scriptSigHex = self.scriptSigHex
        else:
            raise ValueError("Do not have hex representation of the signature script")
        s = s + serialize.serializeVarInt(int(len(scriptSigHex) / 2))
        s = s + scriptSigHex
        #
        # Finally the locktime
        #
        s = s + serialize.serializeUint32(self.sequence)
        return s


        

    
#
# A transaction output
#
# see again primitives/transaction.h
#
class txout:

    def __init__(self, value = None, scriptPubKey = None):
        self.value = value
        self.scriptPubKeyHex = None
        self.scriptPubKey = scriptPubKey
        if scriptPubKey != None:
            if scriptPubKey.getScriptType() != script.SCRIPTTYPE_OTHER:
                self.scriptPubKeyHex = scriptPubKey.serialize()

    #
    # Deserialize a string and initalize the
    # transaction output accordingly
    #
    # see TxOut::SerializeOp 
    #
    def deserialize(self, s):    
        # 
        # First eight bytes are the value in Satoshi
        # 
        self.value, s = serialize.deserializeUint64(s)
        #
        # Then there is the public key script - length
        # and hex representation
        #
        script_len, s = serialize.deserializeVarInt(s)
        self.scriptPubKeyHex = s[0:2*script_len]
        self.scriptPubKey = script.scriptPubKey()
        self.scriptPubKey.deserialize(self.scriptPubKeyHex)
        return s[2*script_len:]
     
    
    #
    # Get value in satoshi
    #
    def getValue(self):
        return self.value

    
    #
    # Get the public key script as a hex string
    #
    def getScriptPubKeyHex(self):
        return self.scriptPubKeyHex
    
    
    #
    # Get the public key script
    #
    def getScriptPubKey(self):
        return self.scriptPubKey
        
    #
    # Serialize
    #
    def serialize(self):
        # 
        # Each txout starts with the amount, which is a 64 bit
        # integer (i.e. 8 bytes, 16 characters) which
        # specifies the amount in satoshis
        #
        if self.value == None:
            return ""
        s = serialize.serializeUint64(self.value)
        #
        # Next there is the scriptPubKey, preceeded by its length
        #   
        if self.scriptPubKey == None:
            return ""
        if self.scriptPubKey.getScriptType() != script.SCRIPTTYPE_OTHER:
            scriptPubKeyHex = self.scriptPubKey.serialize()
        elif self.scriptPubKeyHex != None:
            scriptPubKeyHex = self.scriptPubKeyHex
        else:
            raise ValueError("Could not determine hex representation of script")
        s = s + serialize.serializeVarInt(int(len(scriptPubKeyHex) / 2))
        s = s + scriptPubKeyHex
        return s
    
#
# A transaction 
#
class txn:
    
    def __init__(self, version = 2, locktime = 0):
        self.version = version
        self.inputs = []
        self.outputs = []
        self.locktime = locktime

    #
    # Get the version
    #
    def getVersion(self):
        return self.version
    
    #
    # Get the inputs
    #
    def getInputs(self):
        return self.inputs
    
    #
    # Get the outputs
    #
    def getOutputs(self):
        return self.outputs
    
    
    #
    # Get the locktime
    #
    def getLocktime(self):
        return self.locktime

    
    #
    # Build the transaction from a string. See the function
    # SerializeTransaction in primitives/transaction.h
    #
    def deserialize(self, s):
        #
        # The first four bytes are the version number
        #
        version, vin_str = serialize.deserializeUint32(s)
        if ((version != 1) and (version != 2)):
            raise ValueError("Unknown version number")
        self.version = version
        #
        # Next there is the number of input transactions, followed
        # by the input transactions themselves
        #
        self.inputs =  []
        no_in, vin_str = serialize.deserializeVarInt(vin_str)
        for i in range(no_in):
            vin = txin()
            vin_str = vin.deserialize(vin_str)
            self.inputs.append(vin)
        #
        # do the same for the outgoing transactions
        #
        no_out, vout_str = serialize.deserializeVarInt(vin_str)    
            
        self.outputs = []
        for i in range(no_out):
            vout = txout()
            vout_str = vout.deserialize(vout_str)
            self.outputs.append(vout)
        
        #
        # Last field is the locktime
        #
        self.locktime, vout_str = serialize.deserializeUint32(vout_str)
        
        
    #
    # Serialize the transaction
    #
    def serialize(self):
        s = serialize.serializeUint32(self.version)
        s = s + serialize.serializeVarInt(len(self.inputs))
        for txin in self.inputs:
            s = s + txin.serialize()
        s = s + serialize.serializeVarInt(len(self.outputs))
        for txout in self.outputs:
            s = s + txout.serialize()
        s = s + serialize.serializeUint32(self.locktime)
        return s
        
    #
    # Derive the transaction ID
    #
    def getTxnId(self):
        h = utils.hash256(bytes.fromhex(self.serialize()))
        h = binascii.hexlify(h).decode('ascii')
        #
        # Reverse bytewise
        # 
        s = ""
        for i in range(32):
            s = h[0:2] + s
            h = h[2:]
        return s
        
    #
    # Add an input
    #
    def addInput(self, _txin):
        assert(isinstance(_txin, txin))
        self.inputs.append(_txin)

    #
    # Add an outupt
    #
    def addOutput(self, _txout):
        assert(isinstance(_txout, txout))
        self.outputs.append(_txout)
