#! /usr/bin/env python3
# coding: utf-8


"""
Graphic Interface used by the Pur Beurre application.
3rd project of OC Python Developer Path.

Author: Loïc Mangin
"""


import tkinter as tk

from PB_constants import *


""" BUTTONS """

class Category_button():
    pass

class Home_button():
    pass

class Exit_button():
    pass

class Info_button():
    pass

class Option_button():
    pass

class Previous_button():
    pass

class Save_button():
    pass

""" GRID AND MENU """

class Category_grid():
    pass

class Drop_down_menu():
    pass

class Footer_grid():
    pass

class Product_grid():
    pass

class Result_grid():
    pass

""" PUR BEURRE BRAND ELEMENTS """

class PB_headline():
    pass

class PB_logo():
    pass

class PB_welcome(tk.Frame):
    pass


def PB_window():
    window = tk.Tk()
    window.title(PB_BRAND)
    main_frame = tk.Frame(background=BRAND_COLOR_2,
                          width=960,
                          height=640)
    main_frame.pack()
    return window


def main():
    window = PB_window()

    headline = tk.Label(window, text=PB_BRAND)
    headline.pack()

    window.mainloop()


if __name__ == "__main__":
    main()
