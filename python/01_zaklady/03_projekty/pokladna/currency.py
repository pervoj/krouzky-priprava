import requests


def __get_course():
  api_url = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt"
  res = requests.get(api_url)
  
  lines = res.text.splitlines()[2:]
  currencies = {}
  
  for line in lines:
    parts = line.strip().split("|")
    currencies[parts[3]] = float(parts[4].replace(",", "."))
  
  return currencies


def convert_from_czk(currency: str, in_czk: float) -> float:
  currencies = __get_course()
  return in_czk / currencies[currency]


def convert_to_czk(currency: str, in_currency: float) -> float:
  currencies = __get_course()
  return in_currency * currencies[currency]
