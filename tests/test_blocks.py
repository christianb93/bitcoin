import btc.block

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
# Deserialize a block header
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


#
# Deserialize a block 
# 
def test_tc2():
    raw = '00000020df9e03f6f3b6089704150a0627841c9fb86adbf265fc8f31c95bb6b99e4a604c187d9b8d7dad469812834e9f4f72af649656b4179880d0102499118c7fd488d9bc69b65affff7f20030000000102000000010000000000000000000000000000000000000000000000000000000000000000ffffffff04016b0101ffffffff0200f2052a01000000232103bacc76145b9800c24b519cf659e6add26db1ea0b23806ae361f058e67d84bd04ac0000000000000000266a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf900000000'
    block = btc.block.block()
    raw = block.deserialize(raw)
    #
    # First check block header fields
    #
    blockHeader = block.getBlockHeader()
    assert(blockHeader.getVersion() == 0x20000000)
    assert(blockHeader.getPrevBlockId() == '4c604a9eb9b65bc9318ffc65f2db6ab89f1c8427060a15049708b6f3f6039edf')
    assert(blockHeader.getMerkleRoot() == 'd988d47f8c11992410d0809817b4569664af724f9f4e83129846ad7d8d9b7d18')
    assert(blockHeader.getCreationTime() == 1521904060)
    assert(blockHeader.getBits() == 545259519)
    assert(blockHeader.getNonce() == 3)
    #
    # Now check transactions
    #
    tx = block.getTx()
    assert(1 == len(tx))
    
    
#
# Deserialize a block with two transactions
#
def test_tc3():
    raw = '000000208b04e3a08be31c35257492f18bfac10c5ead328b5a4012473ef20a903cd49850bd11c56cf26bf256e4cdd00cd21b68c37f3b71d9614e9630226f5fa09b4104c1d7a1bf5affff7f20020000000202000000010000000000000000000000000000000000000000000000000000000000000000ffffffff04016c0101ffffffff02a803062a01000000232102a2f9ed878030526366b30093c00e32934f3c04a884f2844af2883ee453f0228dac0000000000000000266a24aa21a9ede8d2abc7618be366fa6688272429dac8512666a1610a72c6a72527c4698ccafc000000000200000001a88649b2ec24cb6fa07011acb68749461d7c438e8b89ddbcea3f5bac89e3ad2b010000006b483045022100ca652e20c2a0ceae370a2c037d8bbce09498c883a7a98a541e8f9fcea294d8c902207a16331540cd8a892186926646f99220489de0a9a9713f870b1c6989cf22948c012103f9fa8e3fba8af74b6c8ba4bd530000df4cc62bf0a50aeff58b6462888f79a5cefeffffff0280d1f008000000001976a914625d8e5d40a1b797b47cb66eee958724a668d8d288acd87adfa9000000001976a914731a59d04408789756ae353eeba6eefc975bfe7688ac1f000000'
    block = btc.block.block()
    block.deserialize(raw)
    #
    # First check block header fields
    #
    blockHeader = block.getBlockHeader()
    assert(blockHeader.getVersion() == 0x20000000)
    #
    # Now check transactions
    #
    tx = block.getTx()
    assert(2 == len(tx))
    #
    # Re-serialize the block manually and compare. The block header
    # has 80 bytes
    #
    _raw = raw[:2*80] + "02" + tx[0].serialize() +  tx[1].serialize()
    assert(_raw == raw)
    #
    # Also check the transaction hashes
    #
    assert(tx[0].getTxnId(byteorder="big") == '7a2470e0242a5dc141f3d260dd3e4c43a06bf2f827ac26d9d3686ad1949bcd66')
    assert(tx[1].getTxnId(byteorder="big") == 'b257a1ff6503d2d93fd5c8fc49c91c3cfc14f38f34788217320b32e4a30e9b40')


#
# Deserialize a block header
# 
def test_tc4():
    raw = '00000020df9e03f6f3b6089704150a0627841c9fb86adbf265fc8f31c95bb6b99e4a604c187d9b8d7dad469812834e9f4f72af649656b4179880d0102499118c7fd488d9bc69b65affff7f20030000000102000000010000000000000000000000000000000000000000000000000000000000000000ffffffff04016b0101ffffffff0200f2052a01000000232103bacc76145b9800c24b519cf659e6add26db1ea0b23806ae361f058e67d84bd04ac0000000000000000266a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf900000000'
    blockHeader = btc.block.blockHeader()
    blockHeader.deserialize(raw)
    assert(blockHeader.serialize() == raw[:160])
    
    
#
# Serialize a block with two transactions
#
def test_tc5():
    raw = '000000208b04e3a08be31c35257492f18bfac10c5ead328b5a4012473ef20a903cd49850bd11c56cf26bf256e4cdd00cd21b68c37f3b71d9614e9630226f5fa09b4104c1d7a1bf5affff7f20020000000202000000010000000000000000000000000000000000000000000000000000000000000000ffffffff04016c0101ffffffff02a803062a01000000232102a2f9ed878030526366b30093c00e32934f3c04a884f2844af2883ee453f0228dac0000000000000000266a24aa21a9ede8d2abc7618be366fa6688272429dac8512666a1610a72c6a72527c4698ccafc000000000200000001a88649b2ec24cb6fa07011acb68749461d7c438e8b89ddbcea3f5bac89e3ad2b010000006b483045022100ca652e20c2a0ceae370a2c037d8bbce09498c883a7a98a541e8f9fcea294d8c902207a16331540cd8a892186926646f99220489de0a9a9713f870b1c6989cf22948c012103f9fa8e3fba8af74b6c8ba4bd530000df4cc62bf0a50aeff58b6462888f79a5cefeffffff0280d1f008000000001976a914625d8e5d40a1b797b47cb66eee958724a668d8d288acd87adfa9000000001976a914731a59d04408789756ae353eeba6eefc975bfe7688ac1f000000'
    block = btc.block.block()
    block.deserialize(raw)
    assert(block.serialize() == raw)

