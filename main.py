from tkinter import *
import webbrowser as web
import people
import dashboard
import transaction
import passbook


# todo: Testing the change_frame method

def change_frame(frame, name, prev="None"):
    global window, people_button, transactions_button, passbook_button
    frame.destroy()
    if name == "Dashboard":
        frame = dashboard.get_frame(window)
        frame.pack(side=TOP)
        if prev == "People" or prev == "Transaction":
            people_button.config(text="People", command=lambda: change_frame(frame, "People", "Dashboard"))
            transactions_button.config(text="Transaction",
                                       command=lambda: change_frame(frame, "Transaction", "Dashboard"))
            people_button.pack(side=LEFT)
            transactions_button.pack(side=LEFT)

    elif name == "People":
        if prev == "Transaction":
            people_button.config(text="Dashboard", command=lambda: change_frame(frame, "Dashboard", "People"))
            transactions_button.config(text="Transaction", command=lambda: change_frame(frame, "Transaction", "People"))
        if prev == "Dashboard":
            people_button.config(text="Dashboard", command=lambda: change_frame(frame, "Dashboard", "People"))
            transactions_button.config(command=lambda: change_frame(frame, "Transaction", "People"))
        frame = people.get_frame(window)
        frame.pack(side=TOP)

    elif name == "Transaction":
        if prev == "People":
            transactions_button.config(text="Dashboard",
                                       command=lambda: change_frame(frame, "Dashboard", "Transaction"))
            people_button.config(text="People", command=lambda: change_frame(frame, "People", "Transaction"))
        if prev == "Dashboard":
            transactions_button.config(text="Dashboard",
                                       command=lambda: change_frame(frame, "Dashboard", "Transaction"))
            people_button.config(command=lambda: change_frame(frame, "People", "Transaction"))
        frame = transaction.get_frame(window)
        frame.pack(side=TOP)

    elif name == "Passbook":
        passbook_button.config(text="Passbook", command=lambda: change_frame(frame, "Passbook", "Passbook"))
        frame = passbook.get_frame(window)
        frame.pack(side=TOP)


# This method adds the menu to the program.
def add_menu(window):
    menu = Menu(window)
    window.config(menu=menu)

    files_menu = Menu(menu)
    help_menu = Menu(menu)

    files_menu.add_command(label="Settings", command=print("#"))
    files_menu.add_separator()
    files_menu.add_command(label="Exit", command=window.quit)

    about_menu = Menu(help_menu)
    about_menu.add_command(label="Sandeep N S",
                           command=lambda: web.open("https://www.linkedin.com/in/sandeep-n-s-6b3888165/"))
    about_menu.add_command(label="Suprad S Parashar",
                           command=lambda: web.open("https://www.linkedin.com/in/supradparashar/"))

    help_menu.add_cascade(label="About", menu=about_menu)

    menu.add_cascade(label="File", menu=files_menu)
    menu.add_cascade(label="Help", menu=help_menu)


# Main Logic of the function
window = Tk()
window.title("Ledger and Transactions Maintenance System")
add_menu(window)
frame = dashboard.get_frame(window)
frame.pack(side=TOP)
navigation_frame = Frame(window)
people_button = Button(navigation_frame, text="People", command=lambda: change_frame(frame, "People", "Dashboard"))
transactions_button = Button(navigation_frame, text="Transactions",
                             command=lambda: change_frame(frame, "Transaction", "Dashboard"))
passbook_button = Button(navigation_frame, text="Passbook",
                         command=lambda: change_frame(frame, "Passbook", "Dashboard"))
quit_button = Button(navigation_frame, text="Quit", command=window.quit)
people_button.pack(side=LEFT)
transactions_button.pack(side=LEFT)
passbook_button.pack(side=LEFT)
quit_button.pack(side=LEFT)
navigation_frame.pack(side=BOTTOM)
window.mainloop()
