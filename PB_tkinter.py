#! /usr/bin/env python3
# coding: utf-8


"""
Graphic Interface used by the Pur Beurre application.
3rd project of OC Python Developer Path.

Author: Loïc Mangin
"""

from pb_constants import *
from tkinter import *


def main():
    window = Tk()

    headline = Label(window,
                     text=pb_headline,
                     bg=brand_color_1, fg=font_color_2)
    headline.pack()

    opt_1_button = Radiobutton(window,
                       text=option_1_text,
                       bg=brand_color_2, fg=font_color_1,
                       command=window.quit)
    opt_1_button.pack()

    opt_2_button = Radiobutton(window,
                          text=option_2_text,
                          bg=brand_color_2, fg=font_color_1,
                          command=window.quit)
    opt_2_button.pack()

    var_text = StringVar()
    choice = Entry(window,
                   textvariable=var_text,
                   bg=bonbon, fg=font_color_2,
                   width=30)
    choice.pack()

    window.mainloop()


if __name__ == "__main__":
    main()
