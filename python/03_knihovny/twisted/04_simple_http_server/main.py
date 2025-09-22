from twisted.internet import reactor, protocol
from os.path import join, dirname, exists, isfile

resBody = """
<!DOCTYPE html>
<html>
  <head>
    <title>Hello, World!</title>
  </head>
  <body>
    <h1>Hello, World!</h1>
    <p>První webový server v Twisted!</p>
  </body>
</html>
""".strip()

class HelloWorldProtocol(protocol.Protocol):
  def dataReceived(self, data):
    msg = data.strip().decode()
    lines = msg.split("\r\n")

    method, path, version = lines[0].split(" ")
    print(f"Požadavek: {path}, ({method})")

    file_path = join(dirname(__file__), path.lstrip("/"))
    if exists(file_path) and isfile(file_path):
      print("Odpovídám souborem")

      f = open(file_path, "rb")
      content = f.read()
      f.close()

      res = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(content)}\r\n"
        "Connection: close\r\n"
        "\r\n"
      )

      self.transport.write(res.encode())
      self.transport.write(content)
      self.transport.loseConnection()
      return

    res = (
      "HTTP/1.1 200 OK\r\n"
      "Content-Type: text/html; charset=utf-8\r\n"
      f"Content-Length: {len(resBody)}\r\n"
      "Connection: close\r\n"
      "\r\n"
      f"{resBody}"
    )

    self.transport.write(res.encode())
    self.transport.loseConnection()

class HelloWorldFactory(protocol.Factory):
  def buildProtocol(self, addr):
    print(f"Připojení z {addr.host}:{addr.port}")
    return HelloWorldProtocol()

reactor.listenTCP(1234, HelloWorldFactory())
reactor.run()
