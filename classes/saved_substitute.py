#! /usr/bin/env python3
# coding: utf-8


"""
The 'Saved_substitute' class used by the 'Pur Beurre' application.

5th project of OC Python Developer Path.

Author: Loïc Mangin
"""

from classes.product import *


class SavedSubstitute:
    """Saved_substitute used by 'Pur Beurre' application.
    Data come from application use and 'Pur Beurre' database.
    """
    def __init__(self, id_sub, id_product, id_substitute, backup_date):
        """More details about Saved_substitute attributes
        on the data_model.JPG file.
        """
        self.id = id_sub
        self.id_product = id_product
        self.id_substitute = id_substitute
        self.backup_date = backup_date

    def display(self, socket):
        """Display the formatted date of the research
        and details on the chosen product and the suggested substitute.
        """
        print("-" * 50)
        product = get_product(socket, self.id_product)
        substitute = get_product(socket, self.id_substitute)
        print()
        print(">>>> Recherche enregistrée le "
              + str(self.backup_date) + " <<<<")
        print(">> Produit choisi :". upper())
        product.display()
        print(">> Substitut proposé :".upper())
        substitute.display()


def get_product(socket, id_prod):
    """Get attributes of the chosen product and the suggested substitute
    from the 'Pur Beurre' database.
    """
    with socket.cursor() as cursor:
        cursor.execute("""  SELECT * FROM Product
                                WHERE id = {0}; """.format(id_prod))
        prod = cursor.fetchone()
    product = Product(prod[0], prod[1], prod[2], prod[3], prod[4], prod[5], prod[6], prod[7])
    return product


def main():
    pass


if __name__ == "__main__":
    main()
