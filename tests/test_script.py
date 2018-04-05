import btc.script

#
# signature scripts
# 

# P2PKH, determine type
def test_tc1():
    s = "47304402203f7d777711a7406424535d96affc8279655918698f727557ad4fcb5aef7a8913022014d213385be262a75d23b1e592f58c702bdc0bc8d8f006d031051ced14dca48b012102de7badda902f573bddeab87d357d6d70f39c058875f0e05d4b52e4a0cc281ebf"    
    thisScript = btc.script.scriptSig()
    thisScript.deserialize(s)
    assert(thisScript.getScriptType() == btc.script.SCRIPTTYPE_P2PKH)
    
    
# P2PKH, get signature
def test_tc2():
    s = "47304402203f7d777711a7406424535d96affc8279655918698f727557ad4fcb5aef7a8913022014d213385be262a75d23b1e592f58c702bdc0bc8d8f006d031051ced14dca48b012102de7badda902f573bddeab87d357d6d70f39c058875f0e05d4b52e4a0cc281ebf"    
    thisScript = btc.script.scriptSig()
    thisScript.deserialize(s)
    assert(thisScript.getSignatureR() == 28717389861751114223003515488885273955485516442781854597805147664463299250451)
    assert(thisScript.getSignatureS() == 9417427507882938937642217020078111785602338856730702784564977326471654450315)
    assert(thisScript.getHashType() == 1)
    
# P2PKH, get public key hashs
def test_tc3():
    s = "47304402203f7d777711a7406424535d96affc8279655918698f727557ad4fcb5aef7a8913022014d213385be262a75d23b1e592f58c702bdc0bc8d8f006d031051ced14dca48b012102de7badda902f573bddeab87d357d6d70f39c058875f0e05d4b52e4a0cc281ebf"    
    thisScript = btc.script.scriptSig()
    thisScript.deserialize(s)
    assert(thisScript.getPubKeyHex() == "02de7badda902f573bddeab87d357d6d70f39c058875f0e05d4b52e4a0cc281ebf")

# P2PK
def test_tc4():
    s = "47304402203999487a9229f09fa12a7bd1257a5fdad08ab73d5c2bd7bf75f4cf8c1021bcb3022033aae41cbbeef9c0434baad4d30167445c115f96a6a7bd7ee76476fec431efd301"
    thisScript = btc.script.scriptSig()
    thisScript.deserialize(s)
    assert(thisScript.getScriptType() == btc.script.SCRIPTTYPE_P2PK)
    assert(thisScript.getSignatureR() == 26052660200400586925139939243725412909408257739410599900363456564897758952627)
    assert(thisScript.getSignatureS() == 23369893651596193469437584182929344151374396562731549816359458289899032145875)
    
#
# Public key scripts
#
    
# P2PKH
def test_tc24():
    s = "76a914a0c2e453aa3208555215254591054296a245dbca88ac"
    thisScript = btc.script.scriptPubKey()
    thisScript.deserialize(s)
    assert(thisScript.getScriptType() == btc.script.SCRIPTTYPE_P2PKH)
    assert(thisScript.getPubKeyHash() == "a0c2e453aa3208555215254591054296a245dbca")
    
    
# P2PK
def test_tc25():
    s = "2102b6f24d800b6f31e5252df9101cd99bb9fe7cf80cfedbfa45366014f0d02c8250ac"
    thisScript = btc.script.scriptPubKey()
    thisScript.deserialize(s)
    assert(thisScript.getScriptType() == btc.script.SCRIPTTYPE_P2PK)    
    assert(thisScript.getPubKeyHex() == "02b6f24d800b6f31e5252df9101cd99bb9fe7cf80cfedbfa45366014f0d02c8250")


