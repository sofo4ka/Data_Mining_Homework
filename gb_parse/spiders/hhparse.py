import scrapy


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

    def vacancy_parse(self, response, *args, **kwargs):
        # потом переписать через HhparseLoader
        vacancy_title = response.css('h1.bloko-header-1::text').extract_first()
        salary = ''.join(response.css('span.bloko-header-2::text').extract())


        print(vacancy_title, salary)
        yield HhparseItem(vacancy_title=vacancy_title, salary=salary)
