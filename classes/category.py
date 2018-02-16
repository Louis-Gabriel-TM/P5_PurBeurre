#! /usr/bin/env python3
# coding: utf-8


"""
The 'Category' class used by the 'Pur Beurre' application.

5th project of OC Python Developer Path.

Author: Loïc Mangin
"""


class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def display(self):
        print("  " + str(self.id) + ". " + self.name)


def main():
    pass


if __name__ == "__main__":
    main()
