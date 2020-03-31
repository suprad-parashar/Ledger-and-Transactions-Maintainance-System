from tkinter import *
import tkinter.messagebox as dialog
import tkinter.ttk as table
import hashlib as Hash
import pickle
import validate

# A Person class to store the deatils of a person.
class Person:
    def __init__(self, identification_hash, name, email, phone, address, gender, dob):
        self.id = identification_hash
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.gender = gender
        self.dob = dob

# This method takes in the main window of the program as a parameter and generates and returns the frame of the Person Module.
def get_frame(window):
    frame = Frame(window)

    # Table to display the people.
    people_table = table.Treeview(frame)
    people_table.grid(row = 0, column = 0, columnspan = 3)
    people_table["columns"] = ["name", "email", "phone"]
    people_table["show"] = "headings"
    people_table.heading("name", text = "Name")
    people_table.heading("email", text = "Email Address")
    people_table.heading("phone", text = "Phone Number")

    try:
        with open("files/people.ltms", "rb") as file:
            index = 0
            while True:
                person = pickle.load(file)
                people_table.insert("", index, values = (person.name, person.email, person.phone))
                index += 1
    except EOFError:
        pass
    except FileNotFoundError:
        with open("files/people.ltms", "wb") as file:
            pass

    # Buttons to add, modify and delete a person.
    add_button = Button(frame, text = "Add Person", command = add_person)
    edit_button = Button(frame, text = "Edit Person")
    delete_button = Button(frame, text = "Delete Person")

    add_button.grid(row = 1, column = 0)
    edit_button.grid(row = 1, column = 1)
    delete_button.grid(row = 1, column = 2)

    return frame

# This method is used to add a person.
def add_person():
    # This method saves the person to the file.
    def save_person():
        person_name = name_input.get()
        person_email = email_input.get()
        person_phone = phone_input.get()    
        person_address = address_input.get("1.0", "end-1c")
        person_gender = gender_int.get()
        person_dob = dob_input.get()
        if person_name == "":
            dialog.showerror("Invalid Input", "Name cannot be empty.")
        elif not validate.isEmailValid(person_email):
            dialog.showerror("Invalid Input", "Invalid Email.")
        elif not validate.isPhoneValid(person_phone):
            dialog.showerror("Invalid Input", "Invalid Phone Number.")
        elif not validate.isDateValid(person_dob):
            dialog.showerror("Invalid Input", "Invalid Date of Birth.")
        else:
            person_id = Hash.md5((person_name + person_email).encode()).hexdigest()
            with open("files/people.ltms", "ab") as file:
                with open("files/index.txt", "a") as index:
                    index.write(person_id + " " + str(file.tell()) + "\n")
                person = Person(person_id, person_name, person_email, person_phone, person_address, person_gender, person_dob)
                pickle.dump(person, file)
            person_sub_window.destroy()

    person_sub_window = Tk()
    person_sub_window.title("Add Person")

    bottom_frame = Frame(person_sub_window)
    bottom_frame.pack(side = BOTTOM)

    save_button = Button(bottom_frame, text = "Save", command = save_person)
    cancel_button = Button(bottom_frame, text = "Cancel", command = person_sub_window.destroy)
    cancel_button.pack(side = RIGHT)
    save_button.pack(side = RIGHT)

    top_frame = Frame(person_sub_window)
    top_frame.pack(side = TOP)

    name = Label(top_frame, text = "Name")
    name.grid(row = 0, column = 0)
    name_input = Entry(top_frame)
    name_input.grid(row = 0, column = 1)

    email = Label(top_frame, text = "Email")
    email.grid(row = 1, column = 0)
    email_input = Entry(top_frame)
    email_input.grid(row = 1, column = 1)

    phone = Label(top_frame, text = "Phone")
    phone.grid(row = 2, column = 0)
    phone_input = Entry(top_frame)
    phone_input.grid(row = 2, column = 1)

    address = Label(top_frame, text = "Address")
    address.grid(row = 3, column = 0)
    address_input = Text(top_frame, width = 50, height = 4)
    address_input.grid(row = 3, column = 1)

    gender = Label(top_frame, text = "Gender")
    gender.grid(row = 4, column = 0)
    gender_int = IntVar(top_frame)

    gender_frame = Frame(top_frame)
    male_radio = Radiobutton(gender_frame, text = "Male", value = 0, variable = gender_int)
    female_radio = Radiobutton(gender_frame, text = "Female", value = 1, variable = gender_int)
    other_radio = Radiobutton(gender_frame, text = "Other", value = 2, variable = gender_int)
    male_radio.pack(side = LEFT)
    female_radio.pack(side = LEFT)
    other_radio.pack(side = LEFT)
    gender_frame.grid(row = 4, column = 1)

    dob = Label(top_frame, text = "Date of Birth (DD/MM/YYYY)")
    dob.grid(row = 5, column = 0)
    dob_input = Entry(top_frame)
    dob_input.grid(row = 5, column = 1)
    
    person_sub_window.mainloop()