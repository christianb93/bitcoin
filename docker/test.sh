#
# Test a container. Assumes that you have executed the command
# in run.sh to spin up a container listening on port 18332
#
bitcoin-cli -regtest -rpcuser=user -rpcpassword=password  getinfo
