#! /usr/bin/env python3
# coding: utf-8


"""
Pur Beurre, an application to find a healthier food.

5th project of OC Python Developer Path.

Author: Loïc Mangin
"""


from classes.category import *
from classes.product import *
from classes.saved_substitute import *
from PB_constants import *

from datetime import datetime

import pymysql


def ask_for_home():
    print()
    option = choose_option("Souhaitez-vous revenir à la page d'accueil ?",
                  option_1="Retourner à l'accueil",
                  option_2="Quitter")
    if option == 1:
        return True
    else:
        return False


def db_connect():
    """Return an access to the 'Pur Beurre' database previously created.
    """
    socket = pymysql.connect(host='localhost',
                             user='remy',
                             passwd='ratatouille',
                             db='PurBeurre_db',
                             charset='utf8')
    return socket


def choose_line(listing, text, alt):
    choice = input(text)
    print()
    if not (1 <= int(choice) <= len(listing)):
        print(alt)
        print()
        choice = choose_line(listing, text, alt)
    return int(choice)


def choose_product(excerpt):
    choice = input("Produit choisi : ")
    print()
    if not (1 <= int(choice) <= len(excerpt)):
        print("Ce produit n'est pas proposé.")
        print()
        choice = choose_product(excerpt)
    return int(choice)


def choose_option(text, option_1, option_2):
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


def db_disconnect(socket):
    """Push the modifications in the 'Pur Beurre' database
    and close access to it.
    """
    socket.commit()
    socket.close()


def display_categories(categories):
    for category in categories:
        category.display()


def display_head():
    head_length = max(len(PB_BRAND), len (PB_HEADLINE))
    print()
    print("#" * (head_length + 8))
    print("#   " + PB_BRAND.upper().center(head_length) + "   #")
    print("#   " + PB_HEADLINE.center(head_length) + "   #")
    print("#" * (head_length + 8))
    print()


def display_excerpt(prod_list, head):
    print("--- " + head.upper() + " ---")
    i = 0
    for product in prod_list:
        i += 1
        print("  " + str(i) + ". " + product.name + " ("
              + product.nutriscore + ", " + str(product.score_100g) + ")")


def get_saved_substitutes(socket):
    saved_list = []
    with socket.cursor() as cursor:
        cursor.execute("""  SELECT * FROM Saved_substitute
                                LIMIT 3; """)
        saved_tuples = cursor.fetchall()
    for saved_sub in saved_tuples:
        saved_substitute = Saved_substitute(saved_sub[0], saved_sub[1], saved_sub[2], saved_sub[3])
        saved_list.append(saved_substitute)
    return saved_list


def get_substitutes(socket, product):
    sub_list = []
    with socket.cursor() as cursor:
        cursor.execute("""  SELECT * FROM Product
                                WHERE subcategory = '{0}' AND nutriscore < '{1}'
                                LIMIT 5; """.format(product.subcategory, product.nutriscore))
        sub_tuples = cursor.fetchall()
    for sub in  sub_tuples:
        substitute = Product(sub[0], sub[1], sub[2], sub[3], sub[4], sub[5], sub[6], sub[7])
        sub_list.append(substitute)
    return sub_list


def get_categories(socket):
    cat_list = []
    with socket.cursor() as cursor:
        cursor.execute("""  SELECT * FROM Category; """)
        cat_tuples = cursor.fetchall()
    for cat in cat_tuples:
        category = Category(cat[0], cat[1])
        cat_list.append(category)
    return cat_list


def get_excerpt(socket, cat_id):
    prod_list = []
    with socket.cursor() as cursor:
        cursor.execute("""  SELECT * FROM Product
                                WHERE id_category = {0} AND nutriscore != 'A'
                                LIMIT 10; """.format(cat_id))
        prod_tuples = cursor.fetchall()
    for prod in prod_tuples:
        #print(prod)
        product = Product(prod[0], prod[1], prod[2], prod[3], prod[4], prod[5], prod[6], prod[7])
        prod_list.append(product)
        #product.display()
    return prod_list


def save_substitute(socket, product, substitute):
    with socket.cursor() as cursor:
        cursor.execute("""  INSERT INTO Saved_substitute (id_product, 
                                                          id_substitute,
                                                          backup_date)
                                VALUES ({0}, {1}, CURRENT_DATE()); """
                       .format(product.id, substitute.id))


def main():
    db = db_connect()
    go_home = True
    while go_home:
        # --- HOME PAGE ---
        display_head()
        option = choose_option(text="En quoi 'Pur Beurre' peut-il vous aider ?",
                               option_1=OPT_1_TEXT,
                               option_2=OPT_2_TEXT)
        if option == 1:
            # --- OPTION 1: Find a substitute ---
            # 1.1. Chose category
            categories = get_categories(db)
            print("--- CATEGORIES DISPONIBLES ---")
            display_categories(categories)
            chosen_cat = choose_line(categories,
                                     text="Catégorie choisie : ",
                                     alt="Cette catégorie n'existe pas.")
            # 1.2. Choose product
            excerpt = get_excerpt(db, chosen_cat)
            display_excerpt(excerpt, "Quelques produits issus de cette catégorie")
            chosen_prod = choose_line(excerpt,
                                         text="Produit choisi : ",
                                         alt="Ce produit n'est pas proposé.")
            # 1.3. Show substitutes
            results = get_substitutes(db, excerpt[chosen_prod - 1])
            if results == []:
                print(">>> Désolé, 'Pur Beurre' n'a pu vous trouver aucun substitut <<<")
            else:
                display_excerpt(results, "Substituts proposés")
                # 1.4. Show more informations on a product
                chosen_substitute = choose_line(results,
                                                text="Sur quel substitut souhaité vous davantage d'informations : ",
                                                alt="Ce substitut n'est pas proposé.")
                results[chosen_substitute - 1].display()
                option = choose_option(text="Souhaitez-vous sauvegarder ce résultat ?",
                                       option_1="Sauvegarder le substitut",
                                       option_2="Ne pas sauvegarder")
                if option == 1:
                    # 1.5a. Save substitute
                    product = excerpt[chosen_prod - 1]
                    substitute = results[chosen_substitute - 1]
                    save_substitute(db, product, substitute)
        else:
            # --- OPTION 2: View saved substitues
            # 2.1. Show saved substitutes
            saved_substitutes = get_saved_substitutes(db)
            for saved_sub in saved_substitutes:
                saved_sub.display(db)
            # 2.2. Ask for return to home
        go_home = ask_for_home()
    db_disconnect(db)


if __name__ == "__main__":
    main()
