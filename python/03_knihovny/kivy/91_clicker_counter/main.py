from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class ClickCounter(BoxLayout):
  def __init__(self):
    super().__init__(orientation = "vertical")

    self.count = 0

    self.label = Label(text = "Počet kliknutí: 0", font_size = 32)
    self.add_widget(self.label)

    button = Button(text = "Klikni!", font_size = 32, size_hint_y = None)
    button.bind(on_press=self.increment)
    self.add_widget(button)

  def increment(self, instance):
    self.count += 1
    self.label.text = f"Počet kliknutí: {self.count}"

class ClickCounterApp(App):
  def build(self):
    return ClickCounter()

ClickCounterApp().run()