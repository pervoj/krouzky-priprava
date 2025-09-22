from flask import Flask, request, jsonify
from os.path import join, dirname, isfile
import json

data_file = join(dirname(__file__), "data.json")

app = Flask(__name__)


def load_data():
  if not isfile(data_file):
    return []

  f = open(data_file, "r")
  data = json.load(f)
  return data


@app.route("/products")
def get_products():
  return jsonify(load_data())


@app.route("/products", methods = ["POST"])
def create_product():
  data = load_data()
  data.append(request.json)

  f = open(data_file, "w")
  json.dump(data, f)
  f.close()

  return jsonify({ "message": "Product created" }), 201


if __name__ == "__main__":
  app.run(debug = True)

# curl "http://localhost:5000/products" -X "POST" -H "Content-Type: application/json" -d '{ "id": 4, "name": "Product 4", "price": 400 }'