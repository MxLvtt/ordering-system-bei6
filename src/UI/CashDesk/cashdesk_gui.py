from tkinter import *
from add_order_view import AddOrderView
from content_panel import ContentPanel
from Templates.cbutton import CButton


class CashDeskGUI():
    def __init__(self):
        root = Tk()
        root.attributes('-fullscreen', True)
        root.wm_title("GUI Kasse")
        root.config(background="#696969")

        root.update()

        rootHeight = root.winfo_height()
        rootWidth = root.winfo_width()

        ## HEADER STUFF ##

        header = Frame(root, height=100, background="#EFEFEF")
        header.pack(side=TOP, expand=True, fill='x', padx=5, pady=5)

        def go_back_from_add_order_view():
            add_order_button.config(text="+")
            finish_order_button._hide()
            body.set_add_order_visibilty(False)

        def click_add_order_button():
            if body.is_add_order_visible():  # Clicked on "<"
                go_back_from_add_order_view()
            else:  # Clicked on "+"
                add_order_button.config(text="<")
                finish_order_button._show()
                body.set_add_order_visibilty(True)

        def click_finish_order_button():
            # TODO: Save order etc.
            go_back_from_add_order_view()

        add_order_button = CButton(
            parent=header,
            text="+",
            command=click_add_order_button,
            row=0, column=0
        )._show()

        finish_order_button = CButton(
            parent=header,
            text="✔",
            command=click_finish_order_button,
            fg="white", bg="darkgreen",
            row=0, column=1
        )._hide()

        # add_order_button = Button(header, command=click_add_order_button, width=3, height=1, text="+",fg="black",bg="white",font=helv36)
        # add_order_button.grid(row=0,column=0)

        # finish_order_button = Button(header, command=click_finish_order_button, width=3, height=1, text="✔",fg="white",bg="darkgreen",font=helv36)
        # finish_order_button.grid(row=0,column=1)
        # finish_order_button.grid_remove()

        ## FOOTER STUFF ##

        footer = Frame(root, height=100, background="#EFEFEF")
        footer.pack(side=BOTTOM, expand=True, fill='x', padx=5, pady=5)

        CButton( # EXIT BUTTON
            parent=footer,
            text="x",
            command=exit,
            fg="white", bg="darkred",
            row=0, column=0
        )._show()

        ## BODY STUFF ##

        body = ContentPanel(root, height=rootHeight)
        body.pack(side=TOP, expand=True, fill='both', padx=5)

        # TODO:
        # The content panel should contain all the different views (= classes that inherit from Frame)
        # and the corresponding methods to show / hide each of them.
        # For this, the content panel has to have a grid inside.

        mainloop()
