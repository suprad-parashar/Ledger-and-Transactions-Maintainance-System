from tkinter import *
import tkinter.messagebox as dialog
import tkinter.ttk as table
import hashlib as Hash
import pickle
import os
import helper
import transaction


# TODO: Fix bug. Quit has to be pressed multiple times to work.

# A Person class to store the deatils of a person.
class Person:
    # The constructor of the class.
    def __init__(self, identification_hash, name, email, phone, address, gender, dob):
        self.id = identification_hash
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.gender = gender
        self.dob = dob

    # Returns the Data of the person.
    def get_data(self):
        return [
            ("Name", self.name),
            ("Email Address", self.email),
            ("Phone Number", self.phone),
            ("Address", self.address),
            ("Gender", "Male" if self.gender == 0 else "Female" if self.gender == 1 else "Other"),
            ("Date of Birth", self.dob)
        ]

    def get_table_data(self):
        return self.name, self.email, self.phone

    def get_data_frame(self, window):
        frame = Frame(window, borderwidth=2, relief="raised")
        details_table = table.Treeview(frame)
        details_table["columns"] = ["parameter", "value"]
        details_table["show"] = "headings"
        index = 0
        for data in self.get_data():
            details_table.insert("", index, values=data)
            index += 1
        details_table.grid(row=0, column=0, columnspan=2)
        return frame


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
            people_table.insert("", index, values=person.get_table_data(), tags=person.id)
            index += 1


# This method takes in the main window of the program as a parameter and generates and returns the frame of the Person Module.
def get_frame(window):
    frame = Frame(window, name="people")

    # Create files.
    try:
        with open("files/people.ltms", "rb") as _, open("files/index.txt", "r") as _:
            pass
    except FileNotFoundError:
        os.mkdir("files")
        with open("files/people.ltms", "wb") as _, open("files/index.txt", "w") as _:
            pass

    # Table to display the people.
    people_table = table.Treeview(frame)
    people_table.grid(row=0, column=0, columnspan=3)
    people_table["columns"] = ["name", "email", "phone"]
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
            people_table.insert("", index, values=person.get_table_data(), tags=person.id)
            index += 1

    # Buttons to add, modify and delete a person.
    add_button = Button(frame, text="Add Person", command=lambda: add_person(people_table))
    view_button = Button(frame, text="View Details",
                         command=lambda: view_person(people_table.item(people_table.selection()[0]), people_table))
    delete_button = Button(frame, text="Delete",
                           command=lambda: delete_person(people_table.item(people_table.selection()[0]), people_table))

    add_button.grid(row=1, column=0)
    view_button.grid(row=1, column=1)
    delete_button.grid(row=1, column=2)

    return frame


def view_person(item, people_table):
    person_id = item["tags"][0]
    with open("files/people.ltms", "rb") as file:
        while True:
            person = pickle.load(file)
            if person.id == person_id:
                break
        person_details_window = Tk()
        transactions_frame = Frame(person_details_window)

        trans_table = table.Treeview(transactions_frame)
        trans_table.grid(row = 0, column = 0, columnspan = 6)
        trans_table["columns"] = ["name", "amount", "type", "des", "dot"]
        trans_table["show"] = "headings"
        trans_table.heading("name", text = "Name")
        trans_table.heading("amount", text = "Amount")
        trans_table.heading("type", text = "Type")
        trans_table.heading("dot", text = "Date Of Transaction")
        trans_table.heading("des", text = "Description")
        index = 0
        for trans in transaction.get_person_transactions(person):
            trans_table.insert("", index, values=(trans.sender_name, trans.amount, trans.trans_type, trans.description, trans.trans_date))
            index += 1

        transactions_frame.grid(row=0, column=0, columnspan=2)
        person_frame = person.get_data_frame(person_details_window)
        person_frame.grid(row=0, column=2)
        edit_button = Button(person_frame, text="Edit", command=lambda: add_person(people_table, person))
        edit_button.grid(row=1, column=0)
        close_button = Button(person_frame, text="Close", command=person_details_window.destroy)
        close_button.grid(row=1, column=1)
        person_details_window.mainloop()


# This method deletes the selected item from the people table.
def delete_person(item, people_table):
    delete_id = item["tags"][0]
    delete_index = 0
    index = 0
    with open("files/people.ltms", "rb") as people_file, open("files/index.txt", "r") as index_file:
        people = []
        indices = []
        try:
            while True:
                person = pickle.load(people_file)
                entry = index_file.readline().split()
                if person.id == delete_id:
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

        person_id = Hash.md5((person_name + person_email).lower().encode()).hexdigest()
        person = Person(person_id, person_name, person_email, person_phone, person_address, person_gender, person_dob)

        if person_name == "":
            dialog.showerror("Invalid Input", "Name cannot be empty.")
        elif not helper.isEmailValid(person_email):
            dialog.showerror("Invalid Input", "Invalid Email.")
        elif not helper.isPhoneValid(person_phone):
            dialog.showerror("Invalid Input", "Invalid Phone Number.")
        elif not helper.isDateValid(person_dob):
            dialog.showerror("Invalid Input", "Invalid Date of Birth.")
        elif edit:
            people = []
            with open("files/people.ltms", "rb") as people_file:
                try:
                    while True:
                        temp_person = pickle.load(people_file)
                        if temp_person.id == edit_person.id:
                            temp_person = person
                        people.append(temp_person)
                except EOFError:
                    pass
            with open("files/people.ltms", "wb") as people_file, open("files/index.txt", "w") as index_file:
                for temp in people:
                    index_file.write(temp.id + " " + str(people_file.tell()) + "\n")
                    pickle.dump(temp, people_file)
            person_sub_window.destroy()
            refresh_table(people_table)
        else:
            alreadyExists = False
            with open("files/index.txt", "r") as file:
                for line in file:
                    if line.split()[0] == person_id:
                        alreadyExists = True
                        dialog.showerror("Duplicate Entry", "Person already exists.")
            if not alreadyExists:
                with open("files/people.ltms", "ab") as file:
                    with open("files/index.txt", "a") as index:
                        index.write(person_id + " " + str(file.tell()) + "\n")
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
