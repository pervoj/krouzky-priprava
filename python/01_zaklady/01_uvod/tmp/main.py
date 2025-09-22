def slovne(znamka):
    if znamka < 1.5:
        return "Výborně"
    elif znamka < 2.5:
        return "Chvalitebně"
    elif znamka < 3.5:
        return "Dobře"
    elif znamka < 4.5:
        return "Dostatečně"
    else:
        return "Nedostatečně"

znamky = []

while True:
    vstup = input("Zadejte známku: ").strip().replace(",", ".")
    if not vstup: break
    try:
        znamka = float(vstup)

        if znamka < 1 or znamka > 5:
            print("Zadejte platnou známku!")
            continue
        
        if not znamka.is_integer() and (znamka * 10) % 5 != 0:
            print("Zadejte platnou známku!")
            continue

        znamky.append(znamka)
    except ValueError:
        print("Zadejte platné číslo!")

prumer = sum(znamky) / len(znamky)
print("Průměr:", prumer)
print("Známka:", round(prumer), slovne(prumer))
