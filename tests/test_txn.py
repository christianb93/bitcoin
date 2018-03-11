import btc.txn

#
# Compare two strings and return the first charqcte where they
# differ or minus 1
#
def diff_strings(s1, s2):
    l = min(len(s1), len(s2))
    for i in range(l):
        if s1[i] != s2[i]:
            return i
    if len(s1) != len(s2):
        return l
    return -1

#
# Pretty print transaction
#
def pp_txn(raw):
    cpl = 50
    lines = int(len(raw) / cpl)  + 1
    s = raw
    for i in range(lines):
        print(s[0:cpl])
        s = s[cpl:]


#
# Inputs
#

def test_tc1():
    txin_string = "a3632ee302509fd89507dbcc340132544d1607a7e4a853e35ebc995d509b6113000000006a47304402203f7d777711a7406424535d96affc8279655918698f727557ad4fcb5aef7a8913022014d213385be262a75d23b1e592f58c702bdc0bc8d8f006d031051ced14dca48b012102de7badda902f573bddeab87d357d6d70f39c058875f0e05d4b52e4a0cc281ebffeffffff"
    txin = btc.txn.txin()
    txin.deserialize(txin_string)
    assert(txin.getPrevTxId() == "13619b505d99bc5ee353a8e4a707164d54320134ccdb0795d89f5002e32e63a3")
    
    
def test_tc2():
    txin_string = "a3632ee302509fd89507dbcc340132544d1607a7e4a853e35ebc995d509b6113000000006a47304402203f7d777711a7406424535d96affc8279655918698f727557ad4fcb5aef7a8913022014d213385be262a75d23b1e592f58c702bdc0bc8d8f006d031051ced14dca48b012102de7badda902f573bddeab87d357d6d70f39c058875f0e05d4b52e4a0cc281ebffeffffff"
    txin = btc.txn.txin()
    txin.deserialize(txin_string)
    assert(txin.getVout() == 0)
    
    
def test_tc3():
    txin_string = "a3632ee302509fd89507dbcc340132544d1607a7e4a853e35ebc995d509b6113000000006a47304402203f7d777711a7406424535d96affc8279655918698f727557ad4fcb5aef7a8913022014d213385be262a75d23b1e592f58c702bdc0bc8d8f006d031051ced14dca48b012102de7badda902f573bddeab87d357d6d70f39c058875f0e05d4b52e4a0cc281ebffeffffff"
    txin = btc.txn.txin()
    txin.deserialize(txin_string)
    assert(txin.getScriptSigHex() == "47304402203f7d777711a7406424535d96affc8279655918698f727557ad4fcb5aef7a8913022014d213385be262a75d23b1e592f58c702bdc0bc8d8f006d031051ced14dca48b012102de7badda902f573bddeab87d357d6d70f39c058875f0e05d4b52e4a0cc281ebf")
    
    
def test_tc4():
    txin_string = "a3632ee302509fd89507dbcc340132544d1607a7e4a853e35ebc995d509b6113000000006a47304402203f7d777711a7406424535d96affc8279655918698f727557ad4fcb5aef7a8913022014d213385be262a75d23b1e592f58c702bdc0bc8d8f006d031051ced14dca48b012102de7badda902f573bddeab87d357d6d70f39c058875f0e05d4b52e4a0cc281ebffeffffff"
    txin = btc.txn.txin()
    txin.deserialize(txin_string)
    assert(txin.getSequence() == 4294967294)
    
def test_tc5():
    txin_string = "a3632ee302509fd89507dbcc340132544d1607a7e4a853e35ebc995d509b6113000000006a47304402203f7d777711a7406424535d96affc8279655918698f727557ad4fcb5aef7a8913022014d213385be262a75d23b1e592f58c702bdc0bc8d8f006d031051ced14dca48b012102de7badda902f573bddeab87d357d6d70f39c058875f0e05d4b52e4a0cc281ebffeffffff"
    txin = btc.txn.txin()
    txin.deserialize(txin_string)
    assert(txin.getScriptSig().getSignatureR() == 28717389861751114223003515488885273955485516442781854597805147664463299250451)
    

