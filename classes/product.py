#! /usr/bin/env python3
# coding: utf-8


"""
The Product class used by the Pur Beurre application.
5th project of OC Python Developer Path.

Author: Loïc Mangin
"""


class Product:
    def __init__(self, name, brand, nutriscore, store, url, id_category):
        self.name = name
        self.brand = brand
        self.nutriscore = nutriscore
        self.store = store
        self.link = url
        self.category = id_category

    def display(self):
        print("Nom : " + self.name)
        print("Marque : " + self.brand)
        print(">> Nutriscore : " + self.nutriscore.upper())
        print(">> Magansin : " + self.store)
        print("Plus d'information sur " + self.link)


def main():
    pass


if __name__ == "__main__":
    main()
