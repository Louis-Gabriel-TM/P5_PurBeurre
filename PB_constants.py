#! /usr/bin/env python3
# coding: utf-8


"""
Graphic Constants used by the Pur Beure appplication.

5th project of OC Python Developer Path.

Author: Loïc Mangin
"""


"""
------------------
DATABASE CONSTANTS
------------------
"""


PB_CATEGORIES = {"Aliments d'origine végétale",
                 "Boissons",
                 "Céréales et dérivés",
                 "Desserts",
                 "Plats préparés",
                 "Produits de la mer",
                 "Produits laitiers",
                 "Snacks sucrés",
                 "Viandes"}


"""
-------------------
INTERFACE CONSTANTS
-------------------
"""


HOME_ASK = "En quoi 'Pur Beurre' peut-il vous aider ?"
HOME_1_TEXT = "Je souhaite trouver un substitut à un aliment."
HOME_2_TEXT = "Je souhaite revoir les substituts que j'ai enregistré."

CATEGORY_ASK = "Catégorie choisie : "
CATEGORY_ALT = "Cette catégorie n'est pas proposée."

PRODUCT_HEAD = "Quelques produits issus de cette catégorie"
PRODUCT_ASK = "Produit choisi : "
PRODUCT_ALT = "Ce produit n'est pas proposé."

NO_RESULT = ">>> Désolé, 'Pur Beurre' n'a pu trouver aucun substitut <<<"

SUBSTITUTE_HEAD = "Substituts proposés"
SUBSTITUTE_ASK = "Sur quel substitut souhaitez-vous " \
                 "davantage d'informations : "
SUBSTITUTE_ALT = "Ce substitut n'est pas proposé."

SAVE_ASK = "Souhaitez-vous sauvegarder ce résultat : "
SAVE_1_TEXT = "Sauvegareder le substitut."
SAVE_2_TEXT = "Ne pas sauvegarder."

"""
Corporate Identity and Style Guide Constants
"""

PB_BRAND = "Pur Beurre"
PB_HEADLINE = "Du gras, oui, mais de qualité !"
PB_LOGO = "images/pb_logo.png"

# --- 'PUR BEURRE' COLORS ---
FONT_COLOR_1 = '#C45525'  # color 'Rooibos chocolat'
FONT_COLOR_2 = '#345A61'  # color 'Moules frites'
BONBON_COLOR = '#86EBE6'
BRAND_COLOR_1 = '#DE9440'  # color 'Caramel mou'
BRAND_COLOR_2 = '#E8A75D'  # color 'Biscuit trempé'
