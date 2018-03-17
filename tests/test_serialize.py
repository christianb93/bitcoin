import btc.serialize

def test_tc1():
    #
    # Deserialize a varInt
    #
    s = "1a"
    x, s = btc.serialize.deserializeVarInt(s)
    assert(x == 26)
    assert(s == "")


def test_tc2():
    #
    # Deserialize a varInt with three bytes
    #
    s = "fd1a03"
    x, s = btc.serialize.deserializeVarInt(s)
    assert(hex(x) == "0x31a")
    assert(s == "")


def test_tc3():
    #
    # Deserialize a varInt with four bytes
    #
    s = "fe1a030400"
    x, s = btc.serialize.deserializeVarInt(s)
    assert(hex(x) == "0x4031a")
    assert(s == "")
    
    
def test_tc4():
    #
    # Deserialize a varInt with more than four bytes
    #
    s = "ff0102030405060000"
    x, s = btc.serialize.deserializeVarInt(s)
    assert(hex(x) == "0x60504030201")
    assert(s == "")

def test_tc5():
    #
    # Deserialize a unit32 (four bytes)
    #
    s = "01020304"
    x, s = btc.serialize.deserializeUint32(s)
    assert(hex(x) == "0x4030201")
    assert(s == "")
    
    
def test_tc6():
    #
    # Deserialize a string
    #
    s = "abcdef"
    x, s = btc.serialize.deserializeString(s, 2)
    assert(x == "cdab")
    assert(s == "ef")
    
def test_tc10():
    #
    # Serialize a number
    #
    s = "0102030405060000"
    x, _ = btc.serialize.deserializeNumber(s, 8)
    _s = btc.serialize.serializeNumber(x, 8)
    assert(_s == s)

def test_tc11():
    #
    # Serialize a string
    #
    s = "abcdef"
    x, _ = btc.serialize.deserializeString(s, 3)
    assert(x == "efcdab")
    _s = btc.serialize.serializeString(x, 3)
    assert(_s == s)
    

def test_tc12():
    #
    # Serialize a varInt
    #
    s = "1a"
    x, _ = btc.serialize.deserializeVarInt(s)
    assert(x == 26)
    _s = btc.serialize.serializeVarInt(x)
    assert(_s == s)


def test_tc13():
    #
    # Serialize a varInt with three bytes
    #
    s = "fd1a03"
    x, _ = btc.serialize.deserializeVarInt(s)
    assert(hex(x) == "0x31a")
    _s = btc.serialize.serializeVarInt(x)
    assert(_s == s)


def test_tc14():
    #
    # Deserialize a varInt with four bytes
    #
    s = "fe1a030400"
    x, _ = btc.serialize.deserializeVarInt(s)
    assert(hex(x) == "0x4031a")
    _s = btc.serialize.serializeVarInt(x)
    assert(_s == s)
    

def test_tc15():
    #
    # Sserialize a varInt with more than four bytes
    #
    s = "ff0102030405060000"
    x, _ = btc.serialize.deserializeVarInt(s)
    assert(hex(x) == "0x60504030201")
    _s = btc.serialize.serializeVarInt(x)
    assert(_s == s)

def test_tc16():
    #
    # Serialize a unit32 (four bytes)
    #
    s = "01020304"
    x, _ = btc.serialize.deserializeUint32(s)
    assert(hex(x) == "0x4030201")
    assert(s == btc.serialize.serializeUint32(x))
    
    
