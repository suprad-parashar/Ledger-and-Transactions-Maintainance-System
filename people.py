from tkinter import *
import tkinter.messagebox as dialog
from tkinter.simpledialog import askstring
import tkinter.ttk as table
import hashlib as Hash
import pickle
import os
from datetime import datetime
import helper
import transaction


# TODO: Fix bug. Quit has to be pressed multiple times to work.

# A Person class to store the deatils of a person.
class Person:
    # The constructor of the class.
    def __init__(self, name, email, phone, address, gender, dob, balance = 0):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.gender = gender
        self.dob = dob
        self.balance = balance

    # Returns the Data of the person.
    def get_data(self):
        return [
            ("Name", self.name),
            ("Phone Number", self.phone),
            ("Email Address", self.email),
            ("Balance", "You have to {} ₹{}".format("give" if self.balance < 0 else "receive", abs(self.balance))),
            ("Address", self.address),
            ("Gender", "Male" if self.gender == 0 else "Female" if self.gender == 1 else "Other"),
            ("Date of Birth", self.dob)
        ]

    # Returns a tuple having the name, phone and email of the person.
    def get_table_data(self):
        return self.name, self.phone, self.email

    # Retuns a frame containing the key-value pair of information of the person.
    def get_data_frame(self, window):
        frame = Frame(window, borderwidth=2, relief="raised")
        details_table = table.Treeview(frame)
        details_table["columns"] = ["parameter", "value"]
        details_table["show"] = "headings"
        index = 0
        for data in self.get_data():
            details_table.insert("", index, values=data)
            index += 1
        details_table.grid(row=0, column=0, columnspan=3)
        return frame

# Refreshes the table to reflect changes.
def refresh_table(people_table):
    for entry in people_table.get_children():
        people_table.delete(entry)
    with open("files/people.ltms", "rb") as file:
        people = []
        try:
            while True:
                person = pickle.load(file)
                people.append(person)
        except EOFError:
            pass
        people.sort(key=lambda person: person.name)
        index = 0
        for person in people:
            people_table.insert("", index, values=person.get_table_data(), tags=person.phone)
            index += 1

def search_person(people_table):
    person_phone = askstring("Search", "Enter Phone Number")
    if view_person(person_phone, people_table, True) == -1:
        dialog.showerror("Not Found", "There exists no person with the phone number {}".format(person_phone))

# This method takes in the main window of the program as a parameter and generates and returns the frame of the Person Module.
def get_frame(window):
    frame = Frame(window, name="people")

    # Create files.
    try:
        with open("files/people.ltms", "rb") as _, open("files/index.txt", "r") as _:
            pass
    except FileNotFoundError:
        if not os.path.exists("files"):
            os.mkdir("files")
        with open("files/people.ltms", "wb") as _, open("files/index.txt", "w") as _:
            pass

    # Table to display the people.
    people_table = table.Treeview(frame)
    people_table.grid(row=0, column=0, columnspan=4)
    people_table["columns"] = ["name", "phone", "email"]
    people_table["show"] = "headings"
    people_table.heading("name", text="Name")
    people_table.heading("email", text="Email Address")
    people_table.heading("phone", text="Phone Number")

    with open("files/people.ltms", "rb") as file:
        people = []
        try:
            while True:
                person = pickle.load(file)
                people.append(person)
        except EOFError:
            pass
        people.sort(key=lambda person: person.name)
        index = 0
        for person in people:
            people_table.insert("", index, values=person.get_table_data(), tags=person.phone)
            index += 1

    # Buttons to add, modify and delete a person.
    add_button = Button(frame, text="Add Person", command=lambda: add_person(people_table))
    search_button = Button(frame, text = "Search by Phone", command = lambda: search_person(people_table))
    view_button = Button(frame, text="View Details",
                         command=lambda: view_person(people_table.item(people_table.selection()[0]), people_table))
    delete_button = Button(frame, text="Delete",
                           command=lambda: delete_person(people_table.item(people_table.selection()[0]), people_table))

    add_button.grid(row=1, column=0)
    search_button.grid(row = 1, column = 1)
    view_button.grid(row=1, column = 2)
    delete_button.grid(row=1, column = 3)

    return frame

