from tkinter import *
# Pickle module is used to read and write objects into a file in binary mode.
# import pickle

class Person:
    def __init__(self, name, email, phone, address, gender, dob):
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

def writeName(text):
    print(text)

def add_person():
    person_sub_window = Tk()
    entry_var = StringVar()
    person_sub_window.title("Add Person")

    bottom_frame = Frame(person_sub_window)
    bottom_frame.pack(side = BOTTOM)

    save_button = Button(bottom_frame, text = "Save", command = writeName(entry_var.get()))
    # save_button.bind("<Button-1>", )
    cancel_button = Button(bottom_frame, text = "Cancel", command = person_sub_window.quit)
    cancel_button.pack(side = RIGHT)
    save_button.pack(side = RIGHT)

    top_frame = Frame(person_sub_window)
    top_frame.pack(side = TOP)

    name = Label(top_frame, text = "Name", textvariable = entry_var)
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
    gender_frame = Frame(top_frame)
    male_radio = Radiobutton(gender_frame, text = "Male")
    female_radio = Radiobutton(gender_frame, text = "Female")
    other_radio = Radiobutton(gender_frame, text = "Other")
    male_radio.pack(side = LEFT)
    female_radio.pack(side = LEFT)
    other_radio.pack(side = LEFT)
    gender_frame.grid(row = 4, column = 1)

    dob = Label(top_frame, text = "Date of Birth (DD/MM/YYYY)")
    dob.grid(row = 5, column = 0)
    dob_input = Entry(top_frame)
    dob_input.grid(row = 5, column = 1)
    
    person_sub_window.mainloop()