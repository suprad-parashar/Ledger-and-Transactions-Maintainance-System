import os
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
        if trans_type == 0:
            self.trans_type = "Debit"
        else:
            self.trans_type = "Credit"

    def get_table_data(self):
        return self.sender_name, self.amount, self.trans_type, self.description, self.trans_date

def get_person_transactions(person):
    with open("files/transaction.ltms", "rb") as file:
        transactions = []
        try:
            while True:
                transaction = pickle.load(file)
                if transaction.sender_name == person.name:
                    transactions.append(transaction)
        except:
            return transactions


# Gets Data from People file.
def get_people_list():
    people_names = []
    try:
        with open("files/people.ltms", "rb") as f:
            try:
                while True:
                    person = pickle.load(f)
                    people_names.append(person)
            except EOFError:
                pass
            people_names.sort(key=lambda person: person.name)
    except FileNotFoundError:
        with open("files/people.ltms", "wb") as _:
            pass
    return people_names


# Reloads the Table Contents
def refresh_table(trans_table):
    for entry in trans_table.get_children():
        trans_table.delete(entry)
    with open("files/transaction.ltms", "rb") as file:
        trans = []
        try:
            while True:
                transaction = pickle.load(file)
                trans.append(transaction)
        except EOFError:
            pass
        trans.sort(key=lambda trans: trans.trans_date, reverse=True)
        print(trans)
        index = 0
        for transaction in trans:
            trans_table.insert("", index, values=transaction.get_table_data(), tags=transaction.trans_id)
            index += 1


def get_frame(window):
    frame = Frame(window)

    # Create files if it does not exists.
    try:
        with open("files/transaction.ltms", "rb") as _, open("files/index_transaction.txt", "r") as _:
            pass
    except FileNotFoundError:
        os.mkdir("files")
        with open("files/transaction.ltms", "wb") as _, open("files/index_transaction.txt", "w") as _:
            pass

    trans_table = table.Treeview(frame)
    trans_table.grid(row=0, column=0, columnspan=6)
    trans_table["columns"] = ["name", "amount", "type", "des", "dot" ]
    trans_table["show"] = "headings"
    trans_table.heading("name", text="Name")
    trans_table.heading("amount", text="Amount")
    trans_table.heading("type", text="Type")
    trans_table.heading("dot", text="Date Of Transaction")
    trans_table.heading("des", text="Description")


    try:
        with open("files/transaction.ltms", "rb") as file:
            trans = []
            try:
                while True:
                    a_trans = pickle.load(file)
                    trans.append(a_trans)
            except EOFError:
                pass

            trans.sort(key=lambda a_trans:a_trans.trans_date,reverse=True)
            index = 0
            for a_trans in trans:
                trans_table.insert("", index, values=(
                a_trans.sender_name, a_trans.amount, a_trans.trans_type, a_trans.description, a_trans.trans_date),
                                   tags=a_trans.trans_id)
                index += 1
    except FileNotFoundError:
        with open("files/transaction.ltms", "wb") as _:
            pass

    add_button = Button(frame, text="Add Transaction", command=lambda: add_transaction(trans_table))
    delete_button = Button(frame, text="Delete Transaction",
                           command=lambda: delete_transaction(trans_table.item(trans_table.selection()[0]),
                                                              trans_table))

    add_button.grid(row=1, column=0, columnspan=2)
    delete_button.grid(row=1, column=1, columnspan=2)

    return frame


def writename(text):
    print(text)


