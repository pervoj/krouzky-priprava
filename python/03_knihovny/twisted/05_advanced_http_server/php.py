# https://www6.uniovi.es/~antonio/ncsa_httpd/cgi/env.html

import subprocess
import os

def run_php(resource_dir: str, file_path: str, request: dict, server_address: str, server_name: str):
  env = os.environ.copy()

  env["PHP_SELF"] = os.path.relpath(file_path, resource_dir)
  env["GATEWAY_INTERFACE"] = "CGI/1.1"
  env["SERVER_ADDR"] = server_address
  env["SERVER_NAME"] = server_name
  env["SERVER_PROTOCOL"] = request["version"]
  env["REQUEST_METHOD"] = request["method"]
  env["DOCUMENT_ROOT"] = resource_dir
  env["SCRIPT_FILENAME"] = file_path
  env["SCRIPT_NAME"] = file_path
  env["REQUEST_URI"] = request["full_path"]
  env["REDIRECT_STATUS"] = "1"

  if request["query"]:
    env["QUERY_STRING"] = request["query"]

  if "Content-Length" in request["headers"]:
    env["CONTENT_LENGTH"] = request["headers"]["Content-Length"]

  if "Content-Type" in request["headers"]:
    env["CONTENT_TYPE"] = request["headers"]["Content-Type"]

  for key, value in request["headers"].items():
    env[f"HTTP_{key.upper().replace('-', '_')}"] = value

  process = subprocess.Popen(
    ["php-cgi"],
    env = env,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
    stdin = subprocess.PIPE,
  )

  output, error = process.communicate(
    input = request["body"]
  )

  if error:
    raise Exception(error.decode())

  lines = output.split(b"\r\n")

  headers = {}
  while True:
    if not lines: break
    line = lines.pop(0)
    if not line: break
    key, value = line.decode().split(": ")
    headers[key] = value

  status_str = headers.pop("Status", None)
  status = None
  if status_str: status = int(status_str.split(" ")[0])

  body = b"\r\n".join(lines)

  return status, headers, body
