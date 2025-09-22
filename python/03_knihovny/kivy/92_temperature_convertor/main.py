from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class PrevodnikTeplot(BoxLayout):
  def __init__(self):
    super().__init__(
      orientation = "vertical",
      spacing = 10,
      padding = 10,
    )

    self.input = TextInput(
      hint_text = "Zadej teplotu v °C",
      multiline = False,
      size_hint_y=None,
    )
    self.add_widget(self.input)

    button = Button(
      text = "Převést",
      size_hint_y = None,
    )
    button.bind(on_press = self.prevest)
    self.add_widget(button)

    self.vysledek = Label(
      text = "",
      size_hint_y = None,
    )
    self.add_widget(self.vysledek)

  def prevest(self, instance):
    try:
      celsius = float(self.input.text)
      fahrenheit = celsius * 9 / 5 + 32
      self.vysledek.text = f"{celsius} °C = {fahrenheit:.2f} °F"
    except ValueError:
      self.vysledek.text = "Zadej platné číslo!"

class PrevodnikTeplotApp(App):
  def build(self):
    return PrevodnikTeplot()

PrevodnikTeplotApp().run()