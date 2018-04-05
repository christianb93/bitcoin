# Bitcoin Python package and sample code

This is a collection of python code snippets and modules to play with the bitcoin protocol. The code is intended as an illustration for the posts on my blog www.leftasexercise.com. A short summary of contents:

* The **Python package** btc that contains modules to work with the bitcoin protocol, i.e. to serialize and deserialize transactions and blocks, to create and sign transactions or to communicate with the RPC interface of bitcoin core
* **Docker images** for bitcoin core based on the Alpine Linux distribution
* Sample code for **elliptic curve cryptography**
* Examples that demonstrate how the btc package can be used to work with **bitcoin keys** and to display and create **transactions** 
* A simple **miner** in Python (obviously not good for production use, but for a local test environment)

DISCLAIMER: Please note that this code is published for educational purposes only and under the MIT license. I strongly discourage the use of this code in any production system! Many features of the real bitcoin network are not supported (so far, for instance, I have not added support for the segregated witness feature) and using this on the main net would be a huge security risk and you would probably loose money! So DO NO DO THIS!


