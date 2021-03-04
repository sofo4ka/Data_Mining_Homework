import re
import pymongo
import scrapy


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['http://auto.youla.ru/']

    _css_selectors = {
        "brands": ".TransportMainFilters_brandsList__2tIkv "
                  ".ColumnItemList_container__5gTrc "
                  "a.blackLink",
        "pagination": "a.Paginator_button__u1e7D",
        "car": ".SerpSnippet_titleWrapper__38bZM a.SerpSnippet_name__3F7Yu",
    }

    def _get_follow(self, response, select_str, callback, **kwargs):
        for a in response.css(select_str):
            link = a.attrib.get("href")
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(response,
                                    self._css_selectors["brands"],
                                    self.brand_parse,
                                    hello="moto")

    def brand_parse(self, response, **kwargs):
        yield from self._get_follow(response,
                                    self._css_selectors["pagination"],
                                    self.brand_parse,
                                    )
        yield from self._get_follow(response,
                                    self._css_selectors["car"],
                                    self.car_parse
                                    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = pymongo.MongoClient()

    @staticmethod
    def get_author_id(resp):
        marker = "window.transitState = decodeURIComponent"
        for script in resp.css("script"):
            try:
                if marker in script.css("::text").extract_first():
                    re_pattern = re.compile(r"youlaId%22%2C%22([a-zA-Z|\d]+)%22%2C%22avatar")
                    result = re.findall(re_pattern, script.css("::text").extract_first())
                    return resp.urljoin(f"/user/{result[0]}") if result else None
            except TypeError:
                pass

    @staticmethod
    def get_characteristics(response):
        characteristics_list = []
        for element in response.css("div.AdvertCard_specs__2FEHc .AdvertSpecs_row__ljPcX"):
            line_info = {
                "name": element.css(".AdvertSpecs_label__2JHnS::text").extract_first(),
                "value": element.css(".AdvertSpecs_data__xK2Qx::text").extract_first(),
            }
            characteristics_list.append(line_info)
        return characteristics_list

    def car_parse(self, response):
        """
            # Собрать след стуркутру и сохранить в БД Монго
            # Название объявления+
            # Список фото объявления (ссылки)+
            # Список характеристик
            # Описание объявления
            # ссылка на автора объявления
            # дополнительно попробуйте вытащить телефона
        """
        items = {
            "title": response.css("div.AdvertCard_advertTitle__1S1Ak::text").extract_first().strip(),
            "picture": [img.attrib.get("src") for img in response.css("figure.PhotoGallery_photo__36e_r img")],
            "characteristics": AutoyoulaSpider.get_characteristics(response),
            "author": AutoyoulaSpider.get_author_id(response),
            "price": int(("").join(response.css("div.AdvertCard_price__3dDCr::text").get().split("\u2009"))),
        }
        data = {}
        for key, css_selector in items.items():
            try:
                data[key] = css_selector(response)
            except Exception as err:
                #print(Exception, err)
                continue
        self.db_client["gb_parse"][self.name].insert_one(data)
        c = 1
