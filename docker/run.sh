#
# Run a container with port 18332 (regtest) exposed
#
docker run --rm -it --net=bridge -p 18332:18332  bitcoin-alpine