#TODO: Give option to user whether to enable or diabl this option
def delete_transaction(item, trans_table):
    print(item)
    delete_id = item["tags"][0]
    delete_index = 0
    index = 0
    with open("files/transaction.ltms", "rb") as trans_file, open("files/index_transaction.txt", "r") as index_file:
        trans = []
        indices = []
        try:
            while True:
                transaction = pickle.load(trans_file)
                entry = index_file.readline().split()
                if transaction.trans_id == delete_id:
                    delete_index = index
                trans.append(transaction)
                indices.append(entry)
                index += 1
        except EOFError:
            pass
    deleted_transaction = trans.pop(delete_index)
    indices.pop(delete_index)
    result = dialog.askquestion("Delete Transaction",
                                "Do you want to delete the Transaction with {} from History?".format(
                                    deleted_transaction.sender_name), icon='warning')
    if result == 'yes':
        with open("files/transaction.ltms", "wb") as trans_file, open("files/index_transaction.txt", "w") as index_file:
            for i in range(len(trans)):
                pickle.dump(trans[i], trans_file)
                index_file.write(" ".join(indices[i]) + "\n")
        dialog.showinfo("Deletion Successful",
                        "The Transaction with person named {} on {} has been deleted from the record.".format(
                            deleted_transaction.sender_name, deleted_transaction.trans_date))
        refresh_table(trans_table)

def add_transaction(trans_table):
    # Saving Transactions into File
    def save_transaction():
        sender_name = sname_var.get()
        amount = amount_input.get()
        des = des_input.get()
        trans_type = typeOfTrans.get()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        trans_date_and_time = dt_string

        trans_id = Hash.md5((sender_name + amount).encode()).hexdigest()
        trans = Transaction(trans_id, sender_name, des, amount, trans_date_and_time, trans_type)

        #Verifying entered Amount
        if amount == "0" or amount == "" or not amount.isdigit():
            dialog.showerror("Invalid Input", "Enter Some Amount")
        else:
            #Asking for Confirmation
            r = dialog.askquestion("Delete Transaction",
                                   "Do you want to add this Transaction to record?", icon='warning')
            if r == "yes":
                with open("files/transaction.ltms", "ab") as file:
                    with open("files/index_transaction.txt", "a") as index:
                        index.write(trans_id + " " + str(file.tell()) + "\n")
                    pickle.dump(trans, file)
                    refresh_table(trans_table)
                    trans_sub_window.destroy()

            else:
                trans_sub_window.destroy()
        refresh_table(trans_table)

    # Transaction Window
    trans_sub_window = Tk()
    entry_var = StringVar()
    trans_sub_window.title("Add Transaction")

    bottom_frame = Frame(trans_sub_window)
    bottom_frame.pack(side=BOTTOM)

    add_button = Button(bottom_frame, text="Add Transaction", command=lambda: save_transaction())
    cancel_button = Button(bottom_frame, text="Cancel", command=trans_sub_window.quit)
    add_button.grid(row=6,column=0,columnspan=2)
    cancel_button.grid(row=6,column=2,columnspan=2)


    top_frame = Frame(trans_sub_window)
    top_frame.pack(side=TOP)

    # Adding The Labels And Input Fields (Entry)
    sname = Label(top_frame, text="Sender Name", textvariable=entry_var)
    sname.grid(row=0, column=0)
    sname_var = StringVar(top_frame)

    options = get_people_list()
    names = []
    for i in options:
        names.append(i.name)

    sname_var.set(names[0])
    sname_input = table.Combobox(top_frame, width=17, textvariable=sname_var, values=names)
    sname_input.grid(row=0, column=1)

    amount = Label(top_frame, text="Amount (in Rs.)")
    amount.grid(row=1, column=0)
    amount_input = Entry(top_frame)
    amount_input.grid(row=1, column=1)

    trans_type = Label(top_frame, text="Transaction Type")
    trans_type.grid(row=4, column=0)
    trans_type_frame = Frame(top_frame)
    typeOfTrans = IntVar(trans_type_frame)
    typeOfTrans.set(0)
    debit_radio = Radiobutton(trans_type_frame, text="Debit", value=0, variable=typeOfTrans)
    credit_radio = Radiobutton(trans_type_frame, text="Credit", value=1, variable=typeOfTrans)
    debit_radio.pack(side=LEFT)
    credit_radio.pack(side=LEFT)
    trans_type_frame.grid(row=4, column=1)

    des = Label(top_frame, text="Description")
    des.grid(row=5, column=0)
    des_input = Entry(top_frame)
    des_input.grid(row=5, column=1)

    trans_sub_window.mainloop()