def test_tc26():
    #
    # An example from blockchain.info (txid 1d76bfb6d913b6aee62776271b643f9ef353065cbdad3bd9723cd050744ccc13)
    #
    s = "3045022100843d0108b411452da23ce8b9041368300f11a042716a9ae8f3aaa2e5fe39654c022079864ef33971a7cef3aef4658c1d2dec5a5e27b5e7e41c5722fc192dd84472da01"
    # 48 - OPCODE for pushing the remainder on stack, not part of DER signature
    # 30 = DER signature 
    # 45 = length (69 bytes). This is the length minus the 
    # trailing hash type 01) and the byte 30 plus the length
    # byte itself
    # 02 - DER integer
    # 21 = 33 - length of R
    # next 33 bytes - R
    #
    r_hex = "00843d0108b411452da23ce8b9041368300f11a042716a9ae8f3aaa2e5fe39654c"
    #
    # 02 - DER integer
    # 20 = 32 - length of S
    # next 32 bytes - S
    # 
    s_hex = "79864ef33971a7cef3aef4658c1d2dec5a5e27b5e7e41c5722fc192dd84472da"
    assert(len(r_hex) == 33*2)
    assert(len(s_hex) == 32*2)
    l = len(s)  / 2
    assert(69 == l - 3)
    assert(True == btc.utils.isValidDERSignature(s))
    scriptSig = btc.script.scriptSig()
    scriptSig.deserialize("48" + s)
    assert(scriptSig.getHashType() == 1)
    assert(scriptSig.getScriptType() == btc.script.SCRIPTTYPE_P2PK)
    assert(scriptSig.getSignatureR() == int.from_bytes(bytes.fromhex(r_hex), "big"))
    assert(scriptSig.getSignatureS() == int.from_bytes(bytes.fromhex(s_hex), "big"))
    _s = scriptSig.serialize()
    assert(_s == "48" + s)
    
#
# serialization
#
    

# Serialize a P2PKH signature script
def test_tc30():
    thisScript = btc.script.scriptSig(pubKeyHex = "02de7badda902f573bddeab87d357d6d70f39c058875f0e05d4b52e4a0cc281ebf", 
                                    r =  28717389861751114223003515488885273955485516442781854597805147664463299250451,
                                    s = 9417427507882938937642217020078111785602338856730702784564977326471654450315,
                                    scriptType = btc.script.SCRIPTTYPE_P2PKH)
    s = thisScript.serialize()
    assert (s == "47304402203f7d777711a7406424535d96affc8279655918698f727557ad4fcb5aef7a8913022014d213385be262a75d23b1e592f58c702bdc0bc8d8f006d031051ced14dca48b012102de7badda902f573bddeab87d357d6d70f39c058875f0e05d4b52e4a0cc281ebf")


# Serialize a P2PK signature script
def test_tc31():
    thisScript = btc.script.scriptSig(r = 26052660200400586925139939243725412909408257739410599900363456564897758952627,
                                    s = 23369893651596193469437584182929344151374396562731549816359458289899032145875,
                                    scriptType = btc.script.SCRIPTTYPE_P2PK)
    s = thisScript.serialize()
    assert(s == "47304402203999487a9229f09fa12a7bd1257a5fdad08ab73d5c2bd7bf75f4cf8c1021bcb3022033aae41cbbeef9c0434baad4d30167445c115f96a6a7bd7ee76476fec431efd301")
    

# Serialize a P2PKH public key script
def test_tc32():
    thisScript = btc.script.scriptPubKey(scriptType = btc.script.SCRIPTTYPE_P2PKH,
                                        pubKeyHash = "a0c2e453aa3208555215254591054296a245dbca")
    s = thisScript.serialize()
    assert(s == "76a914a0c2e453aa3208555215254591054296a245dbca88ac")

# Serialize a P2PK public key script
def test_tc33():
    thisScript = btc.script.scriptPubKey(scriptType = btc.script.SCRIPTTYPE_P2PK,
                                        pubKeyHex = "02b6f24d800b6f31e5252df9101cd99bb9fe7cf80cfedbfa45366014f0d02c8250")
    s = thisScript.serialize()
    assert(s == "2102b6f24d800b6f31e5252df9101cd99bb9fe7cf80cfedbfa45366014f0d02c8250ac")


#
# Serialize for signing
#
def test_tc40():
    s = "0200000001a3632ee302509fd89507dbcc340132544d1607a7e4a853e35ebc995d509b6113010000006b483045022100e73cf45218a3a38f358b257fbaafbfa5ce18afed0111a255fe4e1bf4389662a30220761844c239c28ee3a7f57a5bf9ef71ce169d69a2b0625e2fe0b92c760b314562012102418f38e4eb8a96a25020739c0da0bfd843cdbc311ccda4b1a688f3541c212e61feffffff02586bdaac000000001976a914cf009cfd5d3fb83e9d87238310d0400fdaca487b88ac00e1f505000000001976a914625d8e5d40a1b797b47cb66eee958724a668d8d288ac66000000"
    txn = btc.txn.txn()
    txn.deserialize(s)
    scriptPubKey = btc.script.scriptPubKey()
    scriptPubKey.deserialize("76a914250ed017660abdd723ed28a427fda68a6eb0a3f888ac")
    forSigning = "0200000001a3632ee302509fd89507dbcc340132544d1607a7e4a853e35ebc995d509b6113010000001976a914250ed017660abdd723ed28a427fda68a6eb0a3f888acfeffffff02586bdaac000000001976a914cf009cfd5d3fb83e9d87238310d0400fdaca487b88ac00e1f505000000001976a914625d8e5d40a1b797b47cb66eee958724a668d8d288ac6600000001000000"
    _forSigning = btc.script.serializeForSigning(txn, 0, scriptPubKey)
    assert(_forSigning == forSigning)


