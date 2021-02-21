from pathlib import Path
from les1 import Parse5ka


class Categories_Parse5ka(Parse5ka):

    def __init__(self, categories_url, *args, **kwargs):
        self.categories_url = categories_url
        super().__init__(*args, **kwargs)

    def _parse(self, url: str):
        while url:
            response = self._get_response(url)
            data = response.json()
            return data

    def _get_products(self, parent_group_code):
        products_url = f"{self.start_url}?categories={parent_group_code}"
        while products_url:
            response = self._get_response(products_url)
            data = response.json()
            products_url = data['next']
            for product in data["results"]:
                yield product

    def run(self):
        categories_list = self._parse(self.categories_url)
        for element in categories_list:
            file_name = f"{element['parent_group_code']}.json"
            element["products"] = []
            products_info = self._get_products(element['parent_group_code'])
            element["products"].extend(products_info)
            categories_file_path = self.save_path.joinpath(file_name)
            self._save(element, categories_file_path)


if __name__ == "__main__":
    url = "https://5ka.ru/api/v2/special_offers/"
    categories_url = "https://5ka.ru/api/v2/categories/"
    save_path = Path(__file__).parent.joinpath('categories')
    if not save_path.exists():
        save_path.mkdir()
    categories_parser = Categories_Parse5ka(categories_url, url, save_path)
    categories_parser.run()
