# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

guap = [{"url": "http://portal.guap.ru/portal/priem/priem2020/lists/11_144_BO.html",
         "name": '09.04.01 "Информатика и вычислительная техника" Институт аэрокосмических приборов и систем.',
         "places": 'мест 20, 4 из них целевая квота',
         "last_date": "9 августа"},
        {"url": "http://portal.guap.ru/portal/priem/priem2020/lists/11_173_BO.html",
         "name": '09.04.03 "Прикладная информатика" Институт технологий предпринимательства.',
         "places": 'мест 18, 4 из них целевая квота',
         "last_date": "9 августа"},
        {"url": "http://portal.guap.ru/portal/priem/priem2020/lists/11_163_BO.html",
         "name": '09.04.04 "Программная инженерия" Институт вычислительных систем и программирования.',
         "places": 'мест 15, 3 из них целевая квота',
         "last_date": "9 августа"}]

makarov = [{"name": "09.04.02 Информационные системы и технологии (Проектирование и разработка информационных систем)",
            "table_id": 1,
            "places": 'мест 15, 0 из них целевая квота',
            "last_date": "18 августа"},
           {
               "name": "10.04.01 Информационная безопасность (Технологии построения защищённых информационных систем на транспорте)",
               "table_id": 0,
               "places": 'мест 10, 0 из них целевая квота',
               "last_date": "18 августа"}]


def parse_guap(url: str):
    """
    Метод для парсинга данных от ГУАП
    :param url: адрес таблицы со списком
    :return: Вернет данные по убыванию баллов по столбцу "Сумма конкурсных баллов"
    """
    res = requests.get(url=url)
    soup = BeautifulSoup(res.content.decode('utf-8'), 'html.parser')
    table = soup.tbody
    users_dict = dict()
    for i in table:
        user = i.findAll("td")
        position = 0
        info = ""
        name_key_dict = ""
        for j in user:
            if position < 2 or position > 6:
                info += j.contents[0] + " "
            if position == 7:
                name_key_dict = j.contents[0]
            position += 1

        users_dict[info] = int(name_key_dict)

    list_values = sorted(users_dict.items(), key=lambda x: x[1], reverse=True)
    k = 1
    for i in list_values:
        s = i[0].split()
        if s[5] == 'Да':
            print(k, s[0], s[1], s[2], s[3], s[4], s[5].upper())
            k += 1
    for i in list_values:
        s = i[0].split()
        if s[5] == 'Нет':
            print(k, s[0], s[1], s[2], s[3], s[4], s[5].lower())
            k += 1


def parse_makarov(table_number: int):
    """
    Метод для парсинга данных от Макарова.
    :param table_number: Номер таблицы отслеживания
    :return: выведет таблицу с данными
    """
    res = requests.get(url="https://gumrf.ru/reserve/abitur/hod/?type=211")
    soup = BeautifulSoup(res.content.decode('utf-8'), 'html.parser')
    details_tag = soup.find_all("details")
    table_tag = (details_tag[table_number].findAll("table"))[-1].findAll("td")
    info = ""
    position = 0
    print("№\tФИО\tСумма баллов\tСогласие на зачисление\tСогласие на другом направлении")
    for i in table_tag[1:]:
        if position < 3 or position == 7 or position == 8:
            info += str(i.contents[0]) + " "
        elif position == 9:
            info += str(i.contents[0]) + "\n"
            position = 0
            continue
        position += 1

    print(info)


def get_info_guap():
    for row in guap:
        print(row.get("name"))
        print(row.get("places"))
        print("Дата окончания подачи документов " + row.get("last_date"))
        print("----------------------------------------------------------")
        parse_guap(row.get("url"))
        print("----------------------------------------------------------")


def get_info_makarov():
    for row in makarov:
        print(row.get("name"))
        print(row.get("places"))
        print("Дата окончания подачи документов " + row.get("last_date"))
        print("----------------------------------------------------------")
        parse_makarov(row.get("table_id"))
        print("----------------------------------------------------------")


get_info_guap()
get_info_makarov()