#
# Serialize for signing
#
def test_tc41():
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
    s = "0200000001a81a805a33bc1ea8236629ab04baf30ae871bd14a78afeee191114ad80e6e0f4000000004847304402203999487a9229f09fa12a7bd1257a5fdad08ab73d5c2bd7bf75f4cf8c1021bcb3022033aae41cbbeef9c0434baad4d30167445c115f96a6a7bd7ee76476fec431efd301feffffff0200853577000000001976a914a0c2e453aa3208555215254591054296a245dbca88ac005ed0b2000000001976a914250ed017660abdd723ed28a427fda68a6eb0a3f888ac65000000"
    prev = btc.txn.txn()
    prev.deserialize(s)
    assert(txn.getInputs()[0].getPrevTxId() == prev.getTxnId())
    assert(txn.getInputs()[0].getVout() == 0)
    forSigning = "0200000001a3632ee302509fd89507dbcc340132544d1607a7"
    forSigning += "e4a853e35ebc995d509b6113000000001976a914a0c2e453aa"
    forSigning += "3208555215254591054296a245dbca88acfeffffff0258923f"
    forSigning += "71000000001976a914802da8768a071f707e3d2713568ff4e3"
    forSigning += "bfe6035288ac00e1f505000000001976a914625d8e5d40a1b7"
    forSigning += "97b47cb66eee958724a668d8d288ac6600000001000000"
    _forSigning = btc.script.serializeForSigning(txn, 0, prev.getOutputs()[0].getScriptPubKey())
    assert(forSigning == _forSigning)
    h = btc.script.signatureHash(txn, 0, prev.getOutputs()[0])
    assert(int.from_bytes(h, 'big') == 55810787963993017959789014082265465084317085514403090755484136402704087066930)


#
# Verify signature
#
def test_tc42():
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
    s = "0200000001a81a805a33bc1ea8236629ab04baf30ae871bd14a78afeee191114ad80e6e0f4000000004847304402203999487a9229f09fa12a7bd1257a5fdad08ab73d5c2bd7bf75f4cf8c1021bcb3022033aae41cbbeef9c0434baad4d30167445c115f96a6a7bd7ee76476fec431efd301feffffff0200853577000000001976a914a0c2e453aa3208555215254591054296a245dbca88ac005ed0b2000000001976a914250ed017660abdd723ed28a427fda68a6eb0a3f888ac65000000"
    prev = btc.txn.txn()
    prev.deserialize(s)
    assert(True == btc.script.verifySignature(txn, 0, prev.getOutputs()[0]))
    
    
