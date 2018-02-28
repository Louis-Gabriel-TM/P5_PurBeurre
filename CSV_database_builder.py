#! /usr/bin/env python3
# coding: utf-8


"""
Script building the database for the 'Pur Beurre' application
using the Open Food Facts data in CSV format.

5th project of OC Python Developer Path.

Author: Loïc Mangin
"""


from PB_constants import *

import pandas as pd
import pymysql


"""
------------------------------------------------------
PARSING FUNCTIONS FOR CSV FILES FROM 'OPEN FOOD FACTS'
------------------------------------------------------
"""


def add_nutriscore(dataframe):
    """Add a column 'nutriscore' (A, B, C, D, E) based on
    'main_category' (index=4) and 'nutrition-score-fr_100g' (index=5) fields.
    """
    score = []
    for row in dataframe.values:
        score.append(nutriscore(row[4], row[5]))
    dataframe['nutriscore'] = pd.Series(score)
    return dataframe


def format_csv_data(dataframe):
    """Return the DataFrame with some string fields modified.
    """
    dataframe['product_name'] = pd.DataFrame(name.capitalize()
                                             for name in dataframe['product_name'])
    dataframe['brands'] = pd.DataFrame(brand.capitalize()
                                       for brand in dataframe['brands'])
    dataframe['main_category'] = pd.DataFrame(category[3:].capitalize()
                                              for category in dataframe['main_category'])
    return dataframe


def nutriscore(main_category, score):
    """Return the 'nutriscore' (A, B, C, D, E) based on
    the value of 'nutrition-score-fr_100g'.
    The used scales can be find at :
    https://fr.openfoodfacts.org/score-nutritionnel-experimental-france
    """
    if main_category.upper().find('BOISSON') != -1:
        # Use nutriscore scale for drinks
        if -15 <= score <= 0:
            return 'A'
        elif 1 <= score <= 4:
            return 'B'
        elif 5 <= score <= 8:
            return 'C'
        elif 9 <= score <= 11:
            return 'D'
        else:
            return 'E'
    else:
        # Use nutriscore scale for food
        if -15 <= score <= -2:
            return 'A'
        elif -1 <= score <= 3:
            return 'B'
        elif 4 <= score <= 11:
            return 'C'
        elif 12 <= score <= 16:
            return 'D'
        else:
            return 'E'


def parse_csv_data(dataframe):
    """Return a dataframe containing only products in the right
    categories and without too long strings.
    The brand 'Fleury Michon' is excluded due to escapement issues
    in its strings fields.
    """
    pb_categories = {category.lower() for category in PB_CATEGORIES}
    for i in dataframe.index:
        categories = dataframe.loc[i, 'categories'].split(",")
        categories = {category.lower().strip() for category in categories}
        if pb_categories & categories == set()\
                or len(dataframe.loc[i, 'product_name']) > 50\
                or len(dataframe.loc[i, 'main_category']) > 100\
                or len(dataframe.loc[i, 'brands']) > 50\
                or len(dataframe.loc[i, 'url']) > 100\
                or dataframe.loc[i, 'brands'] in ['Fleury Michon']:
            new_cat = None
        else:
            new_cat = str(list(pb_categories & categories)[0])
        dataframe.at[i, 'categories'] = new_cat
    dataframe = dataframe.dropna()
    dataframe = dataframe.reset_index(drop=True)
    return dataframe


def read_csv_data(file):
    """Return a DataFrame containing the useful data for the 'Pur Beurre'
    application without NaN / NULL field,
    extracted from an Open Food Facts CSV file.
    """
    pb_index = ['url',
                'product_name',
                'brands',
                'categories',
                'main_category',
                'nutrition-score-fr_100g']
    dataframe = pd.read_csv(file, sep='\t',
                            usecols=pb_index)
    dataframe = dataframe.dropna()
    dataframe = dataframe.reset_index(drop=True)
    return dataframe


