from twisted.internet import reactor, protocol, threads

class EchoClient(protocol.Protocol):
  def connectionMade(self):
    print("Connected to server. Type your message:")
    self.getMessageAsync()

  def dataReceived(self, data):
    print(f"Server: {data.decode().strip()}")
    if data.strip() == b"Goodbye!": return
    self.getMessageAsync()

  def getMessageAsync(self):
    threads.deferToThread(self.getMessage)

  def getMessage(self):
    message = input("> ")
    self.transport.write(message.encode() + b"\n")

class EchoClientFactory(protocol.ClientFactory):
  def buildProtocol(self, addr):
    print(f"Connection to {addr.host}:{addr.port}")
    return EchoClient()

  def clientConnectionFailed(self, connector, reason):
    print("Connection failed:", reason)
    reactor.stop()

  def clientConnectionLost(self, connector, reason):
    print("Connection closed.")
    reactor.stop()

reactor.connectTCP("localhost", 8000, EchoClientFactory())
reactor.run()
