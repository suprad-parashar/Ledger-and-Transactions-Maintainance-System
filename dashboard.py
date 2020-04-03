from tkinter import *

def get_frame(window):
    frame = Frame(window, name = "dashboard")

    pay_money_card = Frame(frame, borderwidth = 2, relief = "raised", padx = 5, pady = 5)
    recieve_money_card = Frame(frame, borderwidth = 2, relief = "raised", padx = 5, pady = 5)
    transactions_money_card = Frame(frame, borderwidth = 2, relief = "raised", padx = 5, pady = 5)
    pay_money_card.grid(row = 0, column = 0, columnspan = 3, rowspan = 2)
    recieve_money_card.grid(row = 0, column = 3, columnspan = 3, rowspan = 2)
    transactions_money_card.grid(row = 2, column = 1, columnspan = 4, rowspan = 2)

    return frame