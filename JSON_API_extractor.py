#! /usr/bin/env python3
# coding: utf-8


"""
Builder of the database used by the Pur Beurre application.
5th project of OC Python Developer Path.

Use Open Food Facts API to obtains JSON datas.

Author: Loïc Mangin
"""


import json
import requests
import time

def estimate_total_duration(max_requests, duration):
    with open('categories.json', 'r') as f:
        categories = json.load(f)
    products_nb = 0
    for i in range(categories['count']):
        products_nb += categories['tags'][i]['products']
    estimated_requests_nb = products_nb // 20
    estimated_total_duration = round((estimated_requests_nb / max_requests) * duration, 1)
    print("Nb of products: " + str(products_nb))
    print("Nb of requests: " + str(estimated_requests_nb))
    print("Total duration of JSON extraction: " + str(estimated_total_duration / 3600) + " h")

def get_categories():
    url = 'https://fr.openfoodfacts.org/categories.json'
    datas = requests.get(url).json()
    with open('categories.json', 'w') as f:
        f.write(json.dumps(datas, indent=4))

def get_product_from_categories(min_products, max_requests):
    with open('categories.json', 'r') as f:
        categories = json.load(f)

    requests_nb = 0

    with open('products.json', 'w') as f:
        pass

    for i in range(3):
        products_nb = categories['tags'][i]['products']
        url = categories['tags'][i]['url']
        if products_nb >= min_products:
            for j in range(1, products_nb // 20):
                if requests_nb >= max_requests:
                    break
                request_url = url + "/" + str(j) + ".json"
                print(request_url)
                datas = requests.get(request_url).json()
                requests_nb += 1

                with open('products.json', 'a') as f:
                    f.write(json.dumps(datas, indent=4))

    print("Nb of requests: " + str(requests_nb))

def get_product_with_barcode(url):
    datas = requests.get(url).json()
    with open('granola.json', 'w') as f:
        f.write(json.dumps(datas, indent=4))

def get_product_with_name(name):
    datas = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?\
                         search_terms=' + name + \
                         '&search_simple=1&action=process&json=1').json()
    with open(name + '.json', 'w') as f:
        f.write(json.dumps(datas, indent=4))

def display_product_with_name(name):
    with open(name + '.json', 'r') as f:
        products = json.load(f)
    for product in products['products']:
        print(product['product_name_fr'], end=' ')
        print('[code : ' + product['code'] + ']', end=' >>> ')
        print(product['generic_name'])
        print(product['brands'])
        print('>>> Nutriscore : ' + product['nutrition_grades'].upper())
        print('>>> ' + product['stores'])
        print('>>> ' + product['url'])
        print()

def select_main_categories():
    with open('categories.json') as f:
        categories = json.load(f)
    min_products = 2000
    i = 0
    while categories['tags'][i]['products'] >= min_products:
        print(categories['tags'][i]['name'])
        i += 1
    print(i - 1)


def main():
    #get_categories()
    min_products = 2000
    max_requests = 100

    start_time = time.time()
    get_product_from_categories(min_products, max_requests)
    end_time = time.time()
    duration = round(end_time - start_time, 1)
    print(str(duration) + " s")

    estimate_total_duration(max_requests, duration)


"""
import json
import urllib.request

# https://world.openfoodfacts.org/product/3029330003458
def main():
    for i in range(2, 5):
        url = "https://fr.openfoodfacts.org/categorie/boissons/" + str(i) + ".json"
        data = json.load(urllib.request.urlopen(url))
        print('DATA >>> ' + str(data))
        try:
            product = data['products'][0]
            print('Code : ' + product['code'])
            print('Nom : ' + product['product_name_fr'].upper())
            print('>>>> Marque : ' + product['brands'].capitalize())
            print('>> Catégories : ' + ', '.join(product['categories'].split(',')))
            print('>>>> NutriScore : ' + product['nutrition_grade_fr'].upper())
            print('>>>> Scanné à ' + product['stores'].capitalize() + ' - ' + product['purchase_places'])
            print("Plus d'info sur" + url[:-5])
            print()

        except:
            pass
"""

if __name__ == "__main__":
    main()