#
# Outputs
#    
def test_tc6():
    txout_string = "00e1f505000000001976a914625d8e5d40a1b797b47cb66eee958724a668d8d288ac"
    txout = btc.txn.txout()
    txout.deserialize(txout_string)
    assert(txout.getValue() == 100000000)
    
    
def test_tc7():
    txout_string = "00e1f505000000001976a914625d8e5d40a1b797b47cb66eee958724a668d8d288ac"
    txout = btc.txn.txout()
    txout.deserialize(txout_string)
    assert(txout.getScriptPubKeyHex() == "76a914625d8e5d40a1b797b47cb66eee958724a668d8d288ac")
    
    
    
#
# Full transactions
#
    
#
# Check inputs
#
def test_tc11():
    s = "0200000001a3632ee302509fd89507dbcc340132544d1607a7"
    s += "e4a853e35ebc995d509b6113000000006a47304402203f7d77"
    s += "7711a7406424535d96affc8279655918698f727557ad4fcb5a"
    s += "ef7a8913022014d213385be262a75d23b1e592f58c702bdc0b"
    s += "c8d8f006d031051ced14dca48b012102de7badda902f573bdd"
    s += "eab87d357d6d70f39c058875f0e05d4b52e4a0cc281ebffeff"
    s += "ffff0258923f71000000001976a914802da8768a071f707e3d"
    s += "2713568ff4e3bfe6035288ac00e1f505000000001976a91462"
    s += "5d8e5d40a1b797b47cb66eee958724a668d8d288ac66000000"
    txn = btc.txn.txn()
    txn.deserialize(s)
    assert(txn.getVersion() == 2)
    inputs = txn.getInputs()
    assert(len(inputs) == 1)
    vin = inputs[0]
    assert(vin.getPrevTxId() == "13619b505d99bc5ee353a8e4a707164d54320134ccdb0795d89f5002e32e63a3")
    assert(vin.getVout() == 0)
    assert(vin.getScriptSigHex() == "47304402203f7d777711a7406424535d96affc8279655918698f727557ad4fcb5aef7a8913022014d213385be262a75d23b1e592f58c702bdc0bc8d8f006d031051ced14dca48b012102de7badda902f573bddeab87d357d6d70f39c058875f0e05d4b52e4a0cc281ebf")
    assert(vin.getScriptSig().getSignatureR() == 28717389861751114223003515488885273955485516442781854597805147664463299250451)
    assert(vin.getSequence() == 4294967294)
    

#
# Check outputs
#
def test_tc12():
    s = "0200000001a3632ee302509fd89507dbcc340132544d1607a7"
    s += "e4a853e35ebc995d509b6113000000006a47304402203f7d77"
    s += "7711a7406424535d96affc8279655918698f727557ad4fcb5a"
    s += "ef7a8913022014d213385be262a75d23b1e592f58c702bdc0b"
    s += "c8d8f006d031051ced14dca48b012102de7badda902f573bdd"
    s += "eab87d357d6d70f39c058875f0e05d4b52e4a0cc281ebffeff"
    s += "ffff0258923f71000000001976a914802da8768a071f707e3d"
    s += "2713568ff4e3bfe6035288ac00e1f505000000001976a91462"
    s += "5d8e5d40a1b797b47cb66eee958724a668d8d288ac66000000"
    txn = btc.txn.txn()
    txn.deserialize(s)
    assert(txn.getVersion() == 2)
    outputs = txn.getOutputs()
    assert(len(outputs) == 2)
    o0 = outputs[0]
    assert(o0.getValue() == 1899991640)
    assert(o0.getScriptPubKeyHex() == "76a914802da8768a071f707e3d2713568ff4e3bfe6035288ac")
    assert(o0.getScriptPubKey().getPubKeyHash() == "802da8768a071f707e3d2713568ff4e3bfe60352")
    assert(txn.getLocktime() == 102)

#
# Some examples from bitcoin.info 
# 
# 

