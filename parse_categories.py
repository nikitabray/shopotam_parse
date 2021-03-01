from bs4 import BeautifulSoup
from parse import ToTheParse
import requests
import json


def get_categories(connection):
    url = 'https://shopotam.com/rubrics'
    doc = connection.get(url).text
    soup = BeautifulSoup(doc, 'html.parser')
    soup = soup.find('ul', 'categories')
    result = {}
    x = 1
    for each in soup.find_all('li', 'item'):
        category = each.find('a', href=True)
        category_title = category.getText() + f'[{str(x)}]'
        category_link = 'https://shopotam.com' + category['href']
        result[category_title] = {'Link': category_link}
        x += 1
    return result


def get_subcategories(categories_dict, connection):
    subcategory_obj = {}
    for category, link in categories_dict.items():
        category_link = link['Link']
        doc = connection.get(category_link).text
        soup = BeautifulSoup(doc, 'html.parser')
        active_rubric = soup.find('li', 'catalog-rubrics-item active')
        subcategory_obj[category] = []
        if active_rubric is None:
            subcategory_obj[category].append(
                {category: {
                    'Link': category_link
                }})
            continue
        rubrics = active_rubric.find_all('li', 'catalog-rubrics-item')

        x = 1
        for rub in rubrics:
            subcategory = rub.find('a', href=True)
            subcategory_title = subcategory.getText().strip() + f'[{str(x)}]'
            subcategory_link = 'https://shopotam.com' + subcategory['href']
            subcategory_obj[category].append(
                {subcategory_title: {
                    'Link': subcategory_link
                }})
            x += 1
        # print("-" * 40)
        # print(subcategory_obj)
    return subcategory_obj


def get_sub_subcategories_lol(result, connection):
    sub_subcategory_obj = {}
    for subcategory, sub_subcategories in result.items():
        sub_subcategory_obj[subcategory] = []
        for sub_subcategory in sub_subcategories:
            title = list(sub_subcategory.keys())[0]
            link = list(sub_subcategory.values())[0]
            res = get_subcategories({title: link}, connection)
            sub_subcategory_obj[subcategory].append(res)
        print(sub_subcategory_obj)
    return sub_subcategory_obj


connection = ToTheParse.get_connection()
# result = get_categories(connection)
# subresult = get_subcategories(result, connection)
with open('subcategories.json', 'r') as incomefile:
    subresult = json.load(incomefile)
sub_subresult = get_sub_subcategories_lol(subresult, connection)

with open('sub_subcategories.json', 'w') as outfile:
    json.dump(sub_subresult, outfile)

# with open('subcategories.json', 'w') as outfile:
#     json.dump(subresult, outfile)
