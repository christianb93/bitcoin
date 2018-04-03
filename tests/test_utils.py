import btc.utils
import btc.keys
import btc.block

import binascii

#
# Run tests for the utils module
# 

    
def test_tc1():
    b = binascii.unhexlify("6f250ed017660abdd723ed28a427fda68a6eb0a3f8a46cfc54")
    s = btc.utils.base58Encode(b)
    assert( s == "mitu3NFAd83mPQnVVu6k1yd47VWLJ9JATd")
    assert(b == btc.utils.base58Decode(s))
    assert( s == "mitu3NFAd83mPQnVVu6k1yd47VWLJ9JATd")
    pass
    
def test_tc2():
    b = bytes([0])
    assert(btc.utils.base58Encode(b) == "1")
        
def test_tc3():
    b = b'\0\0'
    assert(btc.utils.base58Encode(b) == "11")
        
def test_tc4():
    assert(bytes([0,0]) == btc.utils.base58Decode("11"))
        
def test_tc5():
    x = bytes.fromhex("12acfe")
    h = btc.utils.hash160(x)
    assert(binascii.hexlify(h).decode('ascii') == "943306d56854ce44ba9454c4a0d874cf41fb243d")
    

def test_tc6():
    #
    # This should be a valid signature script - taken from bitcoin.info, txid = 1d76bfb6d913b6aee62776271b643f9ef353065cbdad3bd9723cd050744ccc13
    #
    s = "3045022100843d0108b411452da23ce8b9041368300f11a042716a9ae8f3aaa2e5fe39654c022079864ef33971a7cef3aef4658c1d2dec5a5e27b5e7e41c5722fc192dd84472da01"
    assert(True == btc.utils.isValidDERSignature(s))

def test_tc7():
    s = "3045022011f9373730c3eb9785e9c31e3e32611b50b33e9eb7c7a92f94162523bb3fbeef0221009b1ec63d55353d536c45bd5e77b223fd47a31da8b25a074e043fa650027f77f001"
    assert(True == btc.utils.isValidDERSignature(s))
    
def test_tc8():
    b = bytes([])
    assert(btc.utils.base58Encode(b) == "")
    
    
def test_tc9():
    s = ""
    assert(btc.utils.base58Decode(s) == bytes([]))
    
    
#
# Test Merkle root
#
def test_tc10():
    raw = '000000208b04e3a08be31c35257492f18bfac10c5ead328b5a4012473ef20a903cd49850bd11c56cf26bf256e4cdd00cd21b68c37f3b71d9614e9630226f5fa09b4104c1d7a1bf5affff7f20020000000202000000010000000000000000000000000000000000000000000000000000000000000000ffffffff04016c0101ffffffff02a803062a01000000232102a2f9ed878030526366b30093c00e32934f3c04a884f2844af2883ee453f0228dac0000000000000000266a24aa21a9ede8d2abc7618be366fa6688272429dac8512666a1610a72c6a72527c4698ccafc000000000200000001a88649b2ec24cb6fa07011acb68749461d7c438e8b89ddbcea3f5bac89e3ad2b010000006b483045022100ca652e20c2a0ceae370a2c037d8bbce09498c883a7a98a541e8f9fcea294d8c902207a16331540cd8a892186926646f99220489de0a9a9713f870b1c6989cf22948c012103f9fa8e3fba8af74b6c8ba4bd530000df4cc62bf0a50aeff58b6462888f79a5cefeffffff0280d1f008000000001976a914625d8e5d40a1b797b47cb66eee958724a668d8d288acd87adfa9000000001976a914731a59d04408789756ae353eeba6eefc975bfe7688ac1f000000'
    block = btc.block.block()
    block.deserialize(raw)
    #
    # Get the blocks Merkle Root in little endian
    #
    m = btc.utils.blockMerkleRoot(block)
    #
    # Convert to big endian to be able to compare it
    #
    m = btc.serialize.serializeString(m, len(m))
    assert(block.getBlockHeader().getMerkleRoot() == m)
    
#
# Get one more block from blockchain.info and test it. Make sure to get an early block as our decoding does
# not yet support the segregated witness feature - this is block #100001
#
def test_tc11():
    raw = btc.utils.getRawBlock("00000000000080b66c911bd5ba14a74260057311eaeb1982802f7010f1a9f090")
    block = btc.block.block()
    block.deserialize(raw)
    #
    # Get the blocks Merkle Root in little endian
    #
    m = btc.utils.blockMerkleRoot(block)
    #
    # Convert to big endian to be able to compare it
    #
    m = btc.serialize.serializeString(m, len(m))
    assert(block.getBlockHeader().getMerkleRoot() == m)
