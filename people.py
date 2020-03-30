from tkinter import *
import tkinter.messagebox as dialog
import re as regex
import hashlib as Hash
import pickle

class Person:
    def __init__(self, identification_hash, name, email, phone, address, gender, dob):
        self.id = identification_hash
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.gender = gender
        self.dob = dob

def get_frame(window):
    frame = Frame(window)

    add_button = Button(frame, text = "Add Person", command = add_person)
    edit_button = Button(frame, text = "Edit Person")
    delete_button = Button(frame, text = "Delete Person")

    add_button.grid(row = 0, column = 0)
    edit_button.grid(row = 0, column = 1)
    delete_button.grid(row = 0, column = 2)

    return frame

isEmailValid = lambda email: regex.search('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email)

def isDateValid(date):
    isLeapYear = lambda year: (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
    try:
        dates = list(map(int, date.split("/")))
        if dates[1] == 2:
            if isLeapYear(dates[2]) and dates[0] in range(1, 30):
                return True
            elif (not isLeapYear) and dates[0] in range(1, 29):
                return True
            else:
                return False
        elif dates[1] in [1, 3, 5, 7, 8, 10, 12] and dates[0] in range(1, 32):
            return True
        elif dates[1] not in [1, 3, 5, 7, 8, 10, 12] and dates[0] in range(1, 31):
            return True
        else:
            return False
    except:
        return False

def isPhoneValid(phone):
    if phone[0] not in [6, 7, 8, 9]:
        return False
    elif len(phone) != 10:
        return False
    else:
        for c in phone:
            if not c.isdigit():
                return False
        return True

def add_person():
    def save_person():
        person_name = name_input.get()
        person_email = email_input.get()
        person_phone = phone_input.get()    
        person_address = address_input.get("1.0", "end-1c")
        person_gender = gender_int.get()
        person_dob = dob_input.get()
        if person_name == "":
            dialog.showerror("Invalid Input", "Name cannot be empty.")
        elif not isEmailValid(person_email):
            dialog.showerror("Invalid Input", "Invalid Email.")
        elif isPhoneValid(person_phone):
            dialog.showerror("Invalid Input", "Invalid Phone Number.")
        elif not isDateValid(person_dob):
            dialog.showerror("Invalid Input", "Invalid Date of Birth.")
        else:
            person_id = Hash.md5((person_name + person_email).encode()).hexdigest()
            with open("people.ltms", "ab") as file:
                with open("index.txt", "a") as index:
                    index.write(person_id + " " + str(file.tell()) + "\n")
                person = Person(person_id, person_name, person_email, person_phone, person_address, person_gender, person_dob)
                pickle.dump(person, file)

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