#
# Verify signature for an example from bitcoin.info
#
def test_tc43():
    spendingTxid = "1d76bfb6d913b6aee62776271b643f9ef353065cbdad3bd9723cd050744ccc13"
    s = "01000000017f328ae9b46c631d38a7efb88ec0214519341cd5c0ed250fc88d20b47aa5f9c0010000006b483045022100843d0108b411452da23ce8b9041368300f11a042716a9ae8f3aaa2e5fe39654c022079864ef33971a7cef3aef4658c1d2dec5a5e27b5e7e41c5722fc192dd84472da0121029353adf8364a7fe132ba88267b163fc1e55773a99b06d2ae0a18ee706d73db3affffffff02404b4c00000000001976a9148bdeb16c87bd9f5ffeb24879cb2d61cfc60d5b3488ac4c842a13000000001976a914ff4a0e280823418752a883e0ba7ae8cbec46606a88ac00000000"
    spendingTransaction = btc.txn.txn()
    spendingTransaction.deserialize(s)
    _s = spendingTransaction.serialize()
    assert(s == _s)
    assert(spendingTxid == spendingTransaction.getTxnId())
    #
    # We look at input 0 - the only input
    #
    txin = spendingTransaction.getInputs()[0]
    #
    # It spends output 1 of transaction c0f9a57ab4208dc80f25edc0d51c34194521c08eb8efa7381d636cb4e98a327f
    #
    assert(txin.getPrevTxId() == "c0f9a57ab4208dc80f25edc0d51c34194521c08eb8efa7381d636cb4e98a327f")
    assert(txin.getVout() == 1)
    s = "0100000001608fd51af5b2b2601e5e03a768817ea33cd2b9594eabe63be18b0c36a7ff67d3010000006b4830450221008128192e9badf85332f8b1b7364728e7a39e9d76f516d6726b4856e8099b22fc0220106ab43d6eb531ebae8817ab2b96375229da73bc2e75aa1e88065e1cdbab9fe1012103fd0f9db55d71d43fe1ef48d88724ce1f454a93ce0294826c346920e1e6563415ffffffff0220300500000000001976a914093a094888bcf19767c48af29bd625e3d809ba1388ac641d7913000000001976a9145d88b5b3eaca46287b1e960b15c6d6af40eb83cb88ac00000000"
    prevTransaction = btc.txn.txn()
    prevTransaction.deserialize(s)
    assert(prevTransaction.getTxnId() == txin.getPrevTxId())
    spentTxout = prevTransaction.getOutputs()[txin.getVout()]
    assert(True == btc.script.verifySignature(spendingTransaction, 0, spentTxout))

#
# An example from the local test regnet with two inputs
# 
def test_tc44():
    spendingTxid = "3a551c41a67987218d40549b1ac1f9549829bebae4ef2897dcba3bddc47e7c76"
    s = "02000000022defa4cc31ae5fb6b2c52c6a1c9f34e7429c3ed37fb6227869a4bcea94e0daa70000000049483045022100f8103217d8c7ef464e4580a312973d6070efb10d54f477e7aa2d29ccd3939fef022058f3631d7143b16075c9232912257b62ca4929da068c64cc2a424ad3455a5d8301feffffff80aa1fd1acc50dc41415c6ffe179059720732a075dfa2be275d7f4a8a16fb767000000006a4730440220018d1d05cdfb481ace05a82e5e91104a1cb92efb5c765c7b2aeda17a7e2114780220514bfe8f388c485846b2d10c347a12ce8d67ec705c203ec7e0e20627e338bc63012103c138b3dc8f9039199232177c8b11459fa402472373d1843f3935566c6ca4dd42feffffff02c896496b000000001976a91429e8633b1bed191b7adbe73628baec4d4451d65f88ac00d3fb2f010000001976a914625d8e5d40a1b797b47cb66eee958724a668d8d288ac43000000"
    spendingTransaction = btc.txn.txn()
    spendingTransaction.deserialize(s)
    _s = spendingTransaction.serialize()
    assert(s == _s)
    assert(spendingTxid == spendingTransaction.getTxnId())
    #
    # We look at input 0 
    #
    txin = spendingTransaction.getInputs()[0]
    #
    # It spends output 0 of transaction  a7dae094eabca4697822b67fd33e9c42e7349f1c6a2cc5b2b65fae31cca4ef2d
    #
    assert(txin.getPrevTxId() == "a7dae094eabca4697822b67fd33e9c42e7349f1c6a2cc5b2b65fae31cca4ef2d")
    assert(txin.getVout() == 0)
    s = "02000000010000000000000000000000000000000000000000000000000000000000000000ffffffff03520101ffffffff0200f2052a01000000232102b6f24d800b6f31e5252df9101cd99bb9fe7cf80cfedbfa45366014f0d02c8250ac0000000000000000266a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf900000000"
    prevTransaction = btc.txn.txn()
    prevTransaction.deserialize(s)
    assert(s == prevTransaction.serialize())
    assert(prevTransaction.getTxnId() == txin.getPrevTxId())
    spentTxout = prevTransaction.getOutputs()[txin.getVout()]
    stringToHash = btc.script.serializeForSigning(spendingTransaction, 0, spentTxout.getScriptPubKey())
    assert(True == btc.script.verifySignature(spendingTransaction, 0, spentTxout))


#
# Test implicit pushes
#
def test_tc45():
    scriptSig = btc.script.scriptSig()
    scriptSig.pushData("05060708")
    s = scriptSig.serialize()
    assert(s == "0405060708")
    #
    # Push more
    #
    scriptSig.pushData("ff")
    s = scriptSig.serialize()
    assert(s == "040506070801ff")
