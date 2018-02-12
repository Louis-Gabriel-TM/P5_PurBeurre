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

"""
------------------------------------------------------
PARSING FUNCTIONS FOR CSV FILES FROM 'OPEN FOOD FACTS'
------------------------------------------------------
"""

def add_nutriscore(data):
    """Add a column 'nutriscore' (A, B, C, D, E)
    based on 'main_category' (index=3)
    and 'nutrition-score-fr_100g' (index=4) fields.
    """
    score = []
    for row in data.values:
        score.append(nutriscore(row[3], row[4]))
    data['nutriscore'] = pd.Series(score)
    return data

def nutriscore(main_category, score):
    """Find the used scales at
    https://fr.openfoodfacts.org/score-nutritionnel-experimental-france
    """
    if main_category.find('BOISSON') == -1:
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
    else:
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

def read_CSV_data(file):
    """Return a DataFrame containing the
    useful data for Pur Beurre application
    without NaN field,
    extracted from an Open Food Facts CSV file.
    """
    PB_index = ['product_name',
                'brands',
                'main_category',
                'nutrition-score-fr_100g',
                'url']
    data = pd.read_csv(file, sep='\t',
                       usecols=PB_index)
    data = data.dropna()
    data = data.reset_index(drop=True)
    return data

def format_data(data):
    """Return the DataFrame with its string fields modified.
    """
    data['product_name'] = pd.DataFrame(name.capitalize()
                                    for name in data['product_name'])
    data['brands'] = pd.DataFrame(brand.capitalize()
                                    for brand in data['brands'])
    data['main_category'] = pd.DataFrame(category[3:].capitalize()
                                    for category in data['main_category'])
    return data

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
                                main_category VARCHAR(200) NOT NULL,
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
                               VALUES ('{}'); """
                       .format(category))

def insert_product(socket, category, product):
    with socket.cursor() as cursor:
        cursor.execute("""  INSERT INTO Product (id_category,
                                                 url,
                                                 name,
                                                 brands,
                                                 main_category,
                                                 score_100g,
                                                 nutriscore)
                                VALUES ((SELECT id FROM Category
                                             WHERE name = "{0}"),
                                        "{1}", "{2}", "{3}", "{4}", {5}, "{6}"); """
                       .format(category, product[0], product[1], product[2], product[3], product[4], product[5]))
    socket.commit()


def main():
    categories =['boissons']

    # PARSING CSV FILES FROM 'OPEN FOOD FACTS'
    for category in categories:
        PB_data = read_CSV_data(category + '.csv')
        PB_data = format_data(PB_data)
        PB_data = add_nutriscore(PB_data)

    # BUILDING 'PUR BEURRE' DATABASE
    db = connect_db()
    create_tables(db)
    for category in categories:
        insert_category(db, category)
    for product in PB_data.values:
        print(product)
        insert_product(db, 'boissons', product)
        for j in range(6):
            print(product[j])
        print()
    disconnect_db(db)


if __name__ == "__main__":
    main()