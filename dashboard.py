from tkinter import *
import transaction
import tkinter.ttk as table

def get_frame(window):
    frame = Frame(window, name = "dashboard")

    pay_money_card = Frame(frame, borderwidth = 2, relief = "raised", padx = 5, pady = 5)
    recieve_money_card = Frame(frame, borderwidth = 2, relief = "raised", padx = 5, pady = 5)
    transactions_card = Frame(frame, borderwidth = 2, relief = "raised", padx = 5, pady = 5)

    trans_table = table.Treeview(transactions_card)
    trans_table.grid(row = 0, column = 0, columnspan = 6)
    trans_table["columns"] = ["name", "amount", "type", "des", "dot"]
    trans_table["show"] = "headings"
    trans_table.heading("name", text = "Name")
    trans_table.heading("amount", text = "Amount")
    trans_table.heading("type", text = "Type")
    trans_table.heading("dot", text = "Date Of Transaction")
    trans_table.heading("des", text = "Description")
    index = 0
    for trans in transaction.get_last_transactions():
        trans_table.insert("", index, values=(trans.person_name, trans.amount, trans.trans_type, trans.description, trans.trans_date))
        index += 1
    pay_money_card.grid(row = 0, column = 0, columnspan = 3, rowspan = 2)
    recieve_money_card.grid(row = 0, column = 3, columnspan = 3, rowspan = 2)
    transactions_card.grid(row = 2, column = 1, columnspan = 4, rowspan = 2)

    return frame