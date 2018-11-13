import socket
from bsonrpc import JSONRpc
from node import *
from bsonrpc import request, service_class
from bsonrpc.exceptions import FramingError
from bsonrpc.framing import (
	JSONFramingNetstring, JSONFramingNone, JSONFramingRFC7464)

# Class providing functions for the client to use:
@service_class
class ServerServices(object):

  @request
  def swapper(self, txt):
    return ''.join(reversed(list(txt)))

  @request
  def nop(self, txt):
    print(txt)
    return txt

  def JSONToGraph(self, jsonString):
    jsonArr = jsonString.split('\n')
    name = jsonArr[0].split(':')[1]
    val = jsonArr[1].split(':')[1]
    children = []
    for c in jsonString[jsonString.find("{")+1:].split(',')[:-1]:
        children.append(self.JSONToGraph(c))
    graph = node(name, children)
    graph.val = int(val)
    return graph

  def graphToJSON(self, graph):
    jsonString = 'name: ' + graph.name + '\n'
    jsonString += 'val: ' + str(graph.val) + '\n'
    jsonString += 'children: {'
    for c in graph.children:
         jsonString += self.graphToJSON(c)
         jsonString += ','
    jsonString += '}'
    return jsonString

  @request
  def increment(self, graph):
    graph = self.JSONToGraph(graph)
    graph.val += 1
    for i in range(len(graph.children)):
        graph.children[i] = self.JSONToGraph(self.increment(self.graphToJSON(graph.children[i]), self.graphToJSON(graph.children[i])))
    return self.graphToJSON(graph)


# Quick-and-dirty TCP Server:
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('localhost', 50017))
ss.listen(10)

while True:
  s, _ = ss.accept()
  # JSONRpc object spawns internal thread to serve the connection.
  JSONRpc(s, ServerServices(),framing_cls=JSONFramingNone)