# Opens a window displaying the information and the recent transactions of the person.
def view_person(item, people_table, direct = False):
    person_phone = str(item["tags"][0]) if not direct else item
    with open("files/index.txt", "r") as file:
        while True:
            data = file.readline().split()
            if data == []:
                return -1
            if data[0] == person_phone:
                pos = int(data[1])
                break
    
    with open("files/people.ltms", "rb") as file:
        file.seek(pos)
        person = pickle.load(file)

    person_details_window = Tk()
    transactions_frame = Frame(person_details_window)

    trans_table = table.Treeview(transactions_frame)
    trans_table.grid(row = 0, column = 0, columnspan = 4)
    trans_table["columns"] = ["dot", "amount", "type", "des"]
    trans_table["show"] = "headings"
    trans_table.heading("amount", text = "Amount")
    trans_table.heading("type", text = "Type")
    trans_table.heading("dot", text = "Date Of Transaction")
    trans_table.heading("des", text = "Description")
    index = 0
    for trans in transaction.get_person_transactions(person):
        trans_table.insert("", index, values=(trans.trans_date, trans.amount, trans.trans_type, trans.description))
        index += 1
    transactions_frame.grid(row=0, column=0, columnspan=2)
    person_frame = person.get_data_frame(person_details_window)
    person_frame.grid(row=0, column=2, columnspan = 2)
    edit_button = Button(person_frame, text="Edit", command=lambda: add_person(people_table, person))
    edit_button.grid(row=1, column=0)
    clear_balance_button = Button(person_frame, text="Clear Balance", command=lambda: clear_balance(person, trans_table))
    clear_balance_button.grid(row=1, column=1)
    close_button = Button(person_frame, text="Close", command=person_details_window.destroy)
    close_button.grid(row=1, column=2)
    person_details_window.mainloop()

def clear_balance(person, trans_table):
    result = dialog.askquestion("Clear Balance", "Do you want to clear the balance of ₹{} of {}?".format(abs(person.balance), person.name),
                                icon='warning')
    if result == 'yes':
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        trans_id = Hash.md5((person.phone + str(-person.balance) + dt_string).encode()).hexdigest()
        trans = transaction.Transaction(trans_id, person.name, person.phone, "Clear Balance", abs(person.balance), dt_string, "Debit" if person.balance < 0 else "Credit")
        with open("files/transaction.ltms", "ab") as file:
            with open("files/index_transaction.txt", "a") as index:
                index.write(trans_id + " " + str(file.tell()) + "\n")
            pickle.dump(trans, file)
        change_balance(person.phone, -person.balance)
        trans_table.destroy()

# This method deletes the selected item from the people table.
def delete_person(item, people_table):
    delete_phone = item["tags"][0]
    delete_index = 0
    index = 0
    with open("files/people.ltms", "rb") as people_file, open("files/index.txt", "r") as index_file:
        people = []
        indices = []
        try:
            while True:
                person = pickle.load(people_file)
                entry = index_file.readline().split()
                if person.phone == delete_phone:
                    delete_index = index
                people.append(person)
                indices.append(entry)
                index += 1
        except EOFError:
            pass
    deleted_person = people.pop(delete_index)
    indices.pop(delete_index)
    result = dialog.askquestion("Delete Person", "Do you want to delete {} from contacts?".format(deleted_person.name),
                                icon='warning')
    if result == 'yes':
        with open("files/people.ltms", "wb") as people_file, open("files/index.txt", "w") as index_file:
            for i in range(len(people)):
                pickle.dump(people[i], people_file)
                index_file.write(" ".join(indices[i]) + "\n")
        dialog.showinfo("Deletion Successful",
                        "The person named {} has been deleted from the record.".format(deleted_person.name))
        refresh_table(people_table)

# Changes the balance of the person. TODO
def change_balance(person_phone, amount):
    people = []
    with open("files/people.ltms", "rb") as people_file:
        try:
            while True:
                person = pickle.load(people_file)
                if person_phone == person.phone:
                    person.balance += amount
                people.append(person)
        except EOFError:
            pass
    with open("files/people.ltms", "wb") as people_file:
        for person in people:
            pickle.dump(person, people_file)
    
# Returns the list of people.
def get_people_list():
    people_names = []
    with open("files/people.ltms", "rb") as f:    
        try:
            while True:
                person = pickle.load(f)
                people_names.append(person)
        except EOFError:
            pass
    people_names.sort(key=lambda person: person.name)
    return people_names

