abeceda = [
    ["a", ".-"],
    ["b", "-..."],
    ["c", "-.-."],
    ["d", "-.."],
    ["e", "."],
    ["f", "..-."],
    ["g", "--."],
    ["h", "...."],
    ["i", ".."],
    ["j", ".---"],
    ["k", "-.-"],
    ["l", ".-.."],
    ["m", "--"],
    ["n", "-."],
    ["o", "---"],
    ["p", ".--."],
    ["q", "--.-"],
    ["r", ".-."],
    ["s", "..."],
    ["t", "-"],
    ["u", "..-"],
    ["v", "...-"],
    ["w", ".--"],
    ["x", "-..-"],
    ["y", "-.--"],
    ["z", "--.."],
    ["1", ".----"],
    ["2", "..---"],
    ["3", "...--"],
    ["4", "....-"],
    ["5", "....."],
    ["6", "-...."],
    ["7", "--..."],
    ["8", "---.."],
    ["9", "----."],
    ["0", "-----"]
]

vstup = input("Zadejte text: ").strip().lower()
operace = input("Zadejte operaci (šifrování [1], desifrování [2]): ")
if operace == "2": vstup = vstup.strip("/").split("/")

vystup = []

for znak in vstup:
    for pismeno, kod in abeceda:
        if operace == "2":
            if znak == kod:
                vystup.append(pismeno)
                break
        else:
            if znak == pismeno:
                vystup.append(kod)
                break
    else:
        vystup.append(" ")

if operace == "2":
    print("".join(vystup))
else:
    print("/" + "/".join(vystup) + "/")
