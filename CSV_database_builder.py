#! /usr/bin/env python3
# coding: utf-8


"""
Script building the database used by the Pur Beurre application
from the Open Food Facts data in CSV format.
3rd project of OC Python Developer Path.

Author: Loïc Mangin
"""


import pandas as pd
import pymysql

from PB_constants import *

"""
------------------------------------------------------
PARSING FUNCTIONS FOR CSV FILES FROM 'OPEN FOOD FACTS'
------------------------------------------------------
"""

def add_nutriscore(dataframe):
    """Add a column 'nutriscore' (A, B, C, D, E)
    based on 'main_category' (index=4)
    and 'nutrition-score-fr_100g' (index=5) fields.
    """
    score = []
    for row in dataframe.values:
        score.append(nutriscore(row[4], row[5]))
    dataframe['nutriscore'] = pd.Series(score)
    return dataframe

def nutriscore(main_category, score):
    """Find the used scales at
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

def parse_CSV_data(dataframe):
    pb_categories = {category.lower() for category in PB_CATEGORIES}
    for i in dataframe.index:
        categories = dataframe.loc[i,'categories'].split(",")
        categories = {category.lower().strip() for category in categories}
        if pb_categories & categories != set():
            new_cat = str(list(pb_categories & categories)[0])
        else:
            new_cat = None
        dataframe.at[i, 'categories'] = new_cat
    dataframe = dataframe.dropna()
    dataframe = dataframe.reset_index(drop=True)
    return dataframe

def read_CSV_data(file):
    """Return a DataFrame containing the
    useful data for Pur Beurre application
    without NaN field,
    extracted from an Open Food Facts CSV file.
    """
    PB_index = ['url',
                'product_name',
                'brands',
                'categories',
                'main_category',
                'nutrition-score-fr_100g']
    dataframe = pd.read_csv(file, sep='\t',
                       usecols=PB_index)
    dataframe = dataframe.dropna()
    dataframe = dataframe.reset_index(drop=True)
    return dataframe

def format_CSV_data(dataframe):
    """Return the DataFrame with its string fields modified.
    """
    dataframe['product_name'] = pd.DataFrame(name.capitalize()
                                    for name in dataframe['product_name'])
    dataframe['brands'] = pd.DataFrame(brand.capitalize()
                                    for brand in dataframe['brands'])
    dataframe['main_category'] = pd.DataFrame(category[3:].capitalize()
                                    for category in dataframe['main_category'])
    return dataframe

"""
--------------------------------------------
BUILDING FUNCTIONS FOR 'PUR BEURRE' DATABASE
--------------------------------------------
"""

def connect_db():
    socket = pymysql.connect(host='localhost',
                             user='remy',
                             passwd='ratatouille',
                             db='PurBeurre_db',
                             charset='utf8')
    return socket

def disconnect_db(socket):
    socket.commit()
    socket.close()

def create_tables(socket):
    with socket.cursor() as cursor:
        cursor.execute("""  DROP TABLE IF EXISTS Saved_substitute; """)
        cursor.execute("""  DROP TABLE IF EXISTS Product; """)
        cursor.execute("""  DROP TABLE IF EXISTS Category; """)
        cursor.execute("""  CREATE TABLE Category (
                                id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
                                name VARCHAR(200) NOT NULL,
                                PRIMARY KEY(id)
                                )
                                ENGINE = InnoDB
                                DEFAULT CHARSET = 'utf8'; """)
        cursor.execute("""  CREATE TABLE Product (
                                id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                                id_category TINYINT UNSIGNED NOT NULL,
                                name VARCHAR(200) NOT NULL,
                                category VARCHAR(200) NOT NULL,
                                family VARCHAR(200) NOT NULL,
                                brands VARCHAR(200) NOT NULL,
                                score_100g TINYINT NOT NULL,
                                nutriscore CHAR(1) NOT NULL,
                                url VARCHAR(200) NOT NULL,
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

def insert_category(socket, category):
    with socket.cursor() as cursor:
        cursor.execute(""" INSERT INTO Category (name)
                               VALUES ("{}"); """
                       .format(category))

def insert_product(socket, category, product):
    with socket.cursor() as cursor:
        cursor.execute("""  INSERT INTO Product (id_category,
                                                 url,
                                                 name,
                                                 brands,
                                                 category,
                                                 family,
                                                 score_100g,
                                                 nutriscore)
                                VALUES ((SELECT id FROM Category
                                             WHERE name = "{0}"),
                                        "{1}", "{2}", "{3}", "{4}", {5}, "{6}"); """
                       .format(category, product[0], product[1], product[2], product[3], product[4], product[5], product[6]))
    socket.commit()


def main():
    #for category in PB_CATEGORIES:
    #    print(category)


    # PARSING CSV FILES FROM 'OPEN FOOD FACTS'
    PB_data = read_CSV_data('boissons.csv')
    #print(PB_data[:5])
    PB_data = parse_CSV_data(PB_data)
    #print(PB_data[:5])

    PB_data = format_CSV_data(PB_data)
    PB_data = add_nutriscore(PB_data)
    print(PB_data[:5])

    # BUILDING 'PUR BEURRE' DATABASE
    db = connect_db()
    create_tables(db)

    for category in PB_CATEGORIES:
        insert_category(db, category)
    """
    for product in PB_data.values:
        print(product)
        insert_product(db, 'boissons', product)
        for j in range(6):
            print(product[j])
        print()
    """
    disconnect_db(db)



if __name__ == "__main__":
    main()