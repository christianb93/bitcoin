##########################################################################
#
# Test fixtures

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



import pytest


#
# A utility function to get the IP address of a container on the bridge network
# 
def get_ip(client, container, network_name="bridge"):
    nw = client.networks.get(network_name)
    ip = [_.attrs['NetworkSettings']['Networks']['bridge']['IPAddress'] for _ in nw.containers if _.id == container.id][0]
    return ip


@pytest.fixture
def startEnv(request):
    #
    # First we start the container
    #
    client = docker.client.from_env()
    alice = client.containers.run("bitcoin-alpine:latest", auto_remove=True, detach=True, ports={"18332" : "18332"})
    bob = client.containers.run("bitcoin-alpine:latest", auto_remove=True, detach=True)
    #
    # Give them some time to come up
    # 
    time.sleep(5)
    bob_ip = get_ip(client, bob)
    #
    # Ask alice to connect to bob
    # 
    alice.exec_run("bitcoin-cli --rpcuser=user --rpcpassword=password -regtest addnode " + bob_ip + " add")
    #
    # Now generate a few blocks
    #
    alice.exec_run("bitcoin-cli --rpcuser=user --rpcpassword=password -regtest generate 101");
    #
    # Set up an account Alice with address mkvAYmgqrEFEsJ9zGBi9Z87gP5rGNAu2mx
    # The private key for this address is (as WIF)
    # cQowgjRpUocje98dhJrondLbHNmgJgAFKdUJjCTtd3VeMfWeaHh7
    #
    alice.exec_run("bitcoin-cli --rpcuser=user --rpcpassword=password -regtest importprivkey cQowgjRpUocje98dhJrondLbHNmgJgAFKdUJjCTtd3VeMfWeaHh7")
    #
    # and verify
    # 
    # check=alice.exec_run("bitcoin-cli --rpcuser=user --rpcpassword=password -regtest dumpprivkey mkvAYmgqrEFEsJ9zGBi9Z87gP5rGNAu2mx")
    # assert(check.output == b'cQowgjRpUocje98dhJrondLbHNmgJgAFKdUJjCTtd3VeMfWeaHh7\n')
    #
    # Finally transfer 30 bitcoin to this address
    #
    alice.exec_run("bitcoin-cli --rpcuser=user --rpcpassword=password -regtest sendtoaddress mkvAYmgqrEFEsJ9zGBi9Z87gP5rGNAu2mx 30.0")
    #
    # and mine 6 additional blocks
    # 
    alice.exec_run("bitcoin-cli --rpcuser=user --rpcpassword=password -regtest generate 6");
    def fin():
        alice.stop()
        bob.stop()
    request.addfinalizer(fin)
    return True

