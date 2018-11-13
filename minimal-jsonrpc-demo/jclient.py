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
s.connect(('localhost', 50017))

rpc = JSONRpc(s,framing_cls=JSONFramingNone)
server = rpc.get_peer_proxy()

# Execute in server:
leaf1 = node("leaf1")
leaf2 = node("leaf2")

root = node("root", [leaf1, leaf1, leaf2])

def JSONToGraph(jsonString):
    jsonArr = jsonString.split('\n')
    name = jsonArr[0].split(':')[1]
    val = jsonArr[1].split(':')[1]
    children = []
    for c in jsonString[jsonString.find("{")+1:].split(',')[:-1]:
        children.append(JSONToGraph(c))
    graph = node(name, children)
    graph.val = int(val)
    return graph

def graphToJSON(graph):
    jsonString = 'name: ' + graph.name + '\n'
    jsonString += 'val: ' + str(graph.val) + '\n'
    jsonString += 'children: {'
    for c in graph.children:
         jsonString += graphToJSON(c)
         jsonString += ','
    jsonString += '}'
    return jsonString


jsonString = graphToJSON(root)


JSONToGraph(jsonString).show()

print('time to run this shit\n\n\n\n')
result = server.increment(jsonString)
print(result)
result = JSONToGraph(result)
print("graph after increment")
result.show()

print(server.nop({1:[2,3]}))

rpc.close() # Closes the socket 's' also
