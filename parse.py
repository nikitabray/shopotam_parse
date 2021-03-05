from bs4 import BeautifulSoup
import requests
import json


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

    def get_document(self, url):
        from parse_categories import ConnectionManager
        session = ConnectionManager.get_connection()
        resp = session.get(url)
        doc = resp.text
        return resp.status_code, doc

    def get_url_for_page(self, url, val):
        a = f'{url}/page{val}'
        print(a)
        return a

    def check_if_page_exists(self, resp_code):
        if resp_code == 404:
            return False
        else:
            return True

    def get_pattern(self, tp='non-technic'):
        patterns = {
            'non-technic': {
                'block': ['li', 'product'],
                'maker': ['div', 'product-card-title'],
                'title': ['div', 'product-card-title-sub'],
                'price': ['div', 'product-card-price'],
                'price_on_sale': ['div', 'product-card-profit'],
            },
            'technic': {
                'block': ['li', 'product'],
                'maker': ['div', 'product-card-features-title'],
                'title': ['div', 'product-card-title'],
                'price': ['div', 'product-card-price'],
                'price_on_sale': ['div', 'product-card-profit'],
            }
        }
        return patterns[tp]

    def get_product_categoty_type(self, soup):
        if soup.find(*self.get_pattern('technic')['maker']):
            return 'technic'
        else:
            return 'non-technic'

    def search_by_patterns(self, soup, tp):
        patterns = self.get_pattern(tp)
        product_maker = soup.find(*patterns['maker']).getText()
        product_title = soup.find(*patterns['title']).getText()
        product_link = 'https://shopotam.com' + \
            soup.find('a', href=True)['href']
        product_price = soup.find(*patterns['price']).getText()
        product_price_on_sale = soup.find(*patterns['price_on_sale'])
        if product_price_on_sale:
            product_price_on_sale = product_price_on_sale.getText()
        return [
            product_maker,
            product_title,
            product_link,
            product_price,
            product_price_on_sale
        ]

    def pack_it(self, *args):
        maker, title, link, price, sale_price = args
        res = {}
        if sale_price:
            res[maker] = [
                {
                    '': title,
                    '': price,
                    '': sale_price,
                    '': link,
                }
            ]
        else:
            res[maker] = [
                {
                    '': title,
                    '': price,
                    '': link,
                }
            ]
        return res

    def get_product_info(self, url, session, *args):
        a, b, c, d = args
        result = {}
        page = 1
        while True and page < 120:
            urlnew = self.get_url_for_page(url, page)
            resp_code, doc = self.get_document(urlnew)
            if not self.check_if_page_exists(resp_code):
                break
            soup = BeautifulSoup(doc, self.parser)
            for each in soup.find_all(*self.get_pattern()['block']):
                tp = self.get_product_categoty_type(each)
                print(tp)
                maker, title, link, price, sale_price = self.search_by_patterns(
                    each, tp)
                packed_data = self.pack_it(
                    maker, title, link, price, sale_price)
                print(f'Нашли в {a}/{b}/{c}/{d}/{page} {title}')
                if maker in result:
                    result[maker].append(packed_data)
                else:
                    result[maker] = packed_data[maker]
            page += 1
        sorted_result = {}
        for i in sorted(result):
            sorted_result[i] = result[i]
        return sorted_result

