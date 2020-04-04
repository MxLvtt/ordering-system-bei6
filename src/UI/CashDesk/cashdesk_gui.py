from tkinter import *
from add_order_view import AddOrderView

class CashDeskGUI():
    def __init__(self):
        root = Tk()
        root.attributes('-fullscreen', True)
        root.wm_title("GUI Kasse")
        root.config(background="#FFFFFF")

        root.update()

        rootHeight = root.winfo_height()
        rootWidth = root.winfo_width()

        headerHeight = 60
        footerHeight = 60
        bodyHeight = rootHeight-headerHeight-footerHeight

        header = Frame(root, width=rootWidth-10, height=footerHeight-10, background="#696969")
        header.grid(row=0, column=0, padx=5, pady=5)
        header.grid_propagate(0)

        body = AddOrderView(root, rootWidth, bodyHeight, 5)
        body.grid(row=1, column=0)
        body.unhide_frame()

        body2 = AddOrderView(root, rootWidth, bodyHeight, 5, "#FF0000")
        body2.grid(row=1, column=0)
        body2.hide_frame()

        footer = Frame(root, width=rootWidth-10, height=footerHeight-10, background="#696969")
        footer.grid(row=2, column=0, padx=5, pady=5)
        footer.grid_propagate(0)

        self.state = True

        def switch_content():
            if self.state:
                body2.unhide_frame()
                body.hide_frame()
                button1.config(text="<")
                self.state = False
            else:
                body.unhide_frame()
                body2.hide_frame()
                button1.config(text="+")
                self.state = True

        pixelVirtual = PhotoImage(width=1, height=1)

        button1 = Button(header, text ="+", command = switch_content, image=pixelVirtual, width=43, height=43, compound="c")
        button1.grid(row=0, column=0)

        button2 = Button(header, text ="x", command = exit, image=pixelVirtual, width=43, height=43, compound="c")
        button2.grid(row=0, column=1)

        # leftFrame = Frame(root, width=lF_width-10, height=rootHeight-10, background="darkgray")
        # leftFrame.grid(row=0, column=0, padx=5, pady=5)
        # leftFrame.grid_propagate(0) # Ensures that the frame doesn't resize when widgets are added

        # leftLabel1 = Label(leftFrame, text="Platzhalter Text")
        # leftLabel1.grid(row=0, column=0, padx=10, pady=3)
        # leftLabel2 = Label(leftFrame, text="Dies ist ein Text\nmit mehreren Zeilen.")
        # leftLabel2.grid(row=0, column=1, columnspan=2, padx=10, pady=3)

        # leftLabel1 = Label(leftFrame, text="Platzhalter Text 2")
        # leftLabel1.grid(row=1, column=0, padx=10, pady=3)
        # leftLabel2 = Label(leftFrame, text="Dies ist ein Text 2")
        # leftLabel2.grid(row=1, column=1, padx=10, pady=3)
        # leftLabel2 = Label(leftFrame, text="Dies ist ein Text 3")
        # leftLabel2.grid(row=1, column=2, padx=10, pady=3)

        mainloop()
