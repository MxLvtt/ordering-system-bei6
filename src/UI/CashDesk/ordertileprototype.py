from tkinter import *
from tkinter import font as tkFont

class OrderTileGUI(Frame):
    COLORS=[
        "#A2ABAD", # gray-ish; Open
        "#BEF291", # green-ish; Prepared
        "#FFE48C", # yellow-ish; Changed
        "#DD726C" # red-ish; Canceled
    ]

    def __init__(
        self,
        parent,
        row,
        column,
        padx=(5,5),
        pady=(5,5),
        width=450,
        height=660,
        background="#A2ABAD"
    ):
        super().__init__(
            master=parent,
            width=width,
            height=height,
            bg=background
        )

        helv18 = tkFont.Font(family='Helvetica', size=18)

        self.grid(row=row,column=column,padx=padx,pady=pady)
        self.pack_propagate(0)

        self._header_frame: Frame = Frame(master=self, bg="green")
        self._header_frame.pack(side=TOP, fill='x', padx=5, pady=5)

        self._order_number_label: Label = Label(master=self._header_frame, text="#123", font=helv18)
        self._order_number_label.pack(side=LEFT)

        self._timestamp_label: Label = Label(master=self._header_frame, text="20:23:43", font=helv18)
        self._timestamp_label.pack(side=RIGHT)

        self._body_frame: Frame = Frame(master=self, bg="blue")
        self._body_frame.pack(side=TOP, expand=1, fill='both', padx=5)

        self._footer_frame: Frame = Frame(master=self, bg="red")
        self._footer_frame.pack(side=BOTTOM, fill='x', padx=5, pady=5)

        self._order_type_label: Label = Label(master=self._footer_frame, text="Eat in", font=helv18)
        self._order_type_label.pack(side=LEFT)

        self._order_status_label: Label = Label(master=self._footer_frame, text="O", font=helv18)
        self._order_status_label.pack(side=RIGHT)

    def test_func(self) -> (int, str):
        return (0, "123")

root = Tk()

OrderTileGUI(parent=root, row=0, column=0, padx=10, pady=10)

mainloop()
