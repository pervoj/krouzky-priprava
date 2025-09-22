# https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers
# https://en.wikipedia.org/wiki/WebSocket

# pip install bitarray

from twisted.internet import reactor, protocol
from hashlib import sha1
from base64 import b64encode
from bitarray import bitarray

resBody = f"""
  <!DOCTYPE html>
    <html>
      <head>
        <title>Hello, World!</title>
      </head>
      <body>
        <h1>Hello, World!</h1>
      </body>
  </html>
""".strip()

class SimpleWSServer(protocol.Protocol):
  hasWsHandshake = False

  def dataReceived(self, data):
    if self.hasWsHandshake:
      self.wsMessage(data)
      return

    request = self.parseRequest(data.decode())

    if self.isWsRequest(request):
      self.wsHandshake(request)
      return

    response = (
      "HTTP/1.1 200 OK\r\n"
      "Content-Type: text/html; charset=utf-8\r\n"
      f"Content-Length: {len(resBody)}\r\n"
      "Connection: close\r\n"
      "\r\n"
      f"{resBody}"
    )

    self.transport.write(response.encode())
    self.transport.loseConnection()

  def wsMessage(self, data):
    bytesData = bytearray(data)

    header = bitarray()
    header.frombytes(bytes(bytesData[:2]))
    bytesData = bytesData[2:]

    fin = header[0]
    opcode = int.from_bytes(bitarray("0000" + header[4:8].to01()).tobytes())
    mask = header[8]

    isLastMessage = fin == 1
    isMasked = mask == 1

    length = int.from_bytes(bitarray("0" + header[9:16].to01()).tobytes())

    if length > 125:
      if length == 126:
        length = int.from_bytes(bytes(bytesData[:2]))
        bytesData = bytesData[2:]
      elif length == 127:
        length = int.from_bytes(bytes(bytesData[:8]))
        bytesData = bytesData[8:]
      else:
        self.transport.loseConnection()

    maskingKey = None
    if isMasked:
      maskingKey = bytes(bytesData[:4])
      bytesData = bytesData[4:]

    dataSlice = bytesData[:length]
    if isMasked:
      dataSlice = bytearray([dataSlice[i] ^ maskingKey[i % 4] for i in range(len(dataSlice))])

    payload = None
    if opcode == 1:
      payload = bytes(dataSlice).decode()
    elif opcode == 2:
      payload = bytes(dataSlice)

    if payload == "close":
      print("  WebSocket close")
      self.transport.loseConnection()
      return

    print(f"  WebSocket message: {payload}")

  def wsHandshake(self, request):
    version = request["headers"]["Sec-WebSocket-Version"]
    key = request["headers"]["Sec-WebSocket-Key"]
    self.hasWsHandshake = True

    print("  WebSocket handshake:", version, key)

    magicStringBytes = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    acceptValue = key.encode() + magicStringBytes
    acceptHash = b64encode(sha1(acceptValue).digest()).decode()

    response = (
      "HTTP/1.1 101 Switching Protocols\r\n"
      "Connection: upgrade\r\n"
      "Upgrade: websocket\r\n"
      f"Sec-WebSocket-Accept: {acceptHash}\r\n"
      "\r\n"
    )

    self.transport.write(response.encode())

  def isWsRequest(self, request):
    return request["headers"]["Connection"].lower() == "upgrade" \
      and request["headers"]["Upgrade"].lower() == "websocket"

  def parseRequest(self, requestString: str):
    lines = requestString.split("\r\n")
    method, path, version = lines.pop(0).split(" ")

    headers = {}

    while True:
      if not lines: break
      line = lines.pop(0)
      if not line: break
      key, value = line.split(": ")
      headers[key] = value

    body = "\r\n".join(lines)
    if not body: body = None

    return {
      "method": method,
      "path": path,
      "version": version,
      "headers": headers,
      "body": body,
    }

class SimpleWSFactory(protocol.Factory):
  connections = []

  def buildProtocol(self, addr):
    print(f"Connection from {addr.host}:{addr.port}")
    connection = SimpleWSServer()
    self.connections.append(connection)
    return connection

reactor.listenTCP(8080, SimpleWSFactory())
reactor.run()
