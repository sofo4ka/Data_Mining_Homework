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
        print(1)


    def car_parse(self, response):
        print(1)
        # data = { }
        # for key, selector in self.data_query.items():
        #     try:
        #         data[key] = selector(response)
        #     except (ValueError, AttributeError):
        #         continue
        # self.db_client["gb_parse_15_02_2021"][self.name].insert_one(data)
        #
