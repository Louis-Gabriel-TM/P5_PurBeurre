# Pur Beurre

This repository contains the Python scripts and additional files of my __4th project__ for the __*Python Developer Path* in [*OpenClassrooms*](https://openclassrooms.com/paths/developpeur-se-dapplication-python)__.

This application is based on the __*Open Food Facts database*__ and uses its API (not really, in fact).

#### The aim of *Pur Beurre*

*Pur Beurre* is a fictive *start up* whose offer a *very simple* application that __*allows a consumer to obtain, for a chosen product, a healthier alternative*__.

## How to use Pur Beurre

Choose one of this two options on the __Home page__ :
1. '*Je souhaite trouver un substitut à un aliment*' [ Find a susbstitute ]
2. '*Je souhaite revoir les substituts que j'ai enregistré*' [ Show saved substitutes ]

#### Option 1: *Find a substitute*

First, choose a __category__ of products.
Second, choose a __product__ in this category.

*Pur Beurre* will propose you a healthier alternative to this product (with some details).

Then, you can choose to save this result (the sustitute with the selected product).

#### Option 2: *Show previous searches*

Show recently saved substitutes, ordered by date (from the youngest to the oldest).


## Files structure

__JSON_API_extractor.py__ contains a demo of data recovery via *Open Food Facts* API in JSON format. A limited number of requests is done to estimate the duration of recovering the entire french data.
The aim is to show this approach is not appropriate because the recovery of the french database would take some hours.

__CSV_database_builder.py__ uses the CSV file, downloaded from *Open Food Facts*, containing the entire french data.
The data are parsed using *dataframes* of the *pandas* library, then stored in a MySQL database, using *pymysql* library.

Download the french *Open Food Facts* database as a CSV file (more than 1.4 Go) : [download CSV file](https://fr.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv)

__PurBeurre.py__ is the main script of the application, using the previously created MySQL database.

__Note :__ *PB_tkinter.py* will offer a graphic interface to the application (in progress).

### Data Model of the MySQL database :

![Data Model](https://github.com/Louis-Gabriel-TM/PurBeurre/blob/master/images/data_model.JPG)
