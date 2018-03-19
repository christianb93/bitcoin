FROM alpine:3.7 as build

#
# First get all the packages for 
# the compile
#
RUN apk update && apk add git \ 
                          make \
                          file \
                          autoconf \
                          automake \ 
                          build-base \
                          libtool \
                          db-c++ \
                          db-dev \
                          boost-system \
                          boost-program_options \
                          boost-filesystem \ 
                          boost-dev \ 
                          libressl-dev \ 
                          libevent-dev 

#
# Pull source code
#
RUN git clone https://github.com/bitcoin/bitcoin --branch v0.15.0 --single-branch

#
# Do the actual build
#
RUN (cd bitcoin  && ./autogen.sh && \
                      ./configure --disable-tests \
                      --disable-bench --disable-static  \
                      --without-gui --disable-zmq \ 
                      --with-incompatible-bdb \
                      CFLAGS='-w' CXXFLAGS='-w' && \
                      make -j 4 && \
                      strip src/bitcoind && \
                      strip src/bitcoin-cli && \
                      strip src/bitcoin-tx && \
                      make install )


FROM alpine:3.7

#
# Copy the binaries from the build to our new container
#
COPY --from=build /usr/local/bin/bitcoind /usr/local/bin

#
# Install all dependencies
#
RUN apk update && apk add boost boost-filesystem \
            boost-program_options \
            boost-system boost-thread busybox db-c++ \
            libevent libgcc libressl2.6-libcrypto \ 
            libstdc++ musl

#
# Copy the bitcoin.conf file from
# the build context into the container
#
COPY bitcoin.conf /bitcoin.conf

#
# Expose the port for the RPC interface
#
EXPOSE 18332/tcp

#
# Start the bitcoin server
#
ENTRYPOINT ["/usr/local/bin/bitcoind"]
CMD ["-conf=/bitcoin.conf", "-regtest", "-rest=1", "-server=1", "-printtoconsole", "-txindex=1"]




