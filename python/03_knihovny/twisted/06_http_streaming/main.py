from twisted.internet import reactor, protocol

class SimpleHTTPServer(protocol.Protocol):
  parts = [
    (
      "<!DOCTYPE html>"
      "<html>"
      "  <head>"
      "    <title>Hello, World!</title>"
      "  </head>"
      "  <body>"
    ),
    "<h1>Page Title</h1>",
    "<p>Page Content</p>",
    "<ul>",
    "<li>Hi!</li></ul>",
    "",
  ]

  def dataReceived(self, data):
    responseHeader = (
      "HTTP/1.1 200 OK\r\n"
      "Content-Type: text/html; charset=utf-8\r\n"
      "Transfer-Encoding: chunked\r\n"
      "Connection: close\r\n"
      "\r\n"
    )

    self.transport.write(responseHeader.encode())
    self.sendChunk()

  def sendChunk(self):
    if not len(self.parts):
      self.transport.loseConnection()
      return

    chunk = self.transformChunk(self.parts.pop(0))
    self.transport.write(chunk)

    reactor.callLater(2, self.sendChunk)

  def transformChunk(self, chunk):
    return f"{len(chunk):x}\r\n{chunk}\r\n".encode()

class SimpleHTTPFactory(protocol.Factory):
  def buildProtocol(self, addr):
    print(f"Connection from {addr.host}:{addr.port}")
    return SimpleHTTPServer()

reactor.listenTCP(8080, SimpleHTTPFactory())
reactor.run()
