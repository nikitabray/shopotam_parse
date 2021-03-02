from bs4 import BeautifulSoup
from parse import ToTheParse
import requests
import json


def get_categories(connection):
    url = 'https://shopotam.com/rubrics'
    doc = connection.get(url).text
    soup = BeautifulSoup(doc, 'html.parser')
    soup = soup.find('ul', 'categories')
    result = {}  #First lvl deep
    x = 1
    for first_category in soup.find_all('li', 'category'):
        first_category_title = first_category.find(
            'h2', 'h5 title').getText().strip()
        result[first_category_title] = []
        for each in first_category.find_all('li', 'item'):
            second_category = each.find('a', href=True)
            second_category_title = second_category.getText()
            second_category_link = 'https://shopotam.com' + second_category[
                'href']
            result[first_category_title].append(
                {second_category_title: {
                    'Link': second_category_link
                }})  #Second level deep
            x += 1
    return result


def get_subcategories(categories_dict,
                      connection,
                      zero_category='',
                      ind='',
                      ind2=''):
    result = {}  #First level deep
    for first_category, second_category_list in categories_dict.items():
        ind3 = '0'
        result[first_category] = []
        result_2 = {}  #Second level deep
        for second_category in second_category_list:
            ind3 = str(int(ind3) + 1)
            second_category_title, second_category_link = list(
                second_category.keys())[0], list(
                    second_category.values())[0]['Link']
            result_2[second_category_title] = []
            doc = connection.get(second_category_link).text
            soup = BeautifulSoup(doc, 'html.parser')
            active_rubric = soup.find('li', 'catalog-rubrics-item active')
            if active_rubric is None:
                result_2[second_category_title].append(
                    {second_category_title: {
                        'Link': second_category_link
                    }})
                continue
            rubrics = active_rubric.find_all('li', 'catalog-rubrics-item')
            x = 1
            for third_level_category in rubrics:
                third = third_level_category.find('a', href=True)
                third_title = third.getText().strip()
                print(zero_category + '/' + first_category + '/' +
                      second_category_title + '/' + third_title + '/' + ind +
                      '/' + ind2 + '/' + ind3)
                third_link = 'https://shopotam.com' + third['href']
                result_2[second_category_title].append(
                    {third_title: {
                        'Link': third_link
                    }})
                x += 1
        result[first_category].append(result_2)
    return result


def get_sub_subcategories_lol(third_result, connection):
    result = {}
    result_3 = {}
    first_ind = 0
    for first_category_title, second_category_list in third_result.items():
        first_ind += 1
        second_ind = 0
        result[first_category_title] = []
        result_2 = {}
        for second_category_title, third_category_list in second_category_list[
                0].items():
            second_ind += 1
            result_2[second_category_title] = []
            result_3 = get_subcategories(
                {second_category_title: third_category_list}, connection,
                first_category_title, str(first_ind), str(second_ind))
            result_2[second_category_title] = result_3[second_category_title]
        result[first_category_title] = result_2
    return result


connection = ToTheParse.get_connection()

try:
    with open('results/categories.json', 'r') as of:
        result = json.load(of)
except FileNotFoundError:
    result = get_categories(connection)
    with open('results/categories.json', 'w') as of:
        json.dump(result, of)

try:
    with open('results/subcategories.json', 'r') as of:
        subresult = json.load(of)
except FileNotFoundError:
    with open('results/categories.json', 'r') as of:
        result = json.load(of)
    subresult = get_subcategories(result, connection)
    with open('results/subcategories.json', 'w') as of:
        json.dump(subresult, of)

try:
    with open('results/sub_subcategories.json', 'r') as of:
        sub_subresult = json.load(of)
except FileNotFoundError:
    with open('results/subcategories.json', 'r') as of:
        subresult = json.load(of)
    sub_subresult = get_sub_subcategories_lol(subresult, connection)
    with open('results/sub_subcategories.json', 'w') as of:
        json.dump(sub_subresult, of)
