def inputInt(vstup):
    while True:
        try:
            return int(input(vstup))
        except ValueError:
            print("Zadejte platné číslo")

cislo = inputInt("Zadejte číslo: ")

soucet = 0
while cislo > 0:
    soucet += cislo % 10
    cislo //= 10

# soucet = 0
# for cifra in str(cislo):
#     soucet += int(cifra)

print(f"Ciferný součet: {soucet}")