# https://www.dpp.cz/jizdne/cenik-jizdneho

vek = int(input("Zadej svůj věk: "))

if vek < 15:
  print("Kategorie: Dítě")
  print("Cena: 0 Kč")
elif vek < 26:
  print("Kategorie: Student")
  print("Cena: 30 Kč")
elif vek < 60:
  print("Kategorie: Dospělý")
  print("Cena: 30 Kč")
else:
  print("Kategorie: Senior")
  print("Cena: 15 Kč")