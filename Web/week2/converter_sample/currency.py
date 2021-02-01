from bs4 import BeautifulSoup
from decimal import Decimal


def get_course(body: object, charcode: str) -> tuple:
    course = Decimal(body.find("charcode", text=charcode).find_next_sibling("value"). \
                     string.replace(",", "."))
    nominal = Decimal(body.find("charcode", text=charcode).find_next_sibling("nominal"). \
                      string.replace(",", "."))
    return course, nominal


def convert(amount, cur_from, cur_to, date, requests):
    amount = Decimal(amount)
    param = {"date_req": date}
    response = requests.get("http://www.cbr.ru/scripts/XML_daily.asp",
                            params=param)
    body = BeautifulSoup(response.text, "lxml")
    if cur_from == "RUR" and cur_to == "RUR":
        result = amount
    elif cur_from == "RUR":
        course, nominal = get_course(body, charcode=cur_to)
        result = (amount / (course / nominal))
    elif cur_to == "RUR":
        course, nominal = get_course(body, charcode=cur_from)
        result = course / nominal * amount
    else:
        to_course, to_nominal = get_course(body, charcode=cur_to)
        from_course, from_nominal = get_course(body, charcode=cur_from)
        # количество рублей
        amount_ru_to = from_course / from_nominal * amount
        result = amount_ru_to / (to_course / to_nominal)
    return result.quantize(Decimal("1.0000"))
