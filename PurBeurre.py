#! /usr/bin/env python3
# coding: utf-8


"""
Pur Beurre, an application to find a healthier food.

5th project of OC Python Developer Path.

Author: Loïc Mangin
"""


from classes.category import *
from classes.saved_substitute import *  # also import classes.product
from PB_constants import *

import pymysql
from random import randint


"""
------------------
DATABASE FUNCTIONS
------------------
"""


def db_connect():
    """Return an access to the 'Pur Beurre' database
    previously created with CSV_database_builder.py.
    """
    socket = pymysql.connect(host='localhost',
                             user='remy',
                             passwd='ratatouille',
                             db='PurBeurre_db',
                             charset='utf8')
    return socket


def db_disconnect(socket):
    """Push the modifications in the 'Pur Beurre' database
    and close access to it.
    """
    socket.commit()
    socket.close()


def get_categories(socket):
    """Get categories from 'Pur Beurre' datbase.
    Return a list of Category instances.
    """
    cat_list = []
    with socket.cursor() as cursor:
        cursor.execute("""  SELECT * FROM Category; """)
        cat_tuples = cursor.fetchall()
    for cat in cat_tuples:
        category = Category(cat[0], cat[1])
        cat_list.append(category)
    return cat_list


def get_excerpt(socket, cat_id, nutriscore, length):
    """Get some products from 'Pur Beurre' database
    randomly selected and with a 'bad' nutriscore.
    Return a list of Product instances.
    """
    prod_list = []
    with socket.cursor() as cursor:
        cursor.execute("""  SELECT * FROM Product
                                WHERE id_category = {0}
                                AND nutriscore >= '{1}'; """
                       .format(cat_id, nutriscore))
        prod_tuples = cursor.fetchall()
    index = random_index(length, prod_tuples)
    prod_tuples = [prod_tuples[i] for i in index]
    prod_tuples.sort(key=lambda tup: tup[2])
    for prod in prod_tuples:
        product = Product(prod[0], prod[1], prod[2], prod[3],
                          prod[4], prod[5], prod[6], prod[7])
        prod_list.append(product)
    return prod_list


def get_saved_substitutes(socket, nb):
    """Get last saved researches (product and substitute)
    from 'Pur Beurre' database.
    Return a list of Saved_substitute instances.
    """
    saved_list = []
    with socket.cursor() as cursor:
        cursor.execute("""  SET lc_time_names = 'fr_FR'; """)
        cursor.execute("""  SELECT id, id_product, id_substitute, 
                                    DATE_FORMAT(backup_date, '%W %e %M %Y') 
                                FROM Saved_substitute
                                ORDER BY backup_date DESC
                                LIMIT {0}; """.format(nb))
        saved_tuples = cursor.fetchall()
    for saved_sub in saved_tuples:
        saved_substitute = SavedSubstitute(saved_sub[0], saved_sub[1],
                                            saved_sub[2], saved_sub[3])
        saved_list.append(saved_substitute)
    return saved_list


def get_substitutes(socket, product, length):
    """Get some randomly selected possible substitutes (better nutriscore).
    Return a list of Product instances.
    """
    sub_list = []
    with socket.cursor() as cursor:
        cursor.execute("""  SELECT * FROM Product
                                WHERE subcategory = '{0}' 
                                AND nutriscore < '{1}'; """
                       .format(product.subcategory, product.nutriscore))
        sub_tuples = cursor.fetchall()
    index = random_index(length, sub_tuples)
    sub_tuples = [sub_tuples[i] for i in index]
    sub_tuples.sort(key=lambda tup: tup[2])
    for sub in sub_tuples:
        substitute = Product(sub[0], sub[1], sub[2], sub[3],
                             sub[4], sub[5], sub[6], sub[7])
        sub_list.append(substitute)
    return sub_list


def random_index(length, tup):
    """Return a list of randomly selected index of a tuple.
    """
    index = []
    while len(index) != min(length, len(tup)):
        i = randint(0, len(tup) - 1)
        if i not in index:
            index.append(i)
    return index


def save_substitute(socket, product, substitute):
    """Save a research (product and substitute)
    in the 'Pur Beurre' database.
    """
    with socket.cursor() as cursor:
        cursor.execute("""  INSERT INTO Saved_substitute (id_product, 
                                                          id_substitute,
                                                          backup_date)
                                VALUES ({0}, {1}, CURRENT_DATE()); """
                       .format(product.id, substitute.id))
    print("Produit et substitut sauvegardés.")
    socket.commit()


