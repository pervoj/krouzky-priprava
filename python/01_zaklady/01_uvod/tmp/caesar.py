vstup = input("Zadejte text: ")
posun = int(input("Zadejte číselný posun: "))

operace = input("Zadejte operaci (šifrování [1], desifrování [2]): ")
if operace == "2":
    posun = -posun

vystup = ""

for znak in vstup:
    vystup += chr(ord(znak) + posun)

print(f"Výsledek: '{vystup}'")