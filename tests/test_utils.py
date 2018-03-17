import btc.utils
import btc.keys

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
