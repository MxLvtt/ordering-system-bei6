from tkinter import *
from tkinter import font as tkFont
from add_order_view import AddOrderView
from content_panel import ContentPanel

class CashDeskGUI():
    def __init__(self):
        root = Tk()
        root.attributes('-fullscreen', True)
        root.wm_title("GUI Kasse")
        root.config(background="#696969")

        root.update()

        rootHeight = root.winfo_height()
        rootWidth = root.winfo_width()

        helv36 = tkFont.Font(family='Helvetica', size=26, weight=tkFont.BOLD)

        ## HEADER STUFF ##

        header = Frame(root, height=100, background="#EFEFEF")
        header.pack(side=TOP, expand=True, fill='x', padx=5, pady=5)

        def click_add_order_button():
            if body.is_add_order_visible():
                add_order_button.config(text="<")
                body.set_add_order_visibilty(False)
            else:
                add_order_button.config(text="+")
                body.set_add_order_visibilty(True)

        add_order_button = Button(header, command=click_add_order_button, width=3, height=1, text="+",fg="black",bg="white",font=helv36)
        add_order_button.grid(row=0,column=0)

        ## FOOTER STUFF ##

        footer = Frame(root, height=100, background="#EFEFEF")
        footer.pack(side=BOTTOM, expand=True, fill='x', padx=5, pady=5)

        exit_button = Button(footer, command=exit, width=3, height=1, text="x",fg="white",bg="darkred",font=helv36)
        exit_button.grid(row=0,column=0)

        ## BODY STUFF ##

        body = ContentPanel(root, height=rootHeight)
        body.pack(side=TOP, expand=True, fill='both', padx=5)

        # TODO:
        # The content panel should contain all the different views (= classes that inherit from Frame)
        # and the corresponding methods to show / hide each of them.
        # For this, the content panel has to have a grid inside.

        mainloop()
