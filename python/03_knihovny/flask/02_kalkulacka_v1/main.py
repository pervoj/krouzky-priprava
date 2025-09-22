from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def home():
  operators = ["+", "-", "*", "/"]

  prvni = request.args.get("prvni_cislo")
  druhe = request.args.get("druhe_cislo")
  operator = request.args.get("operator")

  if prvni is None or druhe is None or operator is None:
    return render_template(
      "kalkulacka.html",
      vysledek = "Vyplň formulář",
      prvni_cislo = prvni,
      druhe_cislo = druhe,
      operators = operators,
      selected_operator = operator,
    )

  try:
    prvni = float(prvni)
    druhe = float(druhe)
  except ValueError:
    return render_template(
      "kalkulacka.html",
      vysledek = "Neplatné číslo",
      prvni_cislo = prvni,
      druhe_cislo = druhe,
      operators = operators,
      selected_operator = operator,
    )

  if operator == "+":
    vysledek = prvni + druhe
  elif operator == "-":
    vysledek = prvni - druhe
  elif operator == "*":
    vysledek = prvni * druhe
  elif operator == "/":
    if druhe == 0:
      vysledek = "Nelze dělit nulou"
    else:
      vysledek = prvni / druhe
  else:
    vysledek = "Neznámý operátor"

  return render_template(
    "kalkulacka.html",
    vysledek = vysledek,
    prvni_cislo = prvni,
    druhe_cislo = druhe,
    operators = operators,
    selected_operator = operator,
  )

if __name__ == "__main__":
  app.run(debug = True)
