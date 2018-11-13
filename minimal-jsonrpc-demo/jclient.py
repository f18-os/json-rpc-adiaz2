# minimalistic client example from 
# https://github.com/seprich/py-bson-rpc/blob/master/README.md#quickstart

import socket
from node import *
from bsonrpc import JSONRpc
from bsonrpc.exceptions import FramingError
from bsonrpc.framing import (
	JSONFramingNetstring, JSONFramingNone, JSONFramingRFC7464)

# Cut-the-corners TCP Client:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 50003))

rpc = JSONRpc(s,framing_cls=JSONFramingNone)
server = rpc.get_peer_proxy()

# Execute in server:
leaf1 = node("leaf1")
leaf2 = node("leaf2")

root = node("root", [leaf1, leaf1, leaf2])

print("graph before increment")
root.show()

def graphToJSON(graph):
    jsonString = 'name: ' + graph.name + '\n'
    jsonString += 'val: ' + str(graph.val) + '\n'
    jsonString += 'children: {\n'
    for c in graph.children:
         jsonString += graphToJSON(c)
         jsonString += ','
    jsonString += '}'
    return jsonString

result = server.increment(graphToJSON(root))

print("graph after increment")
root.show()

# "!dlroW olleH"

print(result)

print(server.nop({1:[2,3]}))

rpc.close() # Closes the socket 's' also


