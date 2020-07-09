from tkinter import *
from ContentControl.history_view import HistoryView, HistoryItem
from Templates.scroll_list import Scrolllist
import Templates.references as REFS


class MealsSettingsView(Frame):
    def __init__(
        self,
        parent,
        background
    ):
        super().__init__(
            master=parent,
            cnf={},
            background=background
        )

        ########## HEADER ##########

        header_bg = '#F4F4F4'

        self.header = Frame(
            master=self,
            background=header_bg,
            height=HistoryItem.HEIGHT)
        self.header.pack(side=TOP, fill='x', pady=(0,HistoryView.SPACING))
        self.header.pack_propagate(0)

        self.timestamp_head = Label(
            master=self.header,
            background=header_bg,
            text=REFS.ORDERS_TABLE_TIMESTAMP_GER.capitalize(),
            font=HistoryView.FONT_NORMAL,
            width=18
        )
        self.timestamp_head.pack(side=LEFT, padx=30)

        self.number_head = Label(
            master=self.header,
            background=header_bg,
            text=REFS.ORDERS_TABLE_ID_GER.capitalize(),
            font=HistoryView.FONT_BOLD,
            width=8
        )
        self.number_head.pack(side=LEFT, padx=30)

        self.form_head = Label(
            master=self.header,
            background=header_bg,
            text=REFS.ORDERS_TABLE_FORM_GER.capitalize(),
            font=HistoryView.FONT_NORMAL,
            width=10
        )
        self.form_head.pack(side=LEFT, padx=30)

        self.edit_head = Label(
            master=self.header,
            background=header_bg,
            # text=REFS.HISTORY_TABLE_EDIT,
            font=HistoryView.FONT_NORMAL,
            width=5
        )
        self.edit_head.pack(side=RIGHT, padx=30)
        self.edit_head.update()

        HistoryView.EDIT_HEADER_WIDTH = self.edit_head.winfo_reqwidth()
        
        self.expand_head = Label(
            master=self.header,
            background=header_bg,
            # text=REFS.HISTORY_TABLE_EXPAND,
            font=HistoryView.FONT_NORMAL,
            width=5
        )
        self.expand_head.pack(side=RIGHT, padx=(30,0))
        self.expand_head.update()

        HistoryView.EXPAND_HEADER_WIDTH = self.expand_head.winfo_reqwidth()

        self.active_head = Label(
            master=self.header,
            background=header_bg,
            text=REFS.ORDERS_TABLE_ACTIVE_GER.capitalize(),
            font=HistoryView.FONT_NORMAL,
            width=8
        )
        self.active_head.pack(side=RIGHT, padx=30)

        self.state_head = Label(
            master=self.header,
            background=header_bg,
            text=REFS.ORDERS_TABLE_STATE_GER.capitalize(),
            font=HistoryView.FONT_NORMAL,
            width=10
        )
        self.state_head.pack(side=RIGHT, padx=30)

        ########## TABLE ##########

        self.table = Frame(master=self, background='#F4F4F4')
        self.table.pack(side=TOP, fill='both', expand=1)

        self.scrolllist = ScrollList(parent=self.table, spacing=HistoryView.SPACING, background='#696969')
