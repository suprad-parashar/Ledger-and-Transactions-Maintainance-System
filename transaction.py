"""
Implemented By Sandeep N S (1JB17IS079)
Transaction Module Functionalities are :
    1. Add New Transactions.
    2. Delete Old Transactions.
    3. Displays Transaction that have previously happened.
"""

from tkinter import *
import tkinter.ttk as table
import hashlib as Hash
import pickle
from datetime import datetime
import tkinter.messagebox as dialog


class Transaction:
    def __init__(self, trans_id, sender_name, des, amount, trans_date, trans_type):
        self.trans_id = trans_id
        self.sender_name = sender_name
        self.description = des
        self.amount = amount
        self.trans_date = trans_date
        if trans_type==1:
            self.trans_type = "Debit"
        else:
            self.trans_type = "Credit"


def get_frame(window) :
    frame = Frame(window)

    trans_table = table.Treeview(frame)
    trans_table.grid(row=0, column=0, columnspan=6)
    trans_table["columns"] = ["name", "amount", "dot","des","type"]
    trans_table["show"] = "headings"
    trans_table.heading("name", text="Name")
    trans_table.heading("amount", text="Amount")
    trans_table.heading("dot", text="Date Of Transaction")
    trans_table.heading("des", text="Description")
    trans_table.heading("type",text="Type")
    try:
        with open("files/transaction.ltms", "rb") as file:
            trans = []
            try:
                while True:
                    a_trans = pickle.load(file)
                    trans.append(a_trans)
            except EOFError:
                pass

            trans.sort(key=lambda person: a_trans.trans_date)
            index = 0
            for a_trans in trans:
                trans_table.insert("", index, values=(a_trans.sender_name, a_trans.amount, a_trans.trans_date,a_trans.description,a_trans.trans_type))
                index += 1
    except FileNotFoundError:
        with open("files/transaction.ltms", "wb") as file:
            pass

    add_button = Button(frame, text="Add Transaction", command=add_transaction)
    delete_button = Button(frame, text="Delete Transaction")  # command = delete_transaction
    view_button = Button(frame,text = "View Transaction",command = view_transaction)
    add_button.grid(row=1, column=0, columnspan=2)
    delete_button.grid(row=1, column=2, columnspan=2)
    view_button.grid(row = 1, column=4, columnspan=2)

    return frame


def writename(text):
    print(text)


def add_transaction():

    #Saving Transactions into File
    def save_transaction():
        sender_name = sname_var.get()
        amount = amount_input.get()
        des = des_input.get()
        trans_type = typeOfTrans.get()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        trans_date_and_time = dt_string
        if amount == "0" or amount == "" :
            dialog.showerror("Invalid Input", "Name cannot be empty.")
        else:
            trans_id = Hash.md5((sender_name + amount).encode()).hexdigest()
            with open("files/transaction.ltms", "ab") as file:
                with open("files/index_transaction.txt", "a") as index:
                    index.write(trans_id + " " + str(file.tell()) + "\n")
                trans = Transaction(trans_id, sender_name, des, amount, trans_date_and_time, trans_type)
                pickle.dump(trans, file)
            trans_sub_window.destroy()


    #Variable for the Type Of Transaction(Debit Or Credit)
    typeOfTrans = IntVar()

    #Transaction Window
    trans_sub_window = Tk()
    entry_var = StringVar()
    trans_sub_window.title("Add Transaction")

    bottom_frame = Frame(trans_sub_window)
    bottom_frame.pack(side=BOTTOM)

    add_button = Button(bottom_frame, text="Add Transaction", command=save_transaction)
    cancel_button = Button(bottom_frame, text="Cancel", command=trans_sub_window.quit)
    cancel_button.pack(side=TOP)
    add_button.pack(side=TOP)

    top_frame = Frame(trans_sub_window)
    top_frame.pack(side=TOP)

    #Adding The Labels And Input Fields (Entry)
    sname = Label(top_frame, text="Sender Name", textvariable=entry_var)
    sname.grid(row=0, column=0)
    sname_var = StringVar(top_frame)
    # TODO: The Display the list of Names to choose from.
    #Taking Input from File for List of People added by User.
    try:
        with open("files/people.ltms", "rb") as f:
            people = []
            try:
                while True:
                    person = pickle.load(f)
                    people.append(person)
            except EOFError:
                pass
            people.sort(key=lambda person: person.name)
            print(people)
    except FileNotFoundError :
        with open("files/people.ltms", "wb") as file:
            pass

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
