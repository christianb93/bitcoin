##########################################################################
#
# Demonstrate how to create a transaction. 
#
# We will need a running bitcoind installation to manage our wallet
# and to retrieve UTXOs
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
##########################################################################


import argparse
import binascii
import random

import btc.txn
import btc.script
import btc.keys
import btc.utils




####################################################
# Parse arguments
####################################################
        
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--amount",
                    type=float,
                    default="1.0",
                    help="Amount in BTC to be transferred"
                    )
    parser.add_argument("--target",
                    default="mpV4bFDWN8NrWX9u3V47UgzxD9wSLQivwj",
                    help="Target address"
                    )                    
    args=parser.parse_args()
    return args


####################################################
# Main
####################################################

args = get_args()

#
# First we make an RPC call to retrieve unspent transaction output and 
# select the outputs that we are going to spend
#
listunspent = btc.utils.rpcCall("listunspent")
#
# Now extract transaction IDs and store that in a list of 
# dictionaries
#
# We split this list into one list of entries that are greater
# than the amount we want to transfer and one list of entries
# that are smaller
#
#
smaller = []
greater = []
amount_to_spend = float(args.amount)
for _ in listunspent:
    if _['spendable']:
        txid = _['txid']
        vout = _['vout']
        amount = float(_['amount'])
        address = _['address']
        coin = {'txid': txid,
                  'vout': vout,
                  'amount': amount,
                  'address' : address}
        if amount > amount_to_spend:
            greater.append(coin)
        else:
            smaller.append(coin)

#
# Next we sort the lists. 
#
greater.sort(key=lambda entry: entry['amount'])
smaller.sort(key=lambda entry: entry['amount'], reverse=True)
#
# If greater is not emtpy, take the smallest (i.e. now first)
# element
#
if len(greater) > 0:
    amount_funded = greater[0]['amount']
    to_be_spent = [greater[0]]
else:
    #
    # We need to combine more than one transaction output
    #
    to_be_spent = []
    amount_funded = 0
    for _ in smaller:
        if amount_funded < amount_to_spend:
            to_be_spent.append(_)
            amount_funded += _['amount']
    if (amount_funded < amount_to_spend):
        # Failed, clean up list
        to_be_spent = []



if 0 == len(to_be_spent):
    print("Could not fund transaction")
    exit(1)
else:
    print("Here is the list of transaction outputs that I will use:  ")    
    print(to_be_spent)
    

#
# Now go through the resulting list and build a list of private
# keys.  At the same time, we build a list of transaction outputs
#
txos = []
privateKeys = []
for _ in to_be_spent:
    tx = btc.txn.txn()
    raw = btc.utils.rpcCall("getrawtransaction", [_['txid']])
    tx.deserialize(raw)
    #
    # Get private key using again an RPC call 
    #
    privKey = btc.utils.rpcCall("dumpprivkey", [_['address']])
    privKey = btc.keys.wifToPayloadBytes(privKey)
    privKey = int.from_bytes(privKey, "big")
    privateKeys.append(privKey)
    txos.append(tx.getOutputs()[_['vout']])
    

#
# Next we create our transaction. First we create the transaction 
# inputs. We leave the signature scripts empty for the time
# being
#
txn = btc.txn.txn()
for _ in to_be_spent:
    txin = btc.txn.txin(prevTxid = _['txid'], vout = _['vout'])
    txn.addInput(txin)

#
# Next we do the outputs. For the time being, we use only one output
# So we need to convert the address to a public key hash
#
publicKeyHash = btc.keys.ecAddressToPKH(args.target)
publicKeyHash = binascii.hexlify(publicKeyHash).decode('ascii')
#
# Create locking script
#
lockingScript = btc.script.scriptPubKey(scriptType = btc.script.SCRIPTTYPE_P2PKH, 
                                        pubKeyHash = publicKeyHash)
#
# and output
#
txout = btc.txn.txout(value = int(amount_to_spend * 100000000), 
                      scriptPubKey = lockingScript)
txn.addOutput(txout)

#
# Sign it
#
txn = btc.script.signTransaction(txn, txos, privateKeys)
#
# and send it
#
print("Sending transaction")
raw = txn.serialize()
s = btc.utils.rpcCall("sendrawtransaction", [raw, True])
print("Done, resulting transaction ID: ")
print(s)

