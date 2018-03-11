###################################################################
# 
# Decoding a raw bitcoin transaction
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

import requests

import btc.utils
import btc.txn

#################################################
#
# Utility function to get a transaction in raw
# format from bitcoin.info
#
#################################################

def get_raw_transaction(txid="ed70b8c66a4b064cfe992a097b3406fa81ff09641fe55a709e4266167ef47891"):
    url = 'https://blockchain.info/en/tx/' + txid + '?format=hex'
    r = requests.get(url)
    return r.text


#################################################
#
# Main
#
#################################################


raw = get_raw_transaction()

#
# Print raw transaction first
#
print("--------------------------------------------------------")
print("Raw transaction:")
print("--------------------------------------------------------")
lines = (len(raw) // 60) + 1
for _ in range(lines):
    print(raw[_*60:_*60+60])
    
    
#
# Deserialize into a txn object
#
txn = btc.txn.txn()
txn.deserialize(raw)

#
# Now print out content one by one
#
print("--------------------------------------------------------")
print("Decoded transaction:")
print("--------------------------------------------------------")

print("Version:           ", txn.getVersion())

print("Number of inputs:  ", len(txn.getInputs()))
for i, txin in enumerate(txn.getInputs()):
    print("Input ", i)
    print("    Previous transaction ID: ", txin.getPrevTxId())
    print("    Index:                   ", txin.getVout())
    print("    Signature script length: ", 
        btc.serialize.serialize_varInt(len(txin.getScriptSigHex()) // 2), 
        "(", 
        len(txin.getScriptSigHex()) // 2, 
        ")")
    print("    Signature script:        ")
    script =  txin.getScriptSigHex()
    lines = (len(script) // 60) + 1
    for _ in range(lines):
        print("                             ", script[_*60:_*60+60])
    print("    Sequence number:         ", hex(txin.getSequence()), "(", txin.getSequence(), ")")

print("Number of outputs:", len(txn.getOutputs()))
for i, txout in enumerate(txn.getOutputs()):
    print("Output", i)
    amount = txout.getValue()
    print("    Amount:                  ", hex(amount), "(", amount, ")")
    print("    Public key script length:", 
    btc.serialize.serialize_varInt(len(txout.getScriptPubKeyHex()) // 2), 
        "(", 
        len(txout.getScriptPubKeyHex()) // 2, 
        ")")
    print("    Public key script:       ")
    script =  txout.getScriptPubKeyHex()
    lines = (len(script) // 60) + 1
    for _ in range(lines):
        print("                             ", script[_*60:_*60+60])

print("Locktime:          ", hex(txn.getLocktime()), "(", txn.getLocktime(), ")")
