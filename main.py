import os
import dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
# from gb_parse.spiders.autoyoula import AutoyoulaSpider
# from gb_parse.spiders.hhparse import HhparseSpider
from gb_parse.spiders.instagram import InstagramSpider

if __name__ == "__main__":
    dotenv.load_dotenv(".env")
    crawler_settings = Settings()
    tags = ["python"]
    # crawler_proc.crawl(HhparseSpider)
    # crawler_proc.crawl(AutoyoulaSpider)
    crawler_settings.setmodule("gb_parse.settings")
    crawler_proc = CrawlerProcess(settings=crawler_settings)
    crawler_proc.crawl(
        InstagramSpider,
        login=os.getenv("INST_LOGIN"),
        password=os.getenv("INST_PASSWORD"),
        tags=tags,
    )
    crawler_proc.start()