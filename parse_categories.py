from bs4 import BeautifulSoup
from parse import ToTheParse
import requests
import json


class UrlManager():
    @staticmethod
    def paginate_url(url):
        return


class ConnectionManager():
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


class BeautifulSoupManager():
    @staticmethod
    def beautify(doc, parser='html.parser'):
        return BeautifulSoup(doc, parser)


class DocumentManager():
    @staticmethod
    def get_document(connection, url):
        return connection.get(url).text


class FileManager():

    @staticmethod
    def dump_to_file(data, level_of_category):
        with open(f'results/{level_of_category}.json', 'w') as f:
            json.dump(data, f)

    @staticmethod
    def load_file(self, level_of_category):
        with open(f'results/{level_of_category}.json', 'r') as f:
            data = json.load(f)
        return data

    @staticmethod
    def check_if_file_exists(filename):
        try:
            with open(f'result/{filename}', 'r') as f:
                return True
        except FileNotFoundError:
            return False


class PatternManager():
    patterns = {
        'first_level': {'parent': ['li', 'category'],
                        'child': ['h2', 'h5 title']},
        'second_level': {'parent': ['li', 'catalog-rubrics-item active'],
                         'child': ['li', 'catalog-rubrics-item']},
        'third_level': {'parent': ['li', 'catalog-rubrics-item active'],
                        'child': ['li', 'catalog-rubrics-item']},
        'fourth_level': {'parent': ['li', 'catalog-rubrics-item active'],
                         'child': ['li', 'catalog-rubrics-item']},
    }

    @classmethod
    def get_patterns(cls):
        return cls.patterns


class ParseManager():
    def __init__(self, connection, patterns):
        self.connection = connection
        self.patterns = patterns

    def get_categories(self, soup, category, parent='/'):
        data = {}
        #Check if page has no subcategories
        check = self.check_for_double_active_category(soup)
        if check:
            data[check['title']] = check['url']
            return data
        for primary_category in soup.find_all(*self.patterns[category]['parent']):
            for subcategory in primary_category.find_all(
                    *self.patterns[category]['child']):
                category_title = subcategory.getText().strip()
                category_url = 'https://shopotam.com' + \
                    subcategory.find('a', href=True)['href']
                data[category_title] = category_url
                print(parent + '/' + category_title)
        return data

    @staticmethod
    def check_for_double_active_category(soup):
        try:
            category = soup.find('li', 'catalog-rubrics-item active').find(
                'li', 'catalog-rubrics-item active')
            title = category.getText().strip()
            url = 'https://shopotam.com' + \
                category.find('a', href=True)['href']
            return {'title': title, 'url': url}
        except AttributeError:
            return False

    def cycle(self, data, level):
        temp_data = {}
        for category_title in data:
            category_url = data[category_title]
            if type(category_url) == dict:
                temp_data[category_title] = self.cycle(category_url, level)
                continue
            connection = ConnectionManager.get_connection()
            doc = DocumentManager.get_document(connection, category_url)
            soup = BeautifulSoupManager.beautify(doc)
            temp_data[category_title] = self.get_categories(
                soup, level, category_title)
        return temp_data

    def organize_data(self, start_point_soup):
        data = self.get_categories(start_point_soup, 'first_level')
        FileManager.dump_to_file(data, 'first')
        data_second = self.cycle(data, 'second_level')
        FileManager.dump_to_file(data_second, 'second')
        data_third = self.cycle(data_second, 'third_level')
        FileManager.dump_to_file(data_third, 'third')
        data_fourth = self.cycle(data_third, 'fourth_level')
        FileManager.dump_to_file(data_fourth, 'fourth')
        for item in data_third:
            data_third[item] = data_fourth[item]
        for item in data_second:
            data_second[item] = data_third[item]
        for item in data:
            data[item] = data_second[item]



patterns = PatternManager.get_patterns()
conn = ConnectionManager.get_connection()
doc = DocumentManager.get_document(conn, 'https://shopotam.com/rubrics')
doc = DocumentManager.get_document(
    conn, 'https://shopotam.com/rubrics')
soup = BeautifulSoupManager.beautify(doc)
print(ParseManager(soup, patterns).organize_data(soup))

