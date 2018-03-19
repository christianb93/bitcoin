#
# Uncomment the following lines only if you
# want to build all the intermediate steps as
# well
#

#docker build -f Dockerfile.dev -t alpine-dev .
#docker build -f Dockerfile.build -t bitcoin-alpine-build .
#docker build -f Dockerfile.install -t bitcoin-alpine-bin .
#docker build -f Dockerfile.run -t bitcoin-alpine-run .
#docker build -f Dockerfile.staged -t bitcoin-alpine-run-staged .

#
# Typically this will be the only one you need
#
docker build --rm -f Dockerfile -t bitcoin-alpine .
