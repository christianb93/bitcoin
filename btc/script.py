####################################################
# 
# Bitcoin scripts
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
from . import txn
from . import utils
from . import keys

import binascii
import ecdsa
import random


OP_PUSHDATA1 = 0x4c
OP_DUP = 0x76
OP_CHECKSIG = 0xac
OP_HASH160 = 0xa9
OP_EQUALVERIFY = 0x88


SCRIPTTYPE_P2PKH = "P2PKH"
SCRIPTTYPE_P2PK = "P2PK"
SCRIPTTYPE_OTHER = "OTHER"

SIGHASHTYPE_ALL = 1

class scriptSig:
    
    def __init__(self, scriptType = SCRIPTTYPE_OTHER, r = None, s = None, pubKeyHex = None, hashType = 1):
        self.scriptType = scriptType
        self.r = r
        self.s = s
        self.pubKeyHex = pubKeyHex
        self.hashType = hashType
        self.data = ""
        if scriptType == SCRIPTTYPE_P2PKH:
            if (pubKeyHex == None):
                raise ValueError("Need to provide public key for this script type")
        if scriptType != SCRIPTTYPE_OTHER:
            if (r == None) or (s == None):
                raise ValueError("Need to provide r and s for this scripttype")
        
        
    def getScriptType(self):
        return self.scriptType


    def getSignatureR(self):
        if self.scriptType == SCRIPTTYPE_OTHER:
            raise TypeError("Not a P2PK or P2PKH script")
        else:
            return self.r
            
    def getSignatureS(self):
        if self.scriptType == SCRIPTTYPE_OTHER:
            raise TypeError("Not a P2PK or P2PKH script")
        else:
            return self.s
                        
        
    def getPubKeyHex(self):
        if self.scriptType != SCRIPTTYPE_P2PKH:
            raise TypeError("Not a P2PKH script")
        else:
            return self.pubKeyHex
        
    def getHashType(self):
        return self.hashType
        
    
    #
    # Append data (implicit push)
    #
    def pushData(self, s):
        l = len(s)
        if l >=OP_PUSHDATA1:
            raise ValueError("Input too long, non-implicit pushes not supported")
        if 1 == (l % 2):
            raise ValueError("Input must have even length")
        self.data += serialize.serializeChar(l // 2) + s
    
    
    def deserialize(self, s):
        opcode, s = serialize.deserializeChar(s)
        if (opcode >= OP_PUSHDATA1):
            self.scriptType = SCRIPTTYPE_OTHER
            return
        #
        # Opcode < OP_PUSHDATA1, so it is the length of data
        # that we need to push to the stack
        # 
        der_signature = s[0:2*opcode]
        s = s[2*opcode:]
        #
        # We expect this to be a DER signature
        #
        if der_signature[0:2] != "30":
            self.scriptType = SCRIPTTYPE_OTHER
            return
        der_signature = der_signature[2:]
        #
        # The next byte should be the byte length of the entire
        # array, excluding the byte that we just read and excluding
        # the hash type
        #
        l, der_signature = serialize.deserializeChar(der_signature)
        #
        # Next byte should be 02 for integer
        #
        if der_signature[0:2] != "02":
            self.scriptType = SCRIPTTYPE_OTHER
            return
        der_signature = der_signature[2:]
        #
        # Read length and r (which is a big endian which is DER standard)
        #
        l, der_signature = serialize.deserializeChar(der_signature)
        sign_r = der_signature[0:l*2]
        sign_r_int = int.from_bytes(bytes.fromhex(sign_r), 'big')
        der_signature = der_signature[2*l:]
        #
        # Next byte should be 02 for integer
        #
        if der_signature[0:2] != "02":
            self.scriptType = SCRIPTTYPE_OTHER
            return
        der_signature = der_signature[2:]    
        l, der_signature = serialize.deserializeChar(der_signature)
        sign_s = der_signature[0:2*l]
        sign_s_int = int.from_bytes(bytes.fromhex(sign_s), 'big')
        der_signature = der_signature[2*l:]
        #
        # last byte is the hash type - see 
        # TransactionSignatureCreator::CreateSig
        #
        if len(der_signature) != 2:
            self.scriptType = SCRIPTTYPE_OTHER
            return
        self.hashType = int.from_bytes(bytes.fromhex(der_signature), "big")
        if s == "":
            #
            # Output was a Pay-to-public-key so there is no
            # public key here
            self.scriptType = SCRIPTTYPE_P2PK
        else:
            #
            # Now the remaining part should start with an opcode again
            # 
            opcode, s = serialize.deserializeChar(s)
            if (opcode >= 0x4c):
                self.scriptType = SCRIPTTYPE_OTHER
                return    
            #
            # Remaining part is compressed pub key
            #
            if len(s) != 66:
                self.scriptType = SCRIPTTYPE_OTHER
                return   
            self.scriptType = SCRIPTTYPE_P2PKH
            self.pubKeyHex = s
            
        self.r = sign_r_int
        self.s = sign_s_int
        
        
    def serialize(self):
        if (self.scriptType != SCRIPTTYPE_P2PK) and (self.scriptType != SCRIPTTYPE_P2PKH):
            #
            # Only return data has explicitly been pushed
            #
            return self.data
        scriptSig = ""
        #
        # First opcode is the length - so we do this
        # not now but when we are done with everything else
        # First we create a DER representation of the private key
        # R and S are both represented by 02 - the DER code for an integer -
        # followed by their values in big endian encoding
        #
        r_str = serialize.serializeNumber(self.r, order="big")
        s_str = serialize.serializeNumber(self.s, order="big")
        #
        # DER requires that the first byte has its highest bit not set, as otherwise
        # this would be interpreted as an integer. So if this is the case, we would 
        # have to append a leading zero byte
        #
        r_first = int(r_str[0:2], 16)
        s_first = int(s_str[0:2], 16)
        if r_first & 0x80:
            r_str = "00" + r_str
        if s_first & 0x80:  
            s_str = "00" + s_str            
        scriptSig = "02" + serialize.serializeChar(int(len(r_str) / 2)) + r_str
        scriptSig = scriptSig + "02" + serialize.serializeChar(int(len(s_str) / 2)) + s_str
        #
        # Now add length and 0x30 - the DER type code for a sequence. We have not yet added
        # the hashtype, so the length we need to decode is the current length in bytes
        #
        scriptSig = "30" + serialize.serializeChar(int(len(scriptSig) / 2)) + scriptSig
        #
        # Add hashtype
        #
        scriptSig = scriptSig + serialize.serializeChar(self.hashType)
        #
        # finally add opcode for push data which is simply the length
        #
        scriptSig = serialize.serializeChar(int(len(scriptSig) / 2)) + scriptSig
        #
        # Now we are done with the first push operation. If this is a P2PK 
        # script we are done
        # 
        if (self.scriptType == SCRIPTTYPE_P2PK):
            return scriptSig
        #
        # Otherwise we need to push the pub key
        # 
        scriptSig = scriptSig + serialize.serializeChar(int(len(self.pubKeyHex) / 2))
        scriptSig = scriptSig + self.pubKeyHex
        return scriptSig
            
        
        
        
class scriptPubKey():
    
    def __init__(self, scriptType = SCRIPTTYPE_OTHER, pubKeyHex = None, pubKeyHash = None):
        self.scriptType = scriptType
        self.pubKeyHex = pubKeyHex
        self.pubKeyHash = pubKeyHash
        if scriptType == SCRIPTTYPE_P2PK:
            #
            # for P2PK, we need a pubKey
            #
            if pubKeyHex == None:
                raise ValueError("Need public key for this script type")
        if scriptType == SCRIPTTYPE_P2PKH:
            #
            # for P2PKH, we need a pubKey hash
            #
            if pubKeyHash == None:
                raise ValueError("Need public key hash for this script type")
                
    #
    # Get the script type
    #    
    def getScriptType(self):
        return self.scriptType
    
    
    #
    # Get the public key as hex string (compressed)
    #
    def getPubKeyHex(self):
        if self.scriptType != SCRIPTTYPE_P2PK:
            raise TypeError("No P2PK script")
        return self.pubKeyHex


    #
    # Get the public key hash as hex string (
    #
    def getPubKeyHash(self):
        if self.scriptType != SCRIPTTYPE_P2PKH:
            raise TypeError("No P2PKH script")
        return self.pubKeyHash
        
        
    
    def deserialize(self,s):
        opcode, s = serialize.deserializeChar(s)
        if opcode == 33:
            #
            # Could be a P2PK script
            #
            pubKeyHex = s[:66]
            s = s[66:]
            #
            # the next opcode should then be OP_CHECKSIG
            # 
            opcode, s = serialize.deserializeChar(s)
            if opcode != OP_CHECKSIG:
                self.scriptType = SCRIPTTYPE_OTHER
                return
            self.scriptType = SCRIPTTYPE_P2PK
            self.pubKeyHex = pubKeyHex
            return
        if opcode != OP_DUP:
            #
            # Give up if this is not OP_DUP
            #
            self.scriptType = SCRIPTTYPE_OTHER
            return
        #
        # Now we expect OP_HASH160
        # 
        opcode, s = serialize.deserializeChar(s)
        if opcode != OP_HASH160:
            self.scriptType = SCRIPTTYPE_OTHER
            return
        #
        # Next we should push the pubkey hash on the stack,
        # which has 20 bytes
        # 
        opcode, s = serialize.deserializeChar(s)
        if opcode != 20:
            self.scriptType = SCRIPTTYPE_OTHER
            return
        pubKeyHash = s[0:40]
        s = s[40:]
        #
        # Now there should be OP_EQUALVERIFY
        #
        opcode, s = serialize.deserializeChar(s)
        if opcode != OP_EQUALVERIFY:
            self.scriptType = SCRIPTTYPE_OTHER
            return
        #
        # and OP_CHECKSIG
        #
        opcode, s = serialize.deserializeChar(s)
        if opcode != OP_CHECKSIG:
            self.scriptType = SCRIPTTYPE_OTHER
            return
        self.scriptType = SCRIPTTYPE_P2PKH
        self.pubKeyHash = pubKeyHash
    
    #
    # Serialize the script
    # 
    def serialize(self):
        #
        # Can only serialize a standard script
        #
        if self.scriptType == SCRIPTTYPE_OTHER:
            return ""
        #
        # If this is a P2K script, simply push
        # the public key
        #
        if self.scriptType == SCRIPTTYPE_P2PK:
            s = serialize.serializeChar(33)
            s = s + self.pubKeyHex
        else:
            
            #
            # P2KH. First op is OP_DUP
            #
            s = serialize.serializeChar(script.OP_DUP)
            #
            # Now we need OP_HASH160
            # 
            s = s + serialize.serializeChar(script.OP_HASH160)
            #
            # Next we should push the pubkey hash on the stack,
            # which has 20 bytes
            # 
            s = s + serialize.serializeChar(20)
            s = s + self.pubKeyHash
            #
            # Now there should be OP_EQUALVERIFY
            #
            s = s + serialize.serializeChar(script.OP_EQUALVERIFY)
        #
        # Finally there is OP_CHECKSIG
        #
        s = s + serialize.serializeChar(script.OP_CHECKSIG)
        return s
    
    


#
# Given a transaction, determine the string that will be hashed and
# signed to obtain a signature for a specific transaction input. Note
# that different inputs require different signatures, as they can refer
# to unspent outputs with different public keys
# Inputs:
# tx - the transaction to be signed 
# nInput - the index of the input within the transaction for which the
#          signature is created
# scriptPubKey - the public key script of the output to which this 
#                input refers
def serializeForSigning(tx, nInput, scriptPubKey):
    if not isinstance(tx, txn.txn):
        raise  TypeError("Expecting transaction")
    if not isinstance(nInput, int):
        raise TypeError("Expecting integer")
    if not isinstance(scriptPubKey, script.scriptPubKey):
        raise TypeError("Need public key script here")        
    #
    # Version
    #
    s = serialize.serializeUint32(tx.getVersion())
    #
    # Number of input transactions
    #
    s = s + serialize.serializeVarInt(len(tx.getInputs()))
    #
    # Each individual input transaction
    #
    i = 0
    for txin in tx.getInputs():
        s = s + serializeTxinForSigning(txin, nInput, i, scriptPubKey) 
        i += 1
    #
    # Now do the outputs
    #
    s = s + serialize.serializeVarInt(len(tx.getOutputs()))
    for txout in tx.getOutputs():
        s = s + txout.serialize()
    #
    # and the locktime
    #
    s = s + serialize.serializeUint32(tx.getLocktime())
    #
    # plus SIGHASH_ALL
    #
    s = s + serialize.serializeUint32(SIGHASHTYPE_ALL)    
    return s
    
    
def serializeTxinForSigning(txin, nInput, index, scriptPubKey):
    s = ""
    #
    # Previous transaction id
    #
    prev_txid = txin.getPrevTxId()
    s = s + serialize.serializeString(prev_txid, 32)
    #
    # and its index
    #
    vout = txin.getVout()
    s = s + serialize.serializeUint32(vout)
    #
    # Now we use serialized pubKeyScript
    # of the corresponding output if nInput = index and
    # a blank otherwise
    #
    if nInput == index:
        scriptPubKeyHex = scriptPubKey.serialize()
    else:
        scriptPubKeyHex = ""
    s = s + serialize.serializeChar(int(len(scriptPubKeyHex) / 2)) + scriptPubKeyHex
    #
    # finally the sequence
    #
    s = s + serialize.serializeUint32(txin.getSequence())
    return s

#
# Build a hash value for a transaction tx which 
# can be used to sign the input with index nInput
# The third argument should be the transaction output
# that is spent with this input
#
def signatureHash(tx, nInput, spentOutput):
    if not isinstance(tx, txn.txn):
        raise  TypeError("Expecting transaction")
    if not isinstance(nInput, int):
        raise TypeError("Expecting integer")
    if not isinstance(spentOutput, txn.txout):
        raise  TypeError("Expecting transaction output")
    
    h = serializeForSigning(tx, nInput, spentOutput.getScriptPubKey())
    return utils.hash256(bytes.fromhex(h))
    

#
# Verify the signature of a transaction input
# Input:
# tx - the transaction that we want to verify
# nInput - the index of the input that we want to verify
# spentOutput - the output spent by this input
#
def verifySignature(tx, nInput, spentOutput):
    if not isinstance(tx, txn.txn):
        raise  TypeError("Expecting transaction")
    if not isinstance(nInput, int):
        raise TypeError("Expecting integer")
    if not isinstance(spentOutput, txn.txout):
        raise  TypeError("Expecting transaction output")

    #
    # Determine hash256 and interpret it as a big endian integer (according to the
    # standards, for instance SEC1, section 2.3.7, a hash string is converted to 
    # a number using big endian encoding)
    #
    h = int.from_bytes(signatureHash(tx, nInput, spentOutput), "big")
    #
    # Get signature
    #
    txin = tx.getInputs()[nInput]
    r = txin.getScriptSig().getSignatureR()
    s = txin.getScriptSig().getSignatureS()
    #
    # Get standard curve and generator
    #
    curve = ecdsa.curves.SECP256k1
    G = curve.generator
    p = curve.curve.p()
    #
    # Determine the x and y coordinate of the public key
    #
    if txin.getScriptSig().getScriptType() == "P2PKH":
        pubKey = txin.getScriptSig().getPubKeyHex()
    else:
        #
        # use previous output and extract from there
        #
        pubKey = spentOutput.getScriptPubKey().getPubKeyHex()
    x = int.from_bytes(bytes.fromhex(pubKey[2:66]), 'big')
    y = ecdsa.numbertheory.square_root_mod_prime((x**3 +7) % p , p)
    if pubKey[0:2] == "02":
        #
        # y should be even
        # 
        if 1 == (y % 2):
            y = (p - y) % p
    else:
        #
        # y should be odd
        # 
        if 0 == (y % 2):
            y = (p - y) % p
    assert(curve.curve.contains_point(x, y))
    Q = ecdsa.ellipticcurve.Point(curve.curve, x, y)
    pKey = ecdsa.ecdsa.Public_key(G, Q)
    signature = ecdsa.ecdsa.Signature(r,s)
    return pKey.verifies(h, signature)

#
# Sign a transaction. Given the transaction txn,
# a list of unspent transaction outputs txos and
# a list of corresponding private keys, this function
# will sign the transaction inputs of txn and add the
# corresponding signature script to the transaction 
# which is then returned.
#
def signTransaction(txn, txos, privateKeys):
    #
    # Get standard curve and generator
    #
    curve = ecdsa.curves.SECP256k1
    G = curve.generator
    p = curve.curve.p()
    n = G.order()
    #
    # Now go through all the inputs and sign them
    #
    nInput = 0
    for txin in txn.getInputs():
        #
        # Get the hash that we will sign
        #
        spentOutput = txos[nInput]
        h = int.from_bytes(script.signatureHash(txn, nInput, spentOutput), "big")
        #
        # Get the matching private key - we need a hex representation
        #
        secret = privateKeys[nInput]
        pubkey = ecdsa.ecdsa.Public_key(G, G * secret)
        pubKeyHex = keys.ecPointCompressHex(pubkey.point.x(), pubkey.point.y())
        # 
        # Sign using the ECDSA library 
        #
        privkey = ecdsa.ecdsa.Private_key(pubkey, secret)
        signature = privkey.sign(h, random.SystemRandom().randrange( 1, n ))
        #
        # Bitcoin expects that the s value is at most half of the order n,
        # see interpreter.cpp/IsLowDERSignature
        #
        if signature.s > n // 2:
            signature.s = n - signature.s
        #
        # Now create the scriptSig. We need to match its type according
        # to the type of the output
        #
        outputScriptType = spentOutput.getScriptPubKey().getScriptType()
        if outputScriptType == script.SCRIPTTYPE_P2PKH:
            scriptSig = script.scriptSig(scriptType = script.SCRIPTTYPE_P2PKH,
                                     r = signature.r,
                                     s = signature.s,
                                     pubKeyHex = pubKeyHex,
                                     hashType = 1)
        elif outputScriptType == script.SCRIPTTYPE_P2PK:
            scriptSig = script.scriptSig(scriptType = script.SCRIPTTYPE_P2PK,
                                     r = signature.r,
                                     s = signature.s,
                                     pubKeyHex = None,
                                     hashType = 1)
        else:
            raise ValueError("Cannot sign this type of script")
        #
        # Finally plug this scriptSig into the input
        #
        txin.scriptSig = scriptSig
        txin.scriptSigHex = scriptSig.serialize()
        nInput += 1
        
    return txn

