import Templates.references as REFS
from Templates.order import Order
from datetime import datetime
from tkinter import *


class OrderTileGUI(Frame):
    TIMESTAMP_FORMAT="%H:%M:%S"

    COLORS=[
        REFS.LIGHT_GRAY,
        REFS.LIGHT_GREEN,
        REFS.LIGHT_YELLOW,
        REFS.LIGHT_RED
    ]

    LIGHT_GRAY = REFS.LIGHT_GRAY
    DARK_GRAY = "#ADADA9"

    def __init__(self, parent, order: Order, background="#A2ABAD"):
        super().__init__(
            master=parent,
            cnf={},
            background=background
        )

        self._order: Order = order
        self._order.on_state_changed.add(self._state_changed_cb)

        self._font = ('Helvetica', '12')
        self._font_bold = ('Helvetica', '12', 'bold')

        ### Header

        self._header_container = Frame(
            master=self,
            background=self.LIGHT_GRAY,
            height=30
        )
        self._header_container.pack(side=TOP, fill='x')

        self._id_label = Label(
            master=self._header_container,
            background=self.LIGHT_GRAY,
            font=self._font_bold,
            text=f"#{self._order.id}"
        )
        self._id_label.pack(side=LEFT, padx=2, pady=2)

        dateTimeObj = datetime.fromtimestamp(self._order.timestamp)
        timeStampStr = dateTimeObj.strftime(OrderTileGUI.TIMESTAMP_FORMAT)

        self._timestamp_label = Label(
            master=self._header_container,
            background=self.LIGHT_GRAY,
            font=self._font,
            text=f"{timeStampStr}"
        )
        self._timestamp_label.pack(side=RIGHT, padx=2, pady=2)

        ### Footer

        self._footer_container = Frame(
            master=self,
            background=self.COLORS[self._order.state],
            height=30
        )
        self._footer_container.pack(side=BOTTOM, fill='x')

        self._form_label = Label(
            master=self._footer_container,
            background=self.COLORS[self._order.state],
            font=self._font,
            text=REFS.ORDER_FORMS[self._order.form]
        )
        self._form_label.pack(side=LEFT, padx=2, pady=2)

        self._state_label = Label(
            master=self._footer_container,
            background=self.COLORS[self._order.state],
            font=self._font_bold,
            text=REFS.ORDER_STATES[self._order.state]
        )
        self._state_label.pack(side=RIGHT, padx=2, pady=2)

    def _state_changed_cb(self):
        self._footer_container.config(bg=self.COLORS[self._order.state])

        self._form_label.config(bg=self.COLORS[self._order.state])

        self._state_label.config(bg=self.COLORS[self._order.state])
        self._state_label.config(text=REFS.ORDER_STATES[self._order.state])
