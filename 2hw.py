# Источник https://magnit.ru/promo/?geo=moskva
# Необходимо собрать структуры товаров по акции и сохранить их в MongoDB
#
# пример структуры и типы обязательно хранить поля даты как объекты datetime
# {
#     "url": str,
#     "promo_name": str,
#     "product_name": str,
#     "old_price": float,
#     "new_price": float,
#     "image_url": str,
#     "date_from": "DATETIME",
#     "date_to": "DATETIME",
# }

from pathlib import Path
from urllib.parse import urljoin
import requests
import bs4
import pymongo
import datetime as dt


class MagnitParse:
    def __init__(self, start_url, db_client):
        self.start_url = start_url
        self.db = db_client["gb_data_mining"]
        self.collection = self.db["magnit_products"]

    def _get_response(self, url):
        while True:
            response = requests.get(url)
            if response.status_code == 200:
                return response

    def _get_soup(self, url):
        response = self._get_response(url)
        return bs4.BeautifulSoup(response.text, "lxml")

    def run(self):
        soup = self._get_soup(self.start_url)
        catalog = soup.find("div", attrs={"class": "сatalogue__main"})
        for prod_a in catalog.find_all("a", recursive=False):
            product_data = self._parse(prod_a)
            self._save(product_data)

    def get_template(self):
        return {
            "url": lambda a: urljoin(self.start_url, a.attrs.get("href", "")),
            "promo_name": lambda a: a.find("div",
                                           attrs={"class": "card-sale__name"}
                                           ).text,
            "product_name": lambda a: a.find("div",
                                             attrs={"class": "card-sale__title"}
                                             ).text,
            "old_price": lambda a: float(".".join(a.find("div",
                                                         attrs={"class": "label__price_old"}
                                                         ).text.split())),
            "new_price": lambda a: float(".".join(a.find("div",
                                                         attrs={"class": "label__price_new"}
                                                         ).text.split())),
            "image_url": lambda a: urljoin(self.start_url, a.find("img").attrs.get("data-src")),
            "date_from": lambda a: self.__get_date(
                a.find("div", attrs={"class": "card-sale__date"}).text, True
            ),
            "date_to": lambda a: self.__get_date(
                a.find("div", attrs={"class": "card-sale__date"}).text, False
            ),
        }

    def __get_date(self, date: str, date_from) -> list:

        MONTHS = {
            "янв": 1,
            "фев": 2,
            "мар": 3,
            "апр": 4,
            "май": 5,
            "мая": 5,
            "июн": 6,
            "июл": 7,
            "авг": 8,
            "сен": 9,
            "окт": 10,
            "ноя": 11,
            "дек": 12,
        }
        dates = date.split(" ")
        try:
            if date_from:
                return dt.datetime(
                    day=int(dates[1]),
                    month=MONTHS[dates[2][:3]],
                    year=dt.datetime.now().year)
            else:
                return dt.datetime(
                    day=int(dates[3]),
                    month=MONTHS[dates[4][:3]],
                    year=dt.datetime.now().year)
        except Exception as err:
            pass

    def _parse(self, product_a) -> dict:
        data = {}
        for key, funk in self.get_template().items():
            try:
                data[key] = funk(product_a)
            except Exception as err:
                pass
        return data

    def _save(self, data: dict):
        self.collection.insert_one(data)


def get_save_path(dir_name):
    dir_path = Path(__file__).parent.joinpath(dir_name)
    if not dir_path.exists():
        dir_path.mkdir()
    return dir_path


if __name__ == "__main__":
    url = "https://magnit.ru/promo/?geo=moskva"
    save_path = get_save_path("magnit_product")
    db_client = pymongo.MongoClient("mongodb://localhost:27017")
    parser = MagnitParse(url, db_client)
    parser.run()
