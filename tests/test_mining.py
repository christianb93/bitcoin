import btc.block
import btc.mining

import time


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
# Pretty print blocks
#
def pp_block(raw):
    cpl = 50
    lines = int(len(raw) / cpl)  + 1
    s = raw
    for i in range(lines):
        print(s[0:cpl])
        s = s[cpl:]


#
# Verify PoW of a valid block
# 
def test_tc1():
    raw = '00000020df9e03f6f3b6089704150a0627841c9fb86adbf265fc8f31c95bb6b99e4a604c187d9b8d7dad469812834e9f4f72af649656b4179880d0102499118c7fd488d9bc69b65affff7f20030000000102000000010000000000000000000000000000000000000000000000000000000000000000ffffffff04016b0101ffffffff0200f2052a01000000232103bacc76145b9800c24b519cf659e6add26db1ea0b23806ae361f058e67d84bd04ac0000000000000000266a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf900000000'
    blockHeader = btc.block.blockHeader()
    raw = blockHeader.deserialize(raw)
    assert(blockHeader.getVersion() == 0x20000000)
    assert(blockHeader.getPrevBlockId() == '4c604a9eb9b65bc9318ffc65f2db6ab89f1c8427060a15049708b6f3f6039edf')
    assert(blockHeader.getMerkleRoot() == 'd988d47f8c11992410d0809817b4569664af724f9f4e83129846ad7d8d9b7d18')
    assert(blockHeader.getCreationTime() == 1521904060)
    assert(blockHeader.getBits() == 545259519)
    assert(blockHeader.getNonce() == 3)
    assert(raw == '0102000000010000000000000000000000000000000000000000000000000000000000000000ffffffff04016b0101ffffffff0200f2052a01000000232103bacc76145b9800c24b519cf659e6add26db1ea0b23806ae361f058e67d84bd04ac0000000000000000266a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf900000000')
    block = btc.block.block(blockHeader)
    assert(True == btc.mining.checkPoW(block, bits = 545259519))

#
# Verify PoW of a valid block - but use wrong bits
# 
def test_tc2():
    raw = '00000020df9e03f6f3b6089704150a0627841c9fb86adbf265fc8f31c95bb6b99e4a604c187d9b8d7dad469812834e9f4f72af649656b4179880d0102499118c7fd488d9bc69b65affff7f20030000000102000000010000000000000000000000000000000000000000000000000000000000000000ffffffff04016b0101ffffffff0200f2052a01000000232103bacc76145b9800c24b519cf659e6add26db1ea0b23806ae361f058e67d84bd04ac0000000000000000266a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf900000000'
    blockHeader = btc.block.blockHeader()
    raw = blockHeader.deserialize(raw)
    assert(blockHeader.getVersion() == 0x20000000)
    assert(blockHeader.getPrevBlockId() == '4c604a9eb9b65bc9318ffc65f2db6ab89f1c8427060a15049708b6f3f6039edf')
    assert(blockHeader.getMerkleRoot() == 'd988d47f8c11992410d0809817b4569664af724f9f4e83129846ad7d8d9b7d18')
    assert(blockHeader.getCreationTime() == 1521904060)
    assert(blockHeader.getBits() == 545259519)
    assert(blockHeader.getNonce() == 3)
    assert(raw == '0102000000010000000000000000000000000000000000000000000000000000000000000000ffffffff04016b0101ffffffff0200f2052a01000000232103bacc76145b9800c24b519cf659e6add26db1ea0b23806ae361f058e67d84bd04ac0000000000000000266a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf900000000')
    block = btc.block.block(blockHeader)
    assert(False == btc.mining.checkPoW(block, bits = 545259519 - 1))


#
# Create and verify a coinbase transaction
#
def test_tc3():
    coinbase = btc.mining.createCoinbaseTxn("mhjfPZW5gTHetzzmSwpEqhvZC9TZ1sCAdu", 100, 50*10**8)
    assert(coinbase.isCoinbase())
    #
    # Check some fields. First the address
    #
    txout = coinbase.getOutputs()[0]
    scriptPubKey = txout.getScriptPubKey()
    pubKeyHash = scriptPubKey.getPubKeyHash()
    assert(btc.keys.ecAddressToPKH("mhjfPZW5gTHetzzmSwpEqhvZC9TZ1sCAdu") == bytes.fromhex(pubKeyHash))
    
#
# Create a new block
#
def test_tc4():
    block = btc.mining.createNewBlock(address = "mhjfPZW5gTHetzzmSwpEqhvZC9TZ1sCAdu", 
                                    currentLastBlockHash = "40fd433db35e43c9997e702fb0f11bbe171712675651e03461fabb98fbc29598", 
                                    currentHeight = 109, 
                                    coinbasevalue = 50*10**8, 
                                    bits = int("207fffff",16), tx = [],
                                    mintime = int(time.time()))
    #
    # Verify that it has exactly one transaction and that this
    # is a coinbase transaction
    #
    tx = block.getTx()
    assert(1 == len(tx))
    assert(tx[0].isCoinbase())
    #
    # Check block
    #
    assert(btc.mining.checkBlock(block, currentLastBlock = "40fd433db35e43c9997e702fb0f11bbe171712675651e03461fabb98fbc29598"))