"""
--------------------------------------------
BUILDING FUNCTIONS FOR 'PUR BEURRE' DATABASE
--------------------------------------------
"""


def create_tables(socket):
    """Drop existing tables of the 'Pur Beurre' database and recreate them.
    """
    with socket.cursor() as cursor:
        cursor.execute("""  DROP TABLE IF EXISTS Saved_substitute; """)
        cursor.execute("""  DROP TABLE IF EXISTS Product; """)
        cursor.execute("""  DROP TABLE IF EXISTS Category; """)
        cursor.execute("""  CREATE TABLE Category (
                                id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
                                name VARCHAR(50) NOT NULL,
                                PRIMARY KEY(id)
                                )
                                ENGINE = InnoDB
                                DEFAULT CHARSET = 'utf8'; """)
        cursor.execute("""  CREATE TABLE Product (
                                id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                                id_category TINYINT UNSIGNED NOT NULL,
                                name VARCHAR(50) NOT NULL,
                                subcategory VARCHAR(100) NOT NULL,
                                brands VARCHAR(50) NOT NULL,
                                score_100g TINYINT NOT NULL,
                                nutriscore CHAR(1) NOT NULL,
                                url VARCHAR(100) NOT NULL,
                                PRIMARY KEY(id),
                                CONSTRAINT fk_category_id
                                    FOREIGN KEY(id_category)
                                    REFERENCES Category(id)
                                )
                                ENGINE = InnoDB
                                DEFAULT CHARSET = 'utf8'; """)
        cursor.execute("""  CREATE TABLE Saved_substitute (
                                id INT UNSIGNED NOT NULL AUTO_INCREMENT,
                                id_product BIGINT UNSIGNED NOT NULL,
                                id_substitute BIGINT UNSIGNED NOT NULL,
                                backup_date DATE NOT NULL,
                                PRIMARY KEY(id),
                                CONSTRAINT fk_product_id
                                    FOREIGN KEY(id_product)
                                    REFERENCES Product(id),
                                CONSTRAINT fk_substitute_id
                                    FOREIGN KEY(id_substitute)
                                    REFERENCES Product(id)
                                )
                                ENGINE = InnoDB
                                DEFAULT CHARSET = 'utf8'; """)


def db_connect():
    """Return an access to the 'Pur Beurre' database previously created.
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


def insert_category(socket, category):
    """Fill the 'Category' table of 'Pur Beurre' database.
    """
    with socket.cursor() as cursor:
        cursor.execute(""" INSERT INTO Category (name)
                               VALUES ("{}"); """
                       .format(category))


def insert_product(socket, product):
    """Fill the 'Product' table of 'Pur Beurre' database.
    """
    with socket.cursor() as cursor:
        cursor.execute("""  INSERT INTO Product (id_category,
                                                 url,
                                                 name,
                                                 brands,
                                                 subcategory,
                                                 score_100g,
                                                 nutriscore)
                                VALUES ((SELECT id FROM Category
                                             WHERE name = "{0}"), "{1}",
                                              "{2}", "{3}", "{4}", {5}, "{6}"); """
                       .format(product[3], product[0], product[1], product[2], product[4], product[5], product[6]))


"""
-------------
MAIN FUNCTION
-------------
"""


def main():
    # --- PARSING CSV FILES FROM 'OPEN FOOD FACTS' ---
    pb_data = read_csv_data('fr.openfoodfacts.org.products.csv')
    # pb_data = read_CSV_data('boissons.csv')
    pb_data = parse_csv_data(pb_data)
    pb_data = format_csv_data(pb_data)
    pb_data = add_nutriscore(pb_data)

    # --- BUILDING 'PUR BEURRE' DATABASE ---
    db = db_connect()
    create_tables(db)
    for category in PB_CATEGORIES:
        insert_category(db, category)
    count = 0
    for product in pb_data.values:
        count += 1
        print(count)
        print(product)
        insert_product(db, product)
        print()
    db_disconnect(db)


if __name__ == "__main__":
    main()
