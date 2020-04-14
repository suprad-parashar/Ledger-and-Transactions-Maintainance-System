from tkinter import *
import tkinter.ttk as table
from datetime import datetime
import tkinter.messagebox as dialog
import people
import transaction
import helper

# TODO: Radio Button Gets selected upon Hovering.
# TODO: Add Balance to the Passbook

pre_frame = 0

def get_frame(window):
    frame = Frame(window, name="passbook")

    passbook_window = Tk()
    passbook_window.title("Generating Balance Sheet")

    top_frame = Frame(passbook_window)
    top_frame.pack(side=TOP)

    bottom_frame = Frame(passbook_window)
    bottom_frame.pack(side=BOTTOM)

    n_label = Label(bottom_frame, text="Last Transaction")
    n_entry = Entry(bottom_frame)
    people_choices = table.Treeview(bottom_frame)
    from_label = Label(bottom_frame, text="FROM :(dd/mm/yyyy)")
    from_entry = Entry(bottom_frame)
    to_label = Label(bottom_frame, text="TO :")
    to_entry = Entry(bottom_frame)
    ok_button = Button(bottom_frame, text="OK")

    def bottom(radio_button_var):
        global pre_frame
        clear_frame(pre_frame)
        if radio_button_var == 1:
            n_label.grid(row=1, column=1)
            n_entry.grid(row=1, column=2)
            pre_frame = 1
            ok_button.config(command=lambda: display(n=n_entry.get()), text="OK", width=10, height=1)
            ok_button.grid(row=2, column=2)
        elif radio_button_var == 2:
            people_choices.grid(row=2, column=0, columnspan=2)
            people_choices["columns"] = ["name", "phone"]
            people_choices["show"] = "headings"
            people_choices.heading("name", text="Name")
            people_choices.heading("phone", text="Phone")
            index = 0
            for person in people.PEOPLE:
                people_choices.insert("", index, values=(person.name, person.phone), tags=person.id)
                index += 1
            ok_button.config(
                command=lambda: display(name=people_choices.item(people_choices.selection()[0])['values'][0]),
                text="OK", width=10, height=1)
            ok_button.grid(row=3, column=1)
            pre_frame = 2

        elif radio_button_var == 3:
            from_label.grid(row=1, column=1)
            from_entry.grid(row=1, column=2)
            to_label.grid(row=2, column=1)
            to_entry.grid(row=2, column=2)
            ok_button.config(command=lambda: display(from_date=from_entry.get(), to_date=to_entry.get()), width=10,
                             height=1)
            ok_button.grid(row=3, column=1)
            pre_frame = 3

    def clear_frame(pre_frame):
        if pre_frame == 0:
            pass
        elif pre_frame == 1:
            n_label.grid_forget()
            n_entry.grid_forget()
            ok_button.grid_forget()
        elif pre_frame == 2:
            people_choices.grid_forget()
            ok_button.grid_forget()
        elif pre_frame == 3:
            from_label.grid_forget()
            to_entry.grid_forget()
            from_entry.grid_forget()
            to_label.grid_forget()
            ok_button.grid_forget()

    selection_frame = Frame(top_frame)
    selection = IntVar(selection_frame)
    selection.set(1)
    last_n = Radiobutton(selection_frame, text="Last N Transactions", value=1, variable=selection,
                         command=lambda: bottom(1))
    by_person = Radiobutton(selection_frame, text="By Person", value=2, variable=selection, command=lambda: bottom(2))
    by_date = Radiobutton(selection_frame, text="By Date", value=3, variable=selection, command=lambda: bottom(3))

    last_n.pack(side=LEFT)
    by_person.pack(side=LEFT)
    by_date.pack(side=LEFT)
    selection_frame.grid(row=0, column=1)

    return frame


def display(n=None, name=None, from_date=None, to_date=None):
    passbook_sub_window = Tk()
    passbook_sub_window.title("Passbook")

    passbook_table = table.Treeview(passbook_sub_window)
    passbook_table.grid(row=0, column=0, columnspan=6)
    passbook_table["columns"] = ["date", "trans_id", "person_name", "withdrawal", "deposits", "balance"]
    passbook_table["show"] = "headings"
    passbook_table.heading("date", text="Date")
    passbook_table.heading("trans_id", text="Transaction Id")
    passbook_table.heading("person_name", text="Name")
    passbook_table.heading("withdrawal", text="Withdrawals")
    passbook_table.heading("deposits", text="Deposits")
    passbook_table.heading("balance", text="Balance")
    if n != None:
        index = 0
        for trans in transaction.TRANSACTIONS:
            if index >= int(n) :
                break
            if trans.type == "Debit":
                passbook_table.insert("", index,
                                      values=(trans.date, trans.id, trans.person_name, trans.amount, " ", " "))
                index += 1
            else:
                passbook_table.insert("", index,
                                      values=(trans.date, trans.id, trans.person_name, " ", trans.amount, " "))
                index += 1
        passbook_sub_window.mainloop()

    elif name != None:
        index = 0
        for trans in transaction.TRANSACTIONS:
            if trans.person_name == name:
                if trans.type == "Debit":
                    passbook_table.insert("", index,
                                          values=(trans.date, trans.id, trans.person_name, trans.amount, " ", " "))
                    index += 1
                else:
                    passbook_table.insert("", index,
                                          values=(trans.date, trans.id, trans.person_name, " ", trans.amount, " "))
                    index += 1
        passbook_sub_window.mainloop()

    elif from_date != None and to_date != None:

        if helper.isDateValid(from_date) and helper.isDateValid(to_date):
            from_date1 = datetime.strptime(from_date, '%d/%m/%Y').date()
            to_date1 = datetime.strptime(to_date, '%d/%m/%Y').date()
            if from_date1 <= to_date1 and to_date1 <= datetime.now().date() and from_date1 <= datetime.now().date():
                index = 0
                for trans in transaction.TRANSACTIONS:
                    d = datetime.strptime(trans.date, "%d/%m/%Y %H:%M:%S").date()
                    if from_date1 <= d <= to_date1:
                        if trans.type == "Debit":
                            passbook_table.insert("", index, values=(
                                trans.date, trans.id, trans.person_name, trans.amount, " ", " "))
                        else:
                            passbook_table.insert("", index, values=(
                                trans.date, trans.id, trans.person_name, " ", trans.amount, " "))
                        index += 1
            else:
                dialog.showinfo("Invalid Data", "Invalid Date Entered")
                passbook_sub_window.destroy()
        else:
            dialog.showinfo("Invalid Data", "Invalid Date Enter ! Please Enter in (dd/mm/yyyy) format")
            passbook_sub_window.destroy()
