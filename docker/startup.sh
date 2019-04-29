#!/bin/sh
#
# See whether the environment variables BC_RPC_USER and BC_RPC_PASSWORD
# exist
#
if [ X$BC_RPC_USER != "X" ]; then
  if [ X$BC_RPC_PASSWORD != "X" ]; then
    echo "Creating new configuration file"
    echo "regtest=1" > $conf
    echo "server=1" >> $conf
    echo "rpcbind=0.0.0.0:18332" >> $conf
    echo "rpcuser=$BC_RPC_USER" >> $conf
    echo "rpcpassword=$BC_RPC_PASSWORD" >> $conf
    echo "rpcallowip=0.0.0.0/0" >> $conf
    echo "rpcport=18332" >> $conf
    cat $conf
  fi
fi
#
# Now start the actual daemon
#
/usr/local/bin/bitcoind -conf=/bitcoin.conf -regtest -rest=1 -server=1 -printtoconsole -txindex=1
