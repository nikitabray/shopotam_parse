from bs4 import BeautifulSoup
import requests
import json
from parse import ToTheParse
from parse_categories import *


class IBegYou():

    #Parse through one page of category
    def ok_fine(self, link, *args):
        data = args
        a = ToTheParse()
        return a.get_product_info(link, ConnectionManager.get_connection(), *data)

    #Loop this sht to death.
    #Don't look at this if you're sensitive
    def do_it_again_please(self, data):
        ok_daddy = {}
        for a in data:
            b, c, d = '', '', ''
            print(f'Ищем в /{a}')
            ok_daddy[a] = {}
            for b in data[a]:
                print(f'Ищем в /{a}/{b}')
                ok_daddy[a][b] = {}
                if type(data[a][b]) is dict:
                    for c in data[a][b]:
                        print(f'Ищем в /{a}/{b}/{c}')
                        ok_daddy[a][b][c] = {}
                        if type(data[a][b][c]) is dict:
                            for d in data[a][b][c]:
                                print(f'Ищем в /{a}/{b}/{c}/{d}')
                                ok_daddy[a][b][c][d] = {}
                                link = data[a][b][c][d]
                                ok_daddy[a][b][c][d] = self.ok_fine(link, a, b, c, d)
                        else: #Third level
                            link = data[a][b][c]
                            ok_daddy[a][b][c] = self.ok_fine(link, a, b, c, d)
                            continue
                else: #Second level
                    link = data[a][b]
                    ok_daddy[a][b] = self.ok_fine(link, a, b, c, d)
                    continue
        return ok_daddy

with open('results/fourth.json', 'r') as f:
    d = json.load(f)

a = IBegYou()
b = a.do_it_again_please(d)
FileManager.dump_to_file(b, 'salam')

