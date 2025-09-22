from os.path import join, dirname, exists
import json

stock_file = join(dirname(__file__), "stock.json")

def set_stock(stock):
  file = open(stock_file, "w")
  json.dump(stock, file)
  file.close()


def get_stock():
  if not exists(stock_file):
    set_stock([])
    return []
  
  file = open(stock_file, "r")
  stock = json.load(file)
  file.close()
  return stock


def get_product_by_id(id):
  stock = get_stock()
  for product in stock:
    if product["id"] == id:
      return product
  else:
    return None
 

def remove_product(id):
  stock = get_stock()
  for product in stock:
    if product["id"] == id:
      stock.remove(product)
      break
  set_stock(stock)


def update_product(id, data):
  stock = get_stock()
  for product in stock:
    if product["id"] == id:
      for key, value in data.items():
        product[key] = value
      break
  set_stock(stock)


def add_to_stock(id, name, quantity_unit, price_per_unit, quantity):
  product = {
    "id": id,
    "name": name,
    "quantity_unit": quantity_unit,
    "price_per_unit": price_per_unit,
    "quantity": quantity,
  }
  
  if get_product_by_id(id) != None:
    update_product(id, product)
    return
  
  stock = get_stock()
  stock.append(product)
  set_stock(stock)


def set_product_quantity(id, quantity):
  update_product(id, {"quantity": quantity})


def set_product_price(id, price):
  update_product(id, {"price_per_unit": price})


def get_new_id():
  stock = get_stock()
  
  if len(stock) == 0:
    return 1
  
  return max([product["id"] for product in stock]) + 1