# This method is used to add a person.
def add_person(people_table, edit_person=None):
    # This method saves the person to the file.
    def save_person(edit):
        person_name = name_input.get()
        person_email = email_input.get()
        person_phone = phone_input.get()
        person_address = address_input.get("1.0", "end-1c")
        person_gender = gender_int.get()
        person_dob = dob_input.get()

        person = Person(person_name, person_email, person_phone, person_address, person_gender, person_dob)

        if person_name == "":
            dialog.showerror("Invalid Input", "Name cannot be empty.")
        elif not helper.isPhoneValid(person_phone):
            dialog.showerror("Invalid Input", "Invalid Phone Number.")
        elif not helper.isEmailValid(person_email):
            dialog.showerror("Invalid Input", "Invalid Email.")
        elif not helper.isDateValid(person_dob):
            dialog.showerror("Invalid Input", "Invalid Date of Birth.")
        elif edit:
            people = []
            with open("files/people.ltms", "rb") as people_file:
                try:
                    while True:
                        temp_person = pickle.load(people_file)
                        if temp_person.phone == edit_person.phone:
                            temp_person = person
                        people.append(temp_person)
                except EOFError:
                    pass
            with open("files/people.ltms", "wb") as people_file, open("files/index.txt", "w") as index_file:
                for temp in people:
                    index_file.write(temp.phone + " " + str(people_file.tell()) + "\n")
                    pickle.dump(temp, people_file)
            person_sub_window.destroy()
            refresh_table(people_table)
        else:
            alreadyExists = False
            with open("files/index.txt", "r") as file:
                for line in file:
                    if line.split()[0] == person_phone:
                        alreadyExists = True
                        dialog.showerror("Duplicate Entry", "Person already exists.")
            if not alreadyExists:
                with open("files/people.ltms", "ab") as file:
                    with open("files/index.txt", "a") as index:
                        index.write(person_phone + " " + str(file.tell()) + "\n")
                    pickle.dump(person, file)
            person_sub_window.destroy()
            refresh_table(people_table)

    person_sub_window = Tk()
    person_sub_window.title("Add Person")

    bottom_frame = Frame(person_sub_window)
    bottom_frame.pack(side=BOTTOM)

    save_button = Button(bottom_frame, text="Save", command=lambda: save_person(edit_person is not None))
    cancel_button = Button(bottom_frame, text="Cancel", command=person_sub_window.destroy)
    cancel_button.pack(side=RIGHT)
    save_button.pack(side=RIGHT)

    top_frame = Frame(person_sub_window)
    top_frame.pack(side=TOP)

    name = Label(top_frame, text="Name")
    name.grid(row=0, column=0)
    name_input = Entry(top_frame)
    name_input.insert(END, "" if edit_person is None else edit_person.name)
    name_input.grid(row=0, column=1)

    email = Label(top_frame, text="Email")
    email.grid(row=1, column=0)
    email_input = Entry(top_frame)
    email_input.insert(END, "" if edit_person is None else edit_person.email)
    email_input.grid(row=1, column=1)

    phone = Label(top_frame, text="Phone")
    phone.grid(row=2, column=0)
    phone_input = Entry(top_frame)
    phone_input.insert(END, "" if edit_person is None else edit_person.phone)
    phone_input.grid(row=2, column=1)

    address = Label(top_frame, text="Address")
    address.grid(row=3, column=0)
    address_input = Text(top_frame, width=50, height=4)
    address_input.insert(END, "" if edit_person is None else edit_person.address)
    address_input.grid(row=3, column=1)

    gender = Label(top_frame, text="Gender")
    gender.grid(row=4, column=0)
    gender_int = IntVar(top_frame)

    gender_frame = Frame(top_frame)
    male_radio = Radiobutton(gender_frame, text="Male", value=0, variable=gender_int)
    female_radio = Radiobutton(gender_frame, text="Female", value=1, variable=gender_int)
    other_radio = Radiobutton(gender_frame, text="Other", value=2, variable=gender_int)

    gender_value = 0 if edit_person is None else edit_person.gender

    if gender_value == 0:
        male_radio.select()
    elif gender_value == 1:
        female_radio.select()
    else:
        other_radio.select()

    male_radio.pack(side=LEFT)
    female_radio.pack(side=LEFT)
    other_radio.pack(side=LEFT)
    gender_frame.grid(row=4, column=1)

    dob = Label(top_frame, text="Date of Birth (DD/MM/YYYY)")
    dob.grid(row=5, column=0)
    dob_input = Entry(top_frame)
    dob_input.insert(END, "" if edit_person is None else edit_person.dob)
    dob_input.grid(row=5, column=1)

    person_sub_window.mainloop()
