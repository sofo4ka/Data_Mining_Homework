# Необходимо обойти все записи в блоге и извлечь из них информацию следующих полей:
#
# url страницы материала +
# Заголовок материала+
# Первое изображение материала (Ссылка) +
# (найти как преобразовать <img alt="" src=" ...)+
# Дата публикации+   !!!!!( выведено в обычном виде,
# переделать в datetime)
# имя автора материала+
# ссылка на страницу автора материала+
# комментарии в виде (автор комментария и текст комментария)+
# список тегов+
# реализовать SQL структуру хранения данных c следующими таблицами
#
# Post+
# Comment
# Writer+
# Tag+
# Организовать реляционные связи между таблицами
#
# При сборе данных учесть, что полученый из данных автор уже может быть в БД и значит необходимо это заблаговременно проверить.
# Не забываем закрывать сессию по завершению работы с ней


import requests
import bs4
from urllib.parse import urljoin
from lesson3.db import Database


"""
FIFO - first input first output
FILO - first input last output
"""


class GbBlogParse:
    def __init__(self, start_url, database: Database):
        self.db = database
        self.start_url = start_url
        self.done_urls = set()
        self.tasks = [
            self.get_task(self.start_url, self.parse_feed),
        ]
        self.done_urls.add(self.start_url)

    def get_task(self, url, callback):
        def task():
            soup = self._get_soup(url)
            return callback(url, soup)

        return task

    def _get_response(self, url):
        response = requests.get(url)
        return response

    def _get_soup(self, url):
        soup = bs4.BeautifulSoup(self._get_response(url).text, "lxml")
        return soup

    def parse_post(self, url, soup):
        author_tag = soup.find("div", attrs={"itemprop": "author"})
        data = {
            "post_data": {
                "title": soup.find("h1", attrs={"class": "blogpost-title"}).text,
                "url": url,
                "image_url": soup.find('div', attrs={'class': 'hidden', 'itemprop': "image"}).text,
                "date_publ": soup.find("time", attrs={"itemprop": "datePublished"}).text,
                "id": soup.find("comments").attrs.get("commentable-id"),
            },
            "author_data": {
                "url": urljoin(url, author_tag.parent.attrs.get("href")),
                "name": author_tag.text,
            },
            "tags_data": [
                {"name": tag.text, "url": urljoin(url, tag.attrs.get("href"))}
                for tag in soup.find_all("a", attrs={"class": "small"})
            ],
            "comments_data": self._get_comments(soup.find("comments").attrs.get("commentable-id")),
        }
        return data

    def _get_comments(self, post_id):
        api_path = f"/api/v2/comments?commentable_type=Post&commentable_id={post_id}&order=desc"
        response = self._get_response(urljoin(self.start_url, api_path))
        data = response.json()
        print(data)
        return data

    def parse_feed(self, url, soup):
        ul = soup.find("ul", attrs={"class": "gb__pagination"})
        pag_urls = set(
            urljoin(url, href.attrs.get("href"))
            for href in ul.find_all("a")
            if href.attrs.get("href")
        )
        for pag_url in pag_urls:
            if pag_url not in self.done_urls:
                self.tasks.append(self.get_task(pag_url, self.parse_feed))

        post_items = soup.find("div", attrs={"class": "post-items-wrapper"})
        posts_urls = set(
            urljoin(url, href.attrs.get("href"))
            for href in post_items.find_all("a", attrs={"class": "post-item__title"})
            if href.attrs.get("href")
        )

        for post_url in posts_urls:
            if post_url not in self.done_urls:
                self.tasks.append(self.get_task(post_url, self.parse_post))

    def run(self):
        for task in self.tasks:
            task_result = task()
            if task_result:
                self.save(task_result)

    def save(self, data):
        self.db.create_post(data)


if __name__ == "__main__":
    database = Database("sqlite:///gb_blog.db")
    parser = GbBlogParse("https://geekbrains.ru/posts", database)
    parser.run()
