import scrapy
import json
from ..loaders import InstagramTagLoader


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com']
    start_urls = ['http://www.instagram.com/']
    _login_url = "https://www.instagram.com/accounts/login/ajax/"
    _tags_path = "/explore/tags/"

    def __init__(self, login, password, tags, *args, **kwargs):
        self.login = login
        self.password = password
        self.tags = tags
        super().__init__(*args, **kwargs)

    def parse(self, response):
        try:
            js_data = self.js_data_extract(response)
            yield scrapy.FormRequest(
                self._login_url,
                method="POST",
                callback=self.parse,
                formdata={"username": self.login, "enc_password": self.password,},
                headers={"X-CSRFToken": js_data["config"]["csrf_token"]},
            )
        except AttributeError as e:
            print(e)
            for tag_name in self.tags:
                yield response.follow(
                    f"{self._tags_path}{tag_name}/", callback=self.tag_page_parse
                )

    def get_tag_data(self, tag_data: dict):
        return tag_data.get('entry_data').get('TagPage')[0].get('graphql').get('hashtag')

    def tag_page_parse(self, response):
        loader = InstagramTagLoader(response=response)
        loader.add_value("url", response.url)
        tag_data = self.get_tag_data(self.js_data_extract(response))
        tag_characteristics = tag_data.keys()
        for key in tag_characteristics:
            loader.add_value(key, tag_data[key])
        yield loader.load_item()
        print(1)

    def js_data_extract(self, response):
        script = response.xpath(
            "//script[contains(text(), 'window._sharedData =')]/text()"
        ).extract_first()
        return json.loads(script.replace("window._sharedData = ", "")[:-1])