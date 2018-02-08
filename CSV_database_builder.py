#! /usr/bin/env python3
# coding: utf-8


"""
Script building the database used by the Pur Beurre application
from the Open Food Facts data in CSV format.
3rd project of OC Python Developer Path.

Author: Loïc Mangin
"""


import pandas as pd


def add_nutriscore(data):
    """Add a column 'nutriscore' (A, B, C, D, E)
    based on 'main_category' (index=3)
    and 'nutrition-score-fr_100g' (index=4) fields.
    """
    score = []
    for row in data.values:
        print(row[3], row[4])
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
    PB_index = ['url',
                'product_name',
                'brands',
                'main_category',
                'nutrition-score-fr_100g']
    data = pd.read_csv(file, sep='\t',
                       usecols=PB_index)
    data = data.dropna()
    return data

def format_data(data):
    """Return the DataFrame with its string fields modified
    and without NaN field.
    """
    data['product_name'] = pd.DataFrame(name.capitalize()
                                    for name in data['product_name'])
    data['brands'] = pd.DataFrame(brand.capitalize()
                                    for brand in data['brands'])
    data['main_category'] = pd.DataFrame(category.upper()
                                    for category in data['main_category'])
    data = data.dropna()
    return data


def main():
    """categories = ['aliments-origine-végétale',
                  'biscuits-gâteaux',
                  'boissons',
                  'céréales-pommes-terre',
                  'desserts',
                  'plats-préparés',
                  'produits-laitiers',
                  'snacks-sucrés',
                  'viandes'
                  ]
                  """
    categories =['boissons']
    for category in categories:
        PB_data = read_CSV_data(category + '.csv')

        PB_data = format_data(PB_data)

        PB_data = add_nutriscore(PB_data)

    print(PB_data[:5])


if __name__ == "__main__":
    main()