from twisted.internet import reactor, protocol

class EchoServer(protocol.Protocol):
  def dataReceived(self, data):
    message = data.strip()
    print(f"Received: {message.decode()}")

    if message.lower() == b"quit":
      self.transport.write(b"Goodbye!\n")
      self.transport.loseConnection()
    else:
      self.transport.write(b"You said: " + message + b"\n")

class EchoFactory(protocol.Factory):
  def buildProtocol(self, addr):
    print(f"Connection from {addr.host}:{addr.port}")
    return EchoServer()

reactor.listenTCP(8000, EchoFactory())
reactor.run()
