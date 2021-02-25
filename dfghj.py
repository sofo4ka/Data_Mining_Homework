# def __get_date(self, date: str, date_from) -> list:
#     MONTHS = {
#         "янв": 1,
#         "фев": 2,
#         "мар": 3,
#         "апр": 4,
#         "май": 5,
#         "мая": 5,
#         "июн": 6,
#         "июл": 7,
#         "авг": 8,
#         "сен": 9,
#         "окт": 10,
#         "ноя": 11,
#         "дек": 12,
#     }
#     dates = date.split(" ")
#     try:
#         if date_from:
#             day = int(dates[1]),
#             month = MONTHS[dates[2][:3]]
#         else:
#             day = int(dates[3]),
#             month = MONTHS[dates[4][:3]]
#     except Exception as err:
#         # print(Exception, err)
#         pass
#     finally:
#         year = dt.datetime.now().year
#         return dt.datetime(day=day, month=month, year=year)

print(len('            "url": lambda a: urljoin(self.start_url, a.attrs.get("href", "")),'))