from twisted.internet import reactor, protocol

class HelloWorld(protocol.Protocol):
  def connectionMade(self):
    self.transport.write(b"Hello, World!\n")
    self.transport.loseConnection()

class HelloFactory(protocol.Factory):
  def buildProtocol(self, addr):
    print(f"Connection from {addr.host}:{addr.port}")
    return HelloWorld()

reactor.listenTCP(8000, HelloFactory())
reactor.run()
