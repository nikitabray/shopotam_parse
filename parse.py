from bs4 import BeautifulSoup
import requests
import json
import time


class GetUrl():
    def __init__(self, *args, **kwargs):
        self.url = input("Введите url категории: ")

    def get_url(self):
        if self.url:
            return self.url
        else:
            return 'https://shopotam.com/odezhda-i-obuv/zhenshchinam/bele-i-kupalniki/kupalniki'


class ToTheParse():
    def __init__(self,
                 url=None,
                 pages=None,
                 parser='html.parser',
                 *args,
                 **kwargs):
        self.parser = parser
        self.url = url

    @staticmethod
    def get_connection():
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent':
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        session = requests.Session()
        session.headers.update(headers)
        return session

    def get_document(self, url, session):
        resp = session.get(url)
        doc = resp.text
        return resp.status_code, doc

    def get_url_for_page(self, val):
        return f'{self.url}/page{val}'

    def get_product_info(self, session, helpdict):
        result = {}
        page = 1
        while True:
            url = self.get_url_for_page(page)
            resp_code, doc = self.get_document(url, session)
            if resp_code == 404:
                break
            soup = BeautifulSoup(doc, self.parser)
            for each in soup.find_all('div', 'product-card'):
                product_maker = each.find('div',
                                          'product-card-title').getText()
                product_title = each.find('div',
                                          'product-card-title-sub').getText()
                product_link = 'https://shopotam.com' + \
                    each.find('a', href=True)['href']
                product_price = each.find('div',
                                          'product-card-price').getText()
                product_sale_price = each.find('div', 'product-card-profit')
                print(
                    f'{helpdict["first_category_title"]}/{helpdict["second_category_title"]}/{helpdict["third_category_title"]}/{helpdict["fourth_category_title"]}/{helpdict["ind1"]}/{helpdict["ind2"]}/{helpdict["ind3"]}/{helpdict["ind4"]}/{page=}/{product_title}'
                )
                if not product_sale_price:
                    if product_maker in result:
                        result[product_maker].append({
                            'Наименование товара': product_title,
                            'Цена товара': product_price,
                            'Ссылка': product_link,
                        })
                    else:
                        result[product_maker] = [{
                            'Наименование товара': product_title,
                            'Цена товара': product_price,
                            'Ссылка': product_link,
                        }]
                else:
                    if product_maker in result:
                        result[product_maker].append({
                            'Наименование товара':
                            product_title,
                            'Цена товара без скидки':
                            product_price,
                            'Цена товара со скидкой':
                            product_sale_price.getText(),
                            'Ссылка':
                            product_link,
                        })
                    else:
                        result[product_maker] = [{
                            'Наименование товара':
                            product_title,
                            'Цена товара без скидки':
                            product_price,
                            'Цена товара со скидкой':
                            product_sale_price.getText(),
                            'Ссылка':
                            product_link,
                        }]
            page += 1
        sorted_result = {}
        for i in sorted(result):
            sorted_result[i] = result[i]
        return sorted_result


if __name__ == "__main__":
    url_class = GetUrl()
    avito = ToTheParse(url_class.get_url())
    a = avito.get_product_info()
    filename = input(
        'Введите название для файла (без расширения), куда программа сохранит данные: '
    )
    if not filename:
        filename = 'result'
    with open(filename + '.json', 'w') as outfile:
        json.dump(a, outfile)
