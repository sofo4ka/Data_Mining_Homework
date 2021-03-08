import scrapy
from ..items import HhparseItem


class HhparseSpider(scrapy.Spider):
    name = 'hhparse'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    def parse(self, response, *args, **kwargs):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').get()
        yield response.follow(next_page, callback=self.parse)
        vacancies_list = response.css('div.vacancy-serp '
                                      'div.vacancy-serp-item '
                                      'div.vacancy-serp-item__row_header '
                                      'a.bloko-link::attr(href)'
                                      ).extract()
        for link in vacancies_list:
            yield response.follow(link, callback=self.vacancy_parse)

    # author_info_xpaths = {
    #     "employer_name": "//span//text",
    #     "employer_website": '//a[@class="g-user-content"]/@href',
    #     "employer_areas": '//div[@class="bloko-text-emphasis"]//text()',
    #     "employer_description": '//div[@class="company-description"]//text()',
    # }

    def vacancy_parse(self, response, *args, **kwargs):
        vacancy_title = response.xpath('//h1[@class="bloko-header-1"]/text()').extract_first()
        salary = ''.join(response.css('span.bloko-header-2::text').extract())
        # ''.join(response.xpath('//p/span[@class="bloko-header-2 bloko-header-2_lite"]/text()').extract())
        description = response.xpath("//div[@class='vacancy-section']//text()").extract()
        key_skills = response.xpath("//span[@class='bloko-tag__section bloko-tag__section_text']/text()").extract()
        author = response.xpath("//a[@class='vacancy-company-name']/@href").get()
        author_page = f'{"https://hh.ru/"}{author}'

        yield HhparseItem(vacancy_title=vacancy_title,
                          salary=salary,
                          description=description,
                          key_skills=key_skills,
                          author=author,
                          )


