import btc.utils
import btc.keys

import binascii

        
    
#
# Run tests for the keys module
# 

def test_tc1():
    wif = "cRUmzVqx15eTrbJ55opBqwG9XbKMaTvNNySWSvZ8s4tEtbQDELUg"
    _payload = btc.keys.wif_to_payload_bytes(wif)
    d = int.from_bytes(_payload, byteorder='big')
    payload = binascii.hexlify(_payload).decode('ascii')
    assert(payload == "744d2e1c2bb33edb05de0467f9ce66b07d7339a50ca0f49081fb7eba02e8b5fd")
    assert(wif == btc.keys.payload_value_to_wif(d, version=239))
        
def test_tc2():
    pem = b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEQY845OuKlqJQIHOcDaC/2EPNvDEczaSx\n'
    pem = pem + b'pojzVBwhLmG+cEizi6XpSSIrTtiBh7lyxuHcxiba6J0aLwd6o2jHBg==\n-----END PUBLIC KEY-----\n'
    _X, _Y = btc.keys.public_point_from_pem(pem)
    X = int.from_bytes(_X, "big")
    Y = int.from_bytes(_Y, "big")
    assert(X == 29653386957644285094214794487095156456314684607297660684351363437249767222881)
    assert(Y == 86137829868349875656951651687933598437024590075828608787499242182788203988742)
 
def test_tc3():
    hex_uncompressed = "04418f38e4eb8a96a25020739c0da0bfd843cdbc311ccda4b1a688f3541c212e61be7048b38ba5e949222b4ed88187b972c6e1dcc626dae89d1a2f077aa368c706"
    X, Y = btc.keys.ec_point_hex_to_values(hex_uncompressed)
    assert(X == 29653386957644285094214794487095156456314684607297660684351363437249767222881)
    assert(Y == 86137829868349875656951651687933598437024590075828608787499242182788203988742)
    hex_compressed = "02418f38e4eb8a96a25020739c0da0bfd843cdbc311ccda4b1a688f3541c212e61"
    assert(btc.keys.ec_point_compress(X, Y) == bytes.fromhex(hex_compressed))
    assert(btc.keys.ec_point_compress_hex(X, Y) == hex_compressed)
    
def test_tc4():
    hex_compressed = "02418f38e4eb8a96a25020739c0da0bfd843cdbc311ccda4b1a688f3541c212e61"
    assert("mitu3NFAd83mPQnVVu6k1yd47VWLJ9JATd" == btc.keys.ec_address(hex_compressed, version=239))
    
# obtain public key hash160 from the address
def test_tc5():
    hex_compressed = "02418f38e4eb8a96a25020739c0da0bfd843cdbc311ccda4b1a688f3541c212e61"
    address = btc.keys.ec_address(hex_compressed, version=239)
    h = btc.keys.ec_address_to_pkh(address)
    assert(h == btc.utils.hash160(bytes.fromhex(hex_compressed)))
    
# The example on wordpress
def test_tc6():
    wif = "cVDUgUEahS1swavidSk1zdSHQpCy1Ac9XSQHkaxmZKcTTfEA5vTY"
    d = btc.keys.wif_to_payload(wif)
    assert(d == 103028256105408389446438916672504271192164767440296751065327418112299269382535)
    hex_compressed = "02e054ae47f44530f83edb73fe6c5b76b42f3ffab24e2cc12cdc4a77126831324e"
    assert("mx5zVKcjohqsu4G8KJ83esVxN52XiMvGTY" == btc.keys.ec_address(hex_compressed, version=239))
    
