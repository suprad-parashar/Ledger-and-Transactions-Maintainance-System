from tkinter import *
import webbrowser as web
import people

def open_developer_url(index):
    get_developer_URLs = lambda index: "https://www.linkedin.com/in/supradparashar/" if index == 1 else "https://www.linkedin.com/in/sandeep-n-s-6b3888165/"
    web.open(get_developer_URLs(index))

def add_menu(window):
    menu = Menu(window)
    window.config(menu = menu)

    files_menu = Menu(menu)
    help_menu = Menu(menu)

    files_menu.add_command(label = "Settings", command = print("#"))
    files_menu.add_separator()
    files_menu.add_command(label = "Exit", command = window.quit)

    # TODO: Fix opening of the urls at the start of the program. It should open only if the button is clicked.
    about_menu = Menu(help_menu)
    about_menu.add_command(label = "Sandeep N S", command = lambda: open_developer_url(0))
    about_menu.add_command(label = "Suprad S Parashar", command = lambda: open_developer_url(1))

    help_menu.add_cascade(label = "About", menu = about_menu)

    menu.add_cascade(label = "File", menu = files_menu)
    menu.add_cascade(label = "Help", menu = help_menu)

window = Tk()
window.title("Ledger and Transactions Maintainance System")
add_menu(window)
frame = people.get_frame(window)
frame.pack()
window.mainloop()