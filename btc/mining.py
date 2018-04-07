####################################################
# 
# Utility functions supporting mining
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
from . import keys
from . import block 

import binascii
import time

#
# Check whether a given block has a valid PoW
#
def checkPoW(block, bits):
    #
    # First determine the target in the block and verify that
    # the hash does not exceed it
    #
    h = block.getBlockHeader().getBlockHash(byteorder="big")
    h = int(h, 16)
    #
    # Do the same for the target
    #
    _bits = block.getBlockHeader().getBits()
    coefficient = (float)(_bits & 0xFFFFFF)
    size = _bits >> 24
    target = int(coefficient * 2**(8*(size - 3)))
    if h > target:
        return False
    #
    # Next check that the block is in line with the global target
    #
    if bits != block.getBlockHeader().getBits():
        return False
    return True
    
    
#
# Check a given block. Parameters:
# - bits - current target in compact encoding (as an integer)
# - currentLastBlock - hash of current last block (as returned by the RPC call
#   getblockchaininfo, i.e. in big endian 
# This will NOT check the PoW!
#
def checkBlock(block, currentLastBlock):
    #
    # First check that the previous block ID is equal to the current
    # last block
    #
    if block.getBlockHeader().getPrevBlockId() != currentLastBlock:
        return False
    #
    # Next check that the first transaction is a coinbase transaction
    #
    tx = block.getTx()
    if 0 == len(tx):
        return False
    if tx[0].isCoinbase() == False:
        return False
    #
    # Check that no other transactions are coinbase transactions
    #
    for i in range(len(tx)):
        if i > 0:
            if tx[i].isCoinbase():
                return False
    #
    # Check Merkle root
    #
    merkleRoot = utils.blockMerkleRoot(block)
    if merkleRoot != serialize.serializeString(block.getBlockHeader().getMerkleRoot(), 32):
        return False
        
    return True
    
#
# Create a coinbase transaction
# Parameter:
# - address - the address to be used for the transaction output
# - coinbase value in Satoshi, including feeds
# - the current height of the chain as integer
# - an extra nonce as integer
#
def createCoinbaseTxn(address, currentHeight, coinbasevalue, extraNonce = 1):
    coinbase = txn.txn()
    publicKeyHash = keys.ecAddressToPKH(address)
    publicKeyHash = binascii.hexlify(publicKeyHash).decode('ascii')
    #
    # Create locking script
    #
    lockingScript = script.scriptPubKey(scriptType = script.SCRIPTTYPE_P2PKH, 
                                        pubKeyHash = publicKeyHash)
    #
    # and output
    #
    txout = txn.txout(value = int(coinbasevalue), 
                        scriptPubKey = lockingScript)
    coinbase.addOutput(txout)
    #
    # Next we do the input. The previous transaction ID is all zeros
    #
    prevTxId = "".join(["0"]*64)
    #
    # The signature script. To be compliant with BIP34, we put the height first
    #
    scriptSig = script.scriptSig()
    scriptSig.pushData(serialize.serializeNumber(currentHeight + 1, 4))
    #
    # We then add the extra nonce
    #
    scriptSig.pushData(serialize.serializeNumber(currentHeight + 1, 4))
    #
    # and a signature ;-)
    #
    # scriptSig.pushData("cc")
    txin = txn.txin(prevTxid = prevTxId, vout=0xFFFFFFFF, scriptSig = scriptSig)
    coinbase.addInput(txin)
    return coinbase
    
#
# This creates a new block with a preliminary nonce, i.e. this
# block will not yet pass the PoW test
# Parameter:
# - address - the address to be used for the transaction output
# - coinbase value in Satoshi, including feeds
# - the hash of the current last block
# - the current height of the chain as integer
# - bits in compact encoding
# - tx - a list of transactions to become part of the block, not including
#        the coinbase transaction
# - mintime - the minimum time to use for the block as provided by getblocktemplate
def createNewBlock(address, currentLastBlockHash, currentHeight, coinbasevalue, bits, tx, mintime):
    #
    # First we build a block header
    #
    blockHeader = block.blockHeader(creationTime = mintime,
                                    prevBlockId = currentLastBlockHash,
                                    nonce = 1,
                                    bits = bits)
    #
    # Next we do the block
    #
    _block = block.block(blockHeader = blockHeader)
    #
    # add the coinbase transaction, followed by all other 
    # transactions
    #
    _block.addTxn(createCoinbaseTxn(address, currentHeight, coinbasevalue))
    for _tx in tx:
        _block.addTxn(_tx)
        assert(False == _tx.isCoinbase())
    _block.updateMerkleRoot()
    return _block
    
    

    
