##########################################################################
#
# Test functionality related to transactions
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

import docker
import time
import os

import btc.txn
import btc.script
import btc.keys
import btc.utils

import pytest

from fixtures import startEnv

#
# Submit a transaction, then decode it and compare the result against
# the result of the RPC call decoderawtransaction
#

def test_tc1(startEnv):
    id = btc.utils.rpcCall("sendtoaddress", ["mkvAYmgqrEFEsJ9zGBi9Z87gP5rGNAu2mx", 5])
    raw = btc.utils.rpcCall("getrawtransaction", [id])
    txn = btc.txn.txn()
    txn.deserialize(raw)
    #
    # Now get the JSON version and compare
    #
    json = btc.utils.rpcCall("decoderawtransaction", [raw])
    assert(txn.getTxnId() == id)
    assert(txn.getVersion() == json['version'])
    assert(txn.getLocktime() == json['locktime'])
    assert(len(json['vin']) == len(txn.getInputs()))
    #
    # Check inputs
    #
    for i in range(len(txn.getInputs())):
        txin = txn.getInputs()[i]
        _txin = json['vin'][i]
        assert(txin.getScriptSigHex() == _txin['scriptSig']['hex'])
        assert(_txin['vout'] == txin.getVout())
        assert(_txin['sequence'] == txin.getSequence())
    #
    # Check outputs
    #
    for i in range(len(txn.getOutputs())):
        txout = txn.getOutputs()[i]
        _txout = json['vout'][i]
        assert(_txout['n'] == i)
        assert(_txout['scriptPubKey']['hex'] == txout.getScriptPubKeyHex())
        assert(_txout['value']*10**8 == txout.getValue())
        
        
#
# Test SendMoney
#
def test_tc2(startEnv):
    l = btc.utils.rpcCall("listtransactions")
    x = [_ for _ in l if _['address'] == "mpV4bFDWN8NrWX9u3V47UgzxD9wSLQivwj"]
    assert(0 == len(x))
    out = os.system("python SendMoney.py")
    print(out)
    l = btc.utils.rpcCall("listtransactions")
    x = [_ for _ in l if _['address'] == "mpV4bFDWN8NrWX9u3V47UgzxD9wSLQivwj"]
    assert(1 == len(x))
    _txn = x[0]
    assert(_txn['amount'] == -1.0)
    
    
    
