from stock import get_product_by_id

cart = []


def add_to_cart(product_id, quantity = 1):
  product = get_product_by_id(product_id)
  
  if product == None:
    return False
  
  for item in cart:
    if item["product"] == product_id:
      item["quantity"] += quantity
      return True

  cart.append({
    "product": product_id,
    "quantity": quantity
  })
  return True


def remove_from_cart(product_id, quantity = 1):
  for item in cart:
    if item["product"] == product_id:
      if quantity > item["quantity"]:
        raise Exception("Quantity to remove is greater than quantity in cart")

      item["quantity"] -= quantity
      if item["quantity"] <= 0:
        cart.remove(item)
      return True
  return False


def get_cart_total_price():
  total = 0
  for item in cart:
    product = get_product_by_id(item["product"])
    total += product["price_per_unit"] * item["quantity"]
  return total
