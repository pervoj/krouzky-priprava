from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField, widgets

app = Flask(__name__)
app.config["SECRET_KEY"] = "tajný klíč" # CSRF



class Formular(FlaskForm):
  prvni_cislo = FloatField(
    "První číslo",
    widget = widgets.NumberInput()
  )

  druhe_cislo = FloatField(
    "Druhé číslo",
    widget = widgets.NumberInput()
  )

  operator = SelectField(
    "Operátor",
    choices = ["+", "-", "*", "/"]
  )

  submit = SubmitField("Vypočítat")



@app.route("/", methods = ["GET", "POST"])
def home():
  form = Formular()

  if not form.validate_on_submit():
    return render_template(
      "kalkulacka.html",
      form = form,
    )

  prvni = form.prvni_cislo.data
  druhe = form.druhe_cislo.data
  operator = form.operator.data

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

  return render_template(
    "kalkulacka.html",
    form = form,
    vysledek = vysledek,
  )

if __name__ == "__main__":
  app.run(debug = True)
