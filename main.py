from tkinter import *
import webbrowser as web
import people

# This method adds the menu to the program.
def add_menu(window):
    menu = Menu(window)
    window.config(menu = menu)

    files_menu = Menu(menu)
    help_menu = Menu(menu)

    files_menu.add_command(label = "Settings", command = print("#"))
    files_menu.add_separator()
    files_menu.add_command(label = "Exit", command = window.quit)

    about_menu = Menu(help_menu)
    about_menu.add_command(label = "Sandeep N S", command = lambda: web.open("https://www.linkedin.com/in/sandeep-n-s-6b3888165/"))
    about_menu.add_command(label = "Suprad S Parashar", command = lambda: web.open("https://www.linkedin.com/in/supradparashar/"))

    help_menu.add_cascade(label = "About", menu = about_menu)

    menu.add_cascade(label = "File", menu = files_menu)
    menu.add_cascade(label = "Help", menu = help_menu)

# Main Login of the function

window = Tk()
window.title("Ledger and Transactions Maintainance System")
add_menu(window)
frame = people.get_frame(window)
frame.pack()
window.mainloop()