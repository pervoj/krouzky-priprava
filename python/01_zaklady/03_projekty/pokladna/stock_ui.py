import ui
import stock


def stock_loop():
  ui.clear()
  print("CASHDESK: stock")
  print("^^^^^^^^")
  
  while True:
    print()
    print()
    
    print("Use one of the commands to proceed:")
    print("  p - print products table")
    print("  a - add new product")
    print("  q - quit to main menu")
    print()
    
    command = input("Enter command: ").strip().lower()
    
    print()
    print()
    
    if command == "q":
      break
    elif command == "p":
      print("Products table")
    elif command == "a":
      new_product()
    else:
      print("Unknown command")


def print_products_table():
  stock_list = stock.get_stock()
  
  print("ID  | Name                           | Price (CZK) | Quantity | Unit")
  print("----+--------------------------------+-------------+----------+-----")
  
  for product in stock_list:
    id = str(product["id"]).rjust(3)
    name = product["name"].ljust(30)
    unit = product["quantity_unit"].rjust(11)
    price = f"{product["price_per_unit"]:.2f}".rjust(8)
    quantity = str(product["quantity"]).ljust(4)
    
    print(f"{id} | {name} | {price} | {quantity} | {unit}")


def new_product():
  id = stock.get_new_id()
  
  print("Please answer the following questions about the new product:")
  name = input("  Name: ").strip()
  unit = input("  Quantity unit: ").strip()
  price = float(input("  Price: ").strip())
  quantity = float(input("  Current quantity in stock: ").strip())
  
  stock.add_to_stock(id, name, unit, price, quantity)
