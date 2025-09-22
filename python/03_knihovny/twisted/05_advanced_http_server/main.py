# https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview

from twisted.internet import reactor, protocol
from os.path import join, dirname, basename, isfile, isdir
from mimetypes import guess_file_type
from chardet import detect as detect_charset
from php import run_php

statusTexts = {
  200: "OK",
  404: "Not Found",
  500: "Internal Server Error",
}

resource_dir = join(dirname(__file__), "files")

class AdvancedHTTPServer(protocol.Protocol):
  def __init__(self, server_address: str):
    self.server_address = server_address

  def dataReceived(self, data):
    request = self.parseRequest(data)

    print(f"{request['method']} {request['full_path']}")

    file_path = join(resource_dir, request["path"].strip("/"))

    if not basename(file_path).startswith("_"):

      if isfile(file_path):
        self.sendFile(file_path, request)
        return

      if isdir(file_path):
        index_file_path = join(file_path, "index.php")

        if not isfile(index_file_path):
          index_file_path = join(file_path, "index.html")

        if isfile(index_file_path):
          self.sendFile(index_file_path, request)
          return

    self.send404(request)

  def send404(self, request: dict):
    file_path = join(resource_dir, "_404.php")

    if not isfile(file_path):
      file_path = join(resource_dir, "_404.html")

    if isfile(file_path):
      self.sendFile(file_path, request, 404)
      return

    self.sendResponse(404, {}, b"")

  def sendFile(self, filepath: str, request: dict, status: int = 200):
    if basename(filepath).endswith(".php"):
      self.sendPhp(filepath, request, status)
      return

    file = open(filepath, "rb")
    resBody = file.read()
    file.close()

    headers = {}

    file_type, encoding = guess_file_type(filepath)

    if file_type:
      headers["Content-Type"] = file_type

      if file_type.startswith("text/"):
        charset = detect_charset(resBody)["encoding"]

        if charset:
          headers["Content-Type"] += f"; charset={charset}"

    if encoding:
      headers["Content-Encoding"] = encoding

    self.sendResponse(status, headers, resBody)

  def sendPhp(self, filepath: str, request: dict, defaultStatus: int):
    server_name = request["headers"]["Host"] or "localhost"
    status, headers, body = run_php(resource_dir, filepath, request, self.server_address, server_name)
    if not status: status = defaultStatus
    self.sendResponse(status, headers, body)

  def sendResponse(self, status: int, headers: dict, body: bytes):
    response = self.generateResponse(status, headers, body)
    self.transport.write(response)
    self.transport.loseConnection()

  def generateResponse(self, status: int, headers: dict, body: bytes):
    statusText = statusTexts.get(status, "Unknown")
    responseHeaderLines = [f"HTTP/1.1 {status} {statusText}"]

    if "Content-Length" not in headers:
      headers["Content-Length"] = str(len(body))

    if "Connection" not in headers:
      headers["Connection"] = "close"

    for key, value in headers.items():
      responseHeaderLines.append(f"{key}: {value}")

    responseParts = ["\r\n".join(responseHeaderLines).encode(), body]
    return b"\r\n\r\n".join(responseParts)

  def parseRequest(self, request: bytes):
    lines = request.split(b"\r\n")
    method, full_path, version = lines.pop(0).decode().split(" ")

    path_parts = full_path.split("?")
    path = path_parts.pop(0)
    query = path_parts.pop(0) if len(path_parts) else None

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
      "full_path": full_path,
      "path": path,
      "query": query,
      "version": version,
      "headers": headers,
      "body": body,
    }


class AdvancedHTTPFactory(protocol.Factory):
  def buildProtocol(self, addr):
    return AdvancedHTTPServer(addr.host)

reactor.listenTCP(1234, AdvancedHTTPFactory())
reactor.run()
