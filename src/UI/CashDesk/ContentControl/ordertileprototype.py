from tkinter import *
from tkinter import font as tkFont
from random import *

class OrderTileGUI(Frame):
    COLORS=[
        "#D6D6D1", # "#A2ABAD", # gray-ish; Open
        "#BEF291", # green-ish; Prepared
        "#FFE48C", # yellow-ish; Changed
        "#DD726C" # red-ish; Canceled
    ]

    LIGHT_GRAY = "#D6D6D1"
    DARK_GRAY = "#ADADA9"

    I = 1

    def __init__(
        self,
        parent,
        row,
        column,
        padx=(10,5),
        pady=(10,10),
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

        num = int(random() * 10 + 1)
        num = OrderTileGUI.I

        OrderTileGUI.I = OrderTileGUI.I + int(random() + 1)

        minute = int(random() * 20 + 30)
        seconds = int(random() * 30 + 15)

        t = "Eat in"

        r = random()

        if r > 0.5:
            t = "Takeaway"

        state = "Canceled"
        s = 3

        r = random()

        if r > 0.75:
            state = "Open"
            s = 0
        elif r > 0.5:
            state = "Prepared"
            s = 1
        elif r > 0.25:
            state = "Changed"
            s = 2

        self.grid(row=row,column=column,padx=padx,pady=pady,sticky='N')
        self.pack_propagate(0)

        self._header_frame: Frame = Frame(master=self, bg=self.LIGHT_GRAY)
        self._header_frame.pack(side=TOP, fill='x')

        self._order_number_label: Label = Label(master=self._header_frame, text=f"#{num}", font=helv18, bg=self.LIGHT_GRAY)
        self._order_number_label.pack(side=LEFT, padx=5, pady=5)

        self._timestamp_label: Label = Label(master=self._header_frame, text=f"20:{minute}:{seconds}", font=helv18, bg=self.LIGHT_GRAY)
        self._timestamp_label.pack(side=RIGHT, padx=5, pady=5)

        self._body_frame: Frame = Frame(master=self, bg=self.DARK_GRAY)
        self._body_frame.pack(side=TOP, expand=1, fill='both')

        self._footer_frame: Frame = Frame(master=self, bg=self.COLORS[s])
        self._footer_frame.pack(side=BOTTOM, fill='x')

        self._order_type_label: Label = Label(master=self._footer_frame, text=t, font=helv18, bg=self.COLORS[s])
        self._order_type_label.pack(side=LEFT, padx=5, pady=5)

        self._order_status_label: Label = Label(master=self._footer_frame, text=state, font=helv18, bg=self.COLORS[s])
        self._order_status_label.pack(side=RIGHT, padx=5, pady=5)

# root = Tk()

# OrderTileGUI(parent=root, row=0, column=0, padx=10, pady=10)

# mainloop()