"""
-------------------
INTERFACE FUNCTIONS
-------------------
"""


def ask_for_home():
    """Return True if user wants to return to home page.
    """
    print("\n" + "-" * 50 + "\n")
    option = choose_option("Souhaitez-vous revenir à la page d'accueil ?",
                           option_1="Retourner à l'accueil",
                           option_2="Quitter")
    if option == 1:
        return True
    else:
        return False


def choose_option(text, option_1, option_2):
    """Propose an alternative amongst 2 choices.
    Test answer validity and return choice.
    """
    print(text)
    print("  1. " + option_1)
    print("  2. " + option_2)
    choice = input("Option choisie : ")
    print()
    if choice not in ["1", "2"]:
        print("Cette option n'est pas disponible.")
        print()
        choice = choose_option(text, option_1, option_2)
    return int(choice)


def choose_line(listing, text, alt):
    """Propose to choose an option in a listing.
    Test answer validity and return choice.
    """
    choice = input(text)
    print()
    if not (1 <= int(choice) <= len(listing)):
        print(alt)
        print()
        choice = choose_line(listing, text, alt)
    return int(choice)


def choose_product(excerpt):
    """Return the integer representing the chosen product
    in the excerpt.
    """
    choice = input("Produit choisi : ")
    print()
    if not (1 <= int(choice) <= len(excerpt)):
        print("Ce produit n'est pas proposé.")
        print()
        choice = choose_product(excerpt)
    return int(choice)


def display_categories(categories):
    """Display the list of categories
    using the 'display' method of Category class.
    """
    for category in categories:
        category.display()


def display_excerpt(prod_list, head):
    """Display a list of 'Product.name' instances
    (with 'nutriscore' and 'score_100g' to debug).
    """
    print("--- " + head.upper() + " ---")
    i = 0
    for product in prod_list:
        i += 1
        print("  " + str(i) + "." + " " * (2 - (i // 10)) + product.name
              + " (" + product.nutriscore + ", "
              + str(product.score_100g) + ")"
              )


def display_head():
    """Display program header with brand and headline.
    """
    head_length = max(len(PB_BRAND), len(PB_HEADLINE))
    print()
    print("#" * (head_length + 8))
    print("#   " + PB_BRAND.upper().center(head_length) + "   #")
    print("#   " + PB_HEADLINE.center(head_length) + "   #")
    print("#" * (head_length + 8))
    print()


"""
-------------
MAIN FUNCTION
-------------
"""


def main():
    db = db_connect()
    go_home = True
    while go_home:
        # --- HOME PAGE ---
        display_head()
        option = choose_option(text=HOME_ASK,
                               option_1=HOME_1_TEXT,
                               option_2=HOME_2_TEXT)
        if option == 1:
            # --- OPTION 1: Find a substitute ---
            # 1.1. Chose category
            categories = get_categories(db)
            print("--- CATEGORIES DISPONIBLES ---")
            display_categories(categories)
            chosen_cat = choose_line(categories,
                                     text=CATEGORY_ASK,
                                     alt=CATEGORY_ALT)
            # 1.2. Choose product
            excerpt = get_excerpt(db, chosen_cat, 'C', 10)
            display_excerpt(excerpt, PRODUCT_HEAD)
            chosen_prod = choose_line(excerpt,
                                      text=PRODUCT_ASK,
                                      alt=PRODUCT_ALT)
            # 1.3. Show substitutes
            results = get_substitutes(db, excerpt[chosen_prod - 1], 5)
            if not results:
                print(NO_RESULT)
            else:
                display_excerpt(results, SUBSTITUTE_HEAD)
                # 1.4. Show more informations on a product
                chosen_substitute = choose_line(results,
                                                text=SUBSTITUTE_ASK,
                                                alt=SUBSTITUTE_ALT)
                results[chosen_substitute - 1].display()
                option = choose_option(text=SAVE_ASK,
                                       option_1=SAVE_1_TEXT,
                                       option_2=SAVE_2_TEXT)
                if option == 1:
                    # 1.5a. Save substitute
                    product = excerpt[chosen_prod - 1]
                    substitute = results[chosen_substitute - 1]
                    save_substitute(db, product, substitute)
        else:
            # --- OPTION 2: View saved substitues
            # 2.1. Show saved substitutes
            saved_substitutes = get_saved_substitutes(db, 3)
            print(saved_substitutes)
            for saved_sub in saved_substitutes:
                saved_sub.display(db)
            # 2.2. Ask for return to home
        go_home = ask_for_home()
    db_disconnect(db)


if __name__ == "__main__":
    main()
