#! /usr/bin/env python3
# coding: utf-8


"""
Script requesting Open Food Facts API to obtains a few JSON data.
The aim is to show this approach takes to much time to get entire database.

5th project of OC Python Developer Path.

Author: Loïc Mangin
"""


import json
import requests
import time


def products_total_nb():
    """Return the number of products referenced in the Open Food Facts
    french database, based on data in 'categories.json' file.
    """
    with open('categories.json', 'r') as f:
        categories = json.load(f)
    products_count = 0
    for category in categories['tags']:
        products_count += category['products']
    return products_count


def format_duration(duration):
    """Return the duration in the format '{HH} h {MM} min {SS.S} s'.
    """
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = round(duration % 60, 1)
    return "{0} h {1} min {2} s".format(hours, minutes, seconds)


def format_int(n):
    """Return the integer n in a '3-digits' format, with n < 1 000 000.
    """
    return str(n // 1000) + " " + str(n % 1000).zfill(3)


def get_categories():
    """Get all french categories, with some details, in a JSON file
    from the Open Food Facts database.
    """
    url = 'https://fr.openfoodfacts.org/categories.json'
    data = requests.get(url).json()
    with open('categories.json', 'w') as f:
        f.write(json.dumps(data, indent=4))


def get_products(max_requests):
    """Do a limited number of requests, each one getting Open Food Facts
     data for 20 products (or less) in JSON format.
     """
    with open('categories.json', 'r') as f:
        categories = json.load(f)
    requests_count = 0
    with open('products.json', 'w') as f:
        for category in categories['tags']:
            products_nb = category['products']
            url = category['url']
            for i in range(1, products_nb // 20 + 1):
                if requests_count < max_requests:
                    request_url = url + "/" + str(i) + ".json"
                    print(request_url)
                    data = requests.get(request_url).json()
                    #print(data)
                    f.write(json.dumps(data, indent=4))
                    requests_count += 1
    print()
    print("Nombre de requêtes effectuées : " + str(requests_count))


def main():
    get_categories()
    # --- DO A LIMITED NUMBER OF REQUESTS ---
    requests_nb = 5  # Fixed umber of requests to OFF API
    t_start = time.clock()
    get_products(requests_nb)
    t_end = time.clock()
    # --- ESTIMATE DURATION FOR REQUESTING ENTIRE DATABASE ---
    duration = t_end - t_start
    print("Durée des requêtes effectuées : " + format_duration(duration))
    print()
    prod_total = products_total_nb()
    print("Nombre total de produits dans la base : " + format_int(prod_total))
    req_total = prod_total // 20
    print("Estimation (basse) du nombre de requêtes "
          "nécessaires : " + format_int(req_total))
    total_duration = duration * (req_total / requests_nb)
    print("Estimation (basse) de la durée de récupération "
          "de la base complète : " + format_duration(total_duration))


if __name__ == "__main__":
    main()
