####################################################
# 
# A very simple miner in Python
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


# import matplotlib
# matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import argparse
import time

import btc.mining
import btc.utils



#
# Build a preliminary block, using data retrieved via
# the RPC call getblocktemplate
#
def buildBlock(address):
    #
    # First we get a block template from the local
    # bitcoind
    #
    template =  btc.utils.rpcCall(method="getblocktemplate")
    bits = int(template['bits'], 16)
    #
    # Next we build a list of the transactions
    #
    txns = []
    for _ in template['transactions']:
        txn = btc.txn.txn()
        txn.deserialize(_['data'])
        assert(txn.getTxnId(byteorder="big") == _['txid'])
        txns.append(txn)
    #
    # Build a preliminary block
    #
    _block = btc.mining.createNewBlock(address=address,
                                  currentLastBlockHash = template['previousblockhash'],
                                  currentHeight = template['height'] - 1,
                                  coinbasevalue = template['coinbasevalue'],
                                  bits = bits,
                                  tx = txns)
    return _block, bits


#
# Get actual height of the block chain and the current last block
#
def getCurrentHeightLast():
    info = btc.utils.rpcCall(method="getblockchaininfo")    
    currentLast = info['bestblockhash']
    currentHeight = info['blocks']
    return currentHeight, currentLast
    

#
# The actual mining loop. We increment the nonce
# in a loop and calculate the block hash until
# it passes the PoW test
#
def doWork(block, bits):
    success = False
    attempts = 0
    while not success:
        if attempts > 2**32:
            raise Error("Giving up")
        attempts += 1
        block.getBlockHeader().nonce = attempts
        success = btc.mining.checkPoW(block, bits = bits)
    return block, attempts


#
# Parse arguments
#        
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target",
                    default="mhjfPZW5gTHetzzmSwpEqhvZC9TZ1sCAdu",
                    help="Target address"
                    )                    
    parser.add_argument("--blocks", 
                    default=1,
                    type=int,
                    help="Number of blocks to mine")
    parser.add_argument("--plot",
                    default=0,
                    type=int,
                    help="Plot development of difficulty and attempts over time")
    parser.add_argument("--save",
                    default=0,
                    type=int,
                    help="Save plots")
    args=parser.parse_args()
    return args


#######################################################################
# 
# Main
#
#######################################################################


#
# Parse arguments
#
args = get_args()

#
# Get current tip
#
height, _ = getCurrentHeightLast()
print("Current height is :", height)

#
# Logs
#
tries = []
diff = []
bl = []

#
# Now we do the actual mining
#
for _ in range(args.blocks):
    #
    # Build a block and mine
    #
    _block, bits = buildBlock(address=args.target)
    _block, attempts = doWork(_block, bits)
    #
    # Submit
    #
    result = btc.utils.rpcCall(method="submitblock", params = [_block.serialize()])
    if result != None:
        print("Error: ", result)
    #
    # If we mine too many blocks in a very short time, we get the error time--too-old,
    # as the check in ContextualCheckBlockHeader in validation.cpp is using <= and not
    # <, so we get an error if our block has the same time stamp as the current last block
    #
    time.sleep(.5)
    coefficient = (float)(bits & 0xFFFFFF)
    size = bits >> 24
    target = int(coefficient * 2**(8*(size - 3)))
    difficulty = _block.getBlockHeader().getDifficulty()
    print("Block ",_, " with ", len(_block.getTx()), "transactions took ", attempts, "attempts, target is now ", "{0:0{1}x}".format(target, 64), "i.e. difficulty is", difficulty)
    #
    # Append current difficulty, attempts and block number
    # to logs
    #
    diff.append(difficulty)
    tries.append(attempts)
    bl.append(height + _)

newHeight, currentLastBlockHash = getCurrentHeightLast()
print("Done, new height is", newHeight)

#
# Now plot results if requested
#
if 1 == args.plot:
    print("Plotting results")
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(2,1,1)
    ax.plot(bl, diff)
    ax.set_title("Difficulty")
    ax = fig.add_subplot(2,1,2)
    ax.plot(bl, tries)
    ax.set_title("Attempts")
    if 1 == args.save:
        plt.savefig("/tmp/mining.png")
    plt.show()

    