# txid = 1d76bfb6d913b6aee62776271b643f9ef353065cbdad3bd9723cd050744ccc13
def test_tc20():
	s = "01000000017f328ae9b46c631d38a7efb88ec0214519341cd5"
	s += "c0ed250fc88d20b47aa5f9c0010000006b483045022100843d0108"
	s += "b411452da23ce8b9041368300f11a042716a9ae8f3aaa2e5fe39654"
	s += "c022079864ef33971a7cef3aef4658c1d2dec5a5e27b5e7e41c5722"
	s += "fc192dd84472da0121029353adf8364a7fe132ba88267b163fc1e55"
	s += "773a99b06d2ae0a18ee706d73db3affffffff02404b4c00000000001"
	s += "976a9148bdeb16c87bd9f5ffeb24879cb2d61cfc60d5b3488ac4c842a"
	s += "13000000001976a914ff4a0e280823418752a883e0ba7ae8cbec46606a88ac00000000"
	txn = btc.txn.txn()
	txn.deserialize(s)
	assert(txn.getVersion() == 1)
	assert(txn.getLocktime() == 0)
	inputs = txn.getInputs()
	assert(1 == len(inputs))
	assert(inputs[0].getPrevTxId() == "c0f9a57ab4208dc80f25edc0d51c34194521c08eb8efa7381d636cb4e98a327f")
	assert(inputs[0].getVout() == 1)
	assert(inputs[0].getScriptSigHex() == "483045022100843d0108b411452da23ce8b9041368300f11a042716a9ae8f3aaa2e5fe39654c022079864ef33971a7cef3aef4658c1d2dec5a5e27b5e7e41c5722fc192dd84472da0121029353adf8364a7fe132ba88267b163fc1e55773a99b06d2ae0a18ee706d73db3a")
	assert(inputs[0].getSequence() == 4294967295)
	assert(inputs[0].getScriptSig().getPubKeyHex() == "029353adf8364a7fe132ba88267b163fc1e55773a99b06d2ae0a18ee706d73db3a")
	outputs = txn.getOutputs()
	assert(2 == len(outputs))
	output0 = outputs[0]
	assert(output0.getValue() == 0.05 * 100000000)
	assert(output0.getScriptPubKey().getPubKeyHash() == "8bdeb16c87bd9f5ffeb24879cb2d61cfc60d5b34")

# An example with more than one input
# txid = ed70b8c66a4b064cfe992a097b3406fa81ff09641fe55a709e4266167ef47891
# https://blockchain.info/de/rawtx/ed70b8c66a4b064cfe992a097b3406fa81ff09641fe55a709e4266167ef47891
# https://blockchain.info/de/tx/ed70b8c66a4b064cfe992a097b3406fa81ff09641fe55a709e4266167ef47891?format=hex
def test_tc21():
    s = "0200000003620f7bc1087b0111f76978ef747001e3ae0a12f254cbfb858f028f891c40e5f6010000006a47304402207f5dfc2f7f7329b7cc731df605c83aa6f48ec2218495324bb4ab43376f313b840220020c769655e4bfcc54e55104f6adc723867d9d819266d27e755e098f646f689d0121038c2d1cbe4d731c69e67d16c52682e01cb70b046ead63e90bf793f52f541dafbdfefffffff15fe7d9e0815853738ce47deadee69339e027a1dfcfb6fa887cce3a72626e7b010000006a47304402203202e6c640c063989623fc782ac1c9dc3c6fcaed996d852ec876749ba63db63b02207ef86e262ad4b4bc9cebfadb609f52c35b0105e15d58a5ecbecc5e536d3a8cd8012103dc526ca188418ab128d998bf80942d66f1b3be585d0c89bd61c533bddbdaa729feffffff84e6431db86833897bab333d844486c183dd01e69862edea442e480c2d8cb549010000006a47304402200320bc83f35ceab4a7ef0f8181eedb5f54e3f617626826cc49c8c86efc9be0b302203705889d6aed50f716b81b0f3f5769d72d1b8a6b59d1b0b73bcf94245c283b8001210263591c21ce8ee0d96a617108d7c278e2e715ac6d8afd3fcd158bee472c590068feffffff02ca780a00000000001976a914811fb695e46e2386501bcd70e5c869fe6c0bb33988ac10f59600000000001976a9140f2408a811f6d24ab1833924d98d884c44ecee8888ac6fce0700"
    txn = btc.txn.txn()
    txn.deserialize(s)
    assert(txn.getVersion() == 2)
    inputs = txn.getInputs()
    assert(3 == len(inputs))
    assert("03dc526ca188418ab128d998bf80942d66f1b3be585d0c89bd61c533bddbdaa729" == inputs[1].getScriptSig().getPubKeyHex())
    assert(txn.getTxnId() == "ed70b8c66a4b064cfe992a097b3406fa81ff09641fe55a709e4266167ef47891")
    
