#! /usr/bin/env python3
# coding: utf-8


"""
The 'Product' class used by the 'Pur Beurre' application.

5th project of OC Python Developer Path.

Author: Loïc Mangin
"""


class Product:
    def __init__(self, id, id_category, name, subcategory, brands,
                 score_100g, nutriscore, url):
        self.id = id
        self.id_category = id_category
        self.name = name
        self.subcategory = subcategory
        self.brands = brands
        self.score_100g = score_100g
        self.nutriscore = nutriscore
        self.url =url

    def display(self):
        print("Nom          : " + self.name.upper())
        print("Marque       : " + self.brands)
        print("Description  : " + self.subcategory)
        print("Nutriscore   : " + self.nutriscore)
        print("Plus d'infos : " + self.url)
        print()


def main():
    pass


if __name__ == "__main__":
    main()
