prvni = float(input("Zadej první číslo: "))
druhe = float(input("Zadej druhé číslo: "))
operace = input("Zadej operaci: ")

if operace == "+":
  print(f"Součet: {prvni + druhe}")
elif operace == "-":
  print(f"Rozdíl: {prvni - druhe}")
elif operace == "*":
  print(f"Součin: {prvni * druhe}")
elif operace == "/":
  if druhe == 0:
    print("Nelze dělit nulou")
  else:
    print(f"Podíl: {prvni / druhe}")
else:
  print("Neplatná operace")