#
# Test serialization
#

# Serialize a transaction input
def test_tc30():
    scriptSig = btc.script.scriptSig()
    scriptSig.deserialize("47304402203f7d777711a7406424535d96affc8279655918698f727557ad4fcb5aef7a8913022014d213385be262a75d23b1e592f58c702bdc0bc8d8f006d031051ced14dca48b012102de7badda902f573bddeab87d357d6d70f39c058875f0e05d4b52e4a0cc281ebf")
    txin = btc.txn.txin(prevTxid = "13619b505d99bc5ee353a8e4a707164d54320134ccdb0795d89f5002e32e63a3",
                        vout = 0, 
                        scriptSig = scriptSig,
                        sequence = 4294967294)
    s = txin.serialize()
    e = "a3632ee302509fd89507dbcc340132544d1607a7e4a853e35ebc995d509b6113"
    e = e + "00000000"
    e = e + "6a47304402203f7d777711a7406424535d96affc8279655918698f727557ad4fcb5aef7a8913022014d213385be262a75d23b1e592f58c702bdc0bc8d8f006d031051ced14dca48b012102de7badda902f573bddeab87d357d6d70f39c058875f0e05d4b52e4a0cc281ebf"
    e = e + "feffffff"
    assert(s == e)
    _txin = btc.txn.txin()
    _txin.deserialize(s)
    assert(_txin.prevTxid == txin.prevTxid)
    assert(_txin.getScriptSigHex() == txin.getScriptSigHex())
    assert(_txin.vout == txin.vout)
    assert(_txin.sequence == txin.sequence)
                        
    
# Serialize a transaction output
def test_tc31():
    scriptPubKey = btc.script.scriptPubKey()
    scriptPubKey.deserialize("76a914625d8e5d40a1b797b47cb66eee958724a668d8d288ac")
    txout = btc.txn.txout(value = 100000000, scriptPubKey = scriptPubKey)
    s = txout.serialize()
    assert(s == "00e1f505000000001976a914625d8e5d40a1b797b47cb66eee958724a668d8d288ac")
    

# Serialize a transaction
def test_tc32():
    s = "0200000001a3632ee302509fd89507dbcc340132544d1607a7"
    s += "e4a853e35ebc995d509b6113000000006a47304402203f7d77"
    s += "7711a7406424535d96affc8279655918698f727557ad4fcb5a"
    s += "ef7a8913022014d213385be262a75d23b1e592f58c702bdc0b"
    s += "c8d8f006d031051ced14dca48b012102de7badda902f573bdd"
    s += "eab87d357d6d70f39c058875f0e05d4b52e4a0cc281ebffeff"
    s += "ffff0258923f71000000001976a914802da8768a071f707e3d"
    s += "2713568ff4e3bfe6035288ac00e1f505000000001976a91462"
    s += "5d8e5d40a1b797b47cb66eee958724a668d8d288ac66000000"
    txn = btc.txn.txn()
    txn.deserialize(s)
    assert(s == txn.serialize())

def test_tc33():
    spendingTxid = "1d76bfb6d913b6aee62776271b643f9ef353065cbdad3bd9723cd050744ccc13"
    s = "01000000017f328ae9b46c631d38a7efb88ec0214519341cd5c0ed250fc88d20b47aa5f9c0010000006b483045022100843d0108b411452da23ce8b9041368300f11a042716a9ae8f3aaa2e5fe39654c022079864ef33971a7cef3aef4658c1d2dec5a5e27b5e7e41c5722fc192dd84472da0121029353adf8364a7fe132ba88267b163fc1e55773a99b06d2ae0a18ee706d73db3affffffff02404b4c00000000001976a9148bdeb16c87bd9f5ffeb24879cb2d61cfc60d5b3488ac4c842a13000000001976a914ff4a0e280823418752a883e0ba7ae8cbec46606a88ac00000000"
    txn = btc.txn.txn()
    txn.deserialize(s)
    _s = txn.serialize()
    assert(s == _s)
    
    
    
