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
  
  @request
  def increment(self, graph):
    graph = JSONToGraph(graph)
    print('\n\n this is the type of the graph ' type(graph))
    graph.val += 1;
    for c in graph.children:
        self.increment(c)

  def JSONToGraph(self, jsonString):
    jsonArr = jsonString.split('\n')
    name = jsonArr[0].split(':')[1]
    val = jsonArr[1].split(':')[1]
    children = []
    for c in jsonArr[3].split(','):
      children.append(self.JSONToGraph(c))
    graph = node(name, children)
    print('\n\n this is the type of the graph2312 ' +  type(graph))
    graph.val = val
    return graph

# Quick-and-dirty TCP Server:
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('localhost', 50003))
ss.listen(10)

while True:
  s, _ = ss.accept()
  # JSONRpc object spawns internal thread to serve the connection.
  JSONRpc(s, ServerServices(),framing_cls=JSONFramingNone)

