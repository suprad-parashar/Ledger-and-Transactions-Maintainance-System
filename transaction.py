"""
Implemented By Sandeep N S (1JB17IS079)
Transaction Module Functionalities are :
    1. Add New Transactions.
    2. Delete Old Transactions.
    3. Displays Transaction that have previously happened.
"""
from tkinter import *

class Transaction:
    def __init__(self, trans_id, from_, amount, trans_date, trans_type):
        self.trans_id = trans_id
        self.from_ = from_
        self.amount = amount
        self.trans_date = trans_date
        self.trans_type = trans_type


def get_frame(window) :
    frame = Frame(window)

    add_button = Button(frame, text="Add Transaction", command=add_transaction)
    delete_button = Button(frame, text="Delete Transaction")  # command = delete_transaction
    view_button = Button(frame,text = "View Transaction",command = view_transaction)
    add_button.grid(row=0, column=0, columnspan=2)
    delete_button.grid(row=2, column=0, columnspan=2)
    view_button.grid(row = 3, column=0, columnspan=2)

    return frame


def writename(text):
    print(text)


def add_transaction():
    typeOfTrans = StringVar()

    trans_sub_window = Tk()
    entry_var = StringVar()
    trans_sub_window.title("Add Transaction")

    bottom_frame = Frame(trans_sub_window)
    bottom_frame.pack(side=BOTTOM)

    save_button = Button(bottom_frame, text="Add Transaction", command=writename(entry_var.get()))
    # save_button.bind("<Button-1>", )
    cancel_button = Button(bottom_frame, text="Cancel", command=trans_sub_window.quit)
    cancel_button.pack(side=TOP)
    save_button.pack(side=TOP)

    top_frame = Frame(trans_sub_window)
    top_frame.pack(side=TOP)

    sname = Label(top_frame, text="Sender Name", textvariable=entry_var)
    sname.grid(row=0, column=0)
    sname_input = Entry(top_frame)
    sname_input.grid(row=0, column=1)

    amount = Label(top_frame, text="Amount (in Rs.)")
    amount.grid(row=1, column=0)
    amount_input = Entry(top_frame)
    amount_input.grid(row=1, column=1)

    trans_type = Label(top_frame, text="Transaction Type")
    trans_type.grid(row=4, column=0)
    trans_type_frame = Frame(top_frame)
    debit_radio = Radiobutton(trans_type_frame, text="Debit", value = 1, variable=typeOfTrans, state=ACTIVE)
    credit_radio = Radiobutton(trans_type_frame, text="Credit", value =2, variable=typeOfTrans, state=ACTIVE)
    debit_radio.pack(side=LEFT)
    credit_radio.pack(side=LEFT)
    trans_type_frame.grid(row=4, column=1)


    des = Label(top_frame, text="Description")
    des.grid(row = 5, column = 0)
    des_input = Entry(top_frame)
    des_input.grid(row=5, column=1)

    trans_sub_window.mainloop()


# Still in Progress.
def view_transaction():
    trans_history_sub_window = Tk()
    trans_history_sub_window.title("View Transaction")

    list = Listbox(trans_history_sub_window)
    list.insert(1,"India")
    list.pack()

    trans_history_sub_window.mainloop()
