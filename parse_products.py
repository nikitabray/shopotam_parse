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


# def get_result_file():
#     with open('results/sub_subcategories.json', 'r') as f:
#         result = json.load(f)
#     return result


# def get_all_products():
#     connection = ToTheParse.get_connection()
#     result = get_result_file()
#     final_result = {}

#     ind1 = 0
#     for first_category_title, second_category_list in result.items():
#         ind1 += 1
#         ind2 = 0
#         final_result[first_category_title] = []
#         second_result = {}
#         for second_category_title, third_category_list in second_category_list.items():
#             ind2 += 1
#             ind3 = 0
#             second_result[second_category_title] = []
#             third_result = {}
#             for third_category_title, fourth_category_list in third_category_list[0].items():
#                 ind3 += 1
#                 ind4 = 0
#                 third_result[third_category_title] = []
#                 product_result = {}
#                 for fourth_category_title, category_link in fourth_category_list[0].items():
#                     ind4 += 1
#                     helpdict = {
#                         'first_category_title': first_category_title,
#                         'second_category_title': second_category_title,
#                         'third_category_title': third_category_title,
#                         'fourth_category_title': fourth_category_title,
#                         'ind1': ind1,
#                         'ind2': ind2,
#                         'ind3': ind3,
#                         'ind4': ind4,
#                     }
#                     product_result[fourth_category_title] = []
#                     category_link = category_link['Link']
#                     parse = ToTheParse(url=category_link)
#                     product_result[fourth_category_title].append(parse.get_product_info(session=connection, helpdict=helpdict))
#                 third_result[third_category_title].append(product_result)
#             second_result[second_category_title].append(third_result)
#         final_result[first_category_title].append(second_result)
#         return
#     return final_result




# with open('results/final.json', 'w') as f:
#     json.dump(get_all_products())



