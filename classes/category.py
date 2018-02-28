#! /usr/bin/env python3
# coding: utf-8


"""
The 'Category' class used by the 'Pur Beurre' application.

5th project of OC Python Developer Path.

Author: Loïc Mangin
"""


class Category:
    """Category class used by 'Pur Beurre' application.
    Data come from Open Food Facts french database.
    """
    def __init__(self, id_cat, name):
        """More details about Category attributes
        on the data_model.JPG file.
        """
        self.id = id_cat
        self.name = name

    def display(self):
        """Display id and name of the instance
        to appear in a listing.
        """
        print("  " + str(self.id) + ". " + self.name)


def main():
    pass


if __name__ == "__main__":
    main()
