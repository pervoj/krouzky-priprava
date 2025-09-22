# https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers
# https://en.wikipedia.org/wiki/WebSocket

# pip install bitarray

from twisted.internet import reactor, protocol
from os.path import join, dirname, basename, isfile, isdir
from mimetypes import guess_type
from chardet import detect as detect_charset
from hashlib import sha1
from base64 import b64encode
from bitarray import bitarray
from typing import Sequence

statusTexts = {
  101: "Switching Protocols",
  200: "OK",
  404: "Not Found",
  500: "Internal Server Error",
}

resource_dir = join(dirname(__file__), "files")

class HttpServerProtocol(protocol.Protocol):
  has_ws_handshake = False

  def dataReceived(self, data):
    if self.has_ws_handshake:
      self.handleWsMessage(data)
      return

    request = self.parseRequest(data)

    if self.isWsHandshake(request):
      self.wsHandshake(request)
      return

    file_path = join(resource_dir, request["path"].lstrip("/"))

    if not basename(file_path).startswith("_"):

      if isfile(file_path):
        self.sendFile(file_path, request)
        return

      if isdir(file_path):
        index_path = join(file_path, "index.html")
        if isfile(index_path):
          self.sendFile(index_path, request)
          return

    self.send404(request)

  def sendWsMessage(self, payload: Sequence[int], is_last_message = True, opcode = 2, masking_key: Sequence[int] | None = None):
    payload_bytes = bytearray(payload)
    message_bytes = bytearray()

    header_bit_string = ""

    header_bit_string += "1" if is_last_message else "0" # FIN
    header_bit_string += "000" # RSV1, RSV2, RSV3
    header_bit_string += f"{opcode:04b}" # opcode
    header_bit_string += "0" if masking_key is None else "1" # mask

    payload_length = len(payload_bytes)
    if payload_length <= 125:
      header_bit_string += f"{payload_length:07b}"
    elif payload_length < 2 ** 16:
      header_bit_string += f"{126:07b}{payload_length:016b}"
    elif payload_length < 2 ** 64:
      header_bit_string += f"{127:07b}{payload_length:064b}"
    else:
      raise ValueError("Payload too large")

    header = bitarray(header_bit_string)
    message_bytes.extend(header.tobytes())

    if masking_key is not None:
      key = bytearray(masking_key)
      if len(key) != 4:
        raise ValueError("Invalid masking key length")
      message_bytes.extend(key)
      message_bytes.extend(self.wsMaskPayload(payload_bytes, key))
    else:
      message_bytes.extend(payload_bytes)

    self.transport.write(bytes(message_bytes))

  def handleWsMessage(self, message: bytes):
    message_bytes = bytearray(message)

    header_bits = bitarray()
    header_bits.frombytes(message_bytes[:2])
    message_bytes = message_bytes[2:]

    fin = header_bits[0]
    opcode = int.from_bytes(bitarray("0000" + header_bits[4:8].to01()).tobytes())
    mask = header_bits[8]

    is_last_message = fin == 1
    is_masked = mask == 1

    length = int.from_bytes(bitarray("0" + header_bits[9:16].to01()).tobytes())

    if length > 125:
      if length == 126:
        length = int.from_bytes(bytes(message_bytes[:2]))
        message_bytes = message_bytes[2:]
      elif length == 127:
        length = int.from_bytes(bytes(message_bytes[:8]))
        message_bytes = message_bytes[8:]
      else:
        raise ValueError("Invalid length")

    masking_key = None
    if is_masked:
      masking_key = bytes(message_bytes[:4])
      message_bytes = message_bytes[4:]

    data_slice = message_bytes[:length]
    if is_masked:
      data_slice = self.wsMaskPayload(data_slice, masking_key)

    payload = bytes(data_slice)

    self.factory.handleWsMessage(payload, opcode)

  def wsMaskPayload(self, payload: Sequence[int], key: Sequence[int] | None = None):
    payload_bytes = bytearray(payload)
    if key is None:
      return payload_bytes

    if len(key) != 4:
      raise ValueError("Invalid masking key length")

    masked_payload = bytearray()
    masking_key = bytearray(key)

    for i in range(len(payload_bytes)):
      masked_payload.append(payload_bytes[i] ^ masking_key[i % 4])

    return masked_payload

  def wsHandshake(self, request: dict):
    version = request["headers"]["Sec-WebSocket-Version"]
    key = request["headers"]["Sec-WebSocket-Key"]
    self.has_ws_handshake = True

    print("WebSocket handshake:", version, key)

    magicStringBytes = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    acceptValue = key.encode() + magicStringBytes
    acceptHash = b64encode(sha1(acceptValue).digest()).decode()

    response = self.generateResponse(101, {
      "Connection": "upgrade",
      "Upgrade": "websocket",
      "Sec-WebSocket-Accept": acceptHash,
    }, b"")

    self.transport.write(response)
    self.factory.handleWsConnection(self)

  def connectionLost(self, reason):
    self.factory.handleWsDisconnection(self)

  def isWsHandshake(self, request: dict):
    return request["method"] == "GET" \
      and "Sec-WebSocket-Key" in request["headers"] \
      and "Sec-WebSocket-Version" in request["headers"] \
      and request["headers"]["Connection"].lower() == "upgrade" \
      and request["headers"]["Upgrade"].lower() == "websocket"

  def send404(self, request: dict):
    file_path = join(resource_dir, "_404.html")

    if isfile(file_path):
      self.sendFile(file_path, request, 404)
      return

    self.sendResponse(404, {}, b"")

  def sendFile(self, file_path: str, request: dict, status: int = 200):
    file = open(file_path, "rb")
    body = file.read()
    file.close()

    headers = {}

    file_type, encoding = guess_type(file_path)

    if file_type:
      headers["Content-Type"] = file_type

      if file_type.startswith("text/"):
        charset = detect_charset(body)["encoding"]

        if charset:
          headers["Content-Type"] += f"; charset={charset}"

    if encoding:
      headers["Content-Encoding"] = encoding

    self.sendResponse(status, headers, body)

  def sendResponse(self, status: int, headers: dict, body: bytes):
    response = self.generateResponse(status, headers, body)
    self.transport.write(response)
    self.transport.loseConnection()

  def generateResponse(self, status: int, headers: dict, body: bytes):
    statusText = statusTexts.get(status, "Unknown")
    responseHeaderLines = [f"HTTP/1.1 {status} {statusText}"]

    if "Content-Length" not in headers:
      headers["Content-Length"] = len(body)

    if "Connection" not in headers:
      headers["Connection"] = "close"

    for key, value in headers.items():
      responseHeaderLines.append(f"{key}: {value}")

    responseHeader = "\r\n".join(responseHeaderLines).encode()
    return responseHeader + b"\r\n\r\n" + body

  def parseRequest(self, request: bytes):
    lines = request.split(b"\r\n")
    method, path, version = lines.pop(0).decode().split(" ")

    headers = {}
    while True:
      if not lines: break
      line = lines.pop(0)
      if not line: break
      key, value = line.decode().split(": ")
      headers[key] = value

    body = b"\r\n".join(lines)
    if not body: body = None

    return {
      "method": method,
      "path": path,
      "version": version,
      "headers": headers,
      "body": body
    }

class HttpServerFactory(protocol.Factory):
  ws_connections = []

  def buildProtocol(self, addr):
    print(f"Připojení z {addr.host}:{addr.port}")
    connection =  HttpServerProtocol()
    connection.factory = self
    return connection

  def handleWsConnection(self, connection):
    if connection not in self.ws_connections:
      self.ws_connections.append(connection)

  def handleWsDisconnection(self, connection):
    if connection in self.ws_connections:
      self.ws_connections.remove(connection)

  def handleWsMessage(self, message: bytes, opcode: int = 2):
    for connection in self.ws_connections:
      if connection.has_ws_handshake:
        connection.sendWsMessage(message, opcode = opcode)

reactor.listenTCP(1234, HttpServerFactory())
reactor.run()
