from tkinter import *
from tkinter import font as tkFont
from cashdesk_model import CashDeskModel
from ContentControl.add_order_view import AddOrderView
from ContentControl.content_panel import ContentPanel
from Templates.cbutton import CButton
from Templates.images import IMAGES

class CashDeskGUI():
    def __init__(self):
        root = Tk()
        root.attributes('-fullscreen', True)
        root.wm_title("GUI Kasse")
        root.config(background="#696969")

        root.update()

        helv18 = tkFont.Font(family='Helvetica', size=18)

        self.model = CashDeskModel()

        ## HEADER STUFF ##

        header = Frame(root, height=100, background="#EFEFEF")
        header.pack(side=TOP, expand=True, fill='x', padx=5, pady=5)

        self._add_order_button = CButton(
            parent=header,
            image=self.model.checkmark_img,
            command=self.add_order,
            fg=CButton.WHITE, bg=CButton.GREEN,
            row=0, column=0
        )

        self._clear_button = CButton(
            parent=header,
            image=self.model.trashcan_img,
            command=self.model.clear_form,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=1
        )

        ## FOOTER STUFF ##

        footerContainer = Frame(root, height=100, background="#EFEFEF")
        footerContainer.pack(side=BOTTOM, expand=True, fill='x', padx=5, pady=5)

        footer = Frame(footerContainer, height=100, background="#EFEFEF")
        footer.pack(side=LEFT)

        self._footer_title = Label(
            master=footerContainer,
            text="<Current Content View>",
            font=helv18,
            padx=10
        )
        self._footer_title.pack(side=LEFT)

        self._footer_clock = Label(
            master=footerContainer,
            text="<CURRENT_TIME>",
            font=helv18,
            padx=10
        )
        self._footer_clock.pack(side=RIGHT)

        self._exit_button = CButton(
            parent=footer,
            image=self.model.exit_img,
            width=1,
            spaceX=(0.0,1.0),
            command=self.terminate,
            fg=CButton.WHITE, bg=CButton.DARK_RED,
            row=0, column=0
        )

        self._active_orders_button = CButton(
            parent=footer,
            image=self.model.in_progress_img,
            command=self.show_active_orders,
            fg=CButton.DARK, bg=CButton.YELLOW,
            row=0, column=1
        )

        self._history_button = CButton(
            parent=footer,
            image=self.model.history_img,
            spaceX=(0.0,1.0),
            command=self.show_history,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=2
        )

        self._settings_button = CButton(
            parent=footer,
            image=self.model.settings_img,
            spaceX=(0.0,1.0),
            command=self.show_settings,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=3
        )

        ## BODY STUFF ##

        self.body = ContentPanel(root, height=100000)
        self.body.pack(side=TOP, expand=1, fill='both', padx=5)
        self.body.lower()

        # TODO:
        # The content panel should contain all the different views (= classes that inherit from Frame)
        # and the corresponding methods to show / hide each of them.
        # For this, the content panel has to have a grid inside.

        ## ADDITIONAL STUFF ##

        self.model.initialize()
        self.model.on_cycle_event.add(self.on_cycle)

        mainloop()

    @property
    def add_order_button(self) -> CButton:
        return self._add_order_button

    @property
    def clear_button(self) -> CButton:
        return self._clear_button

    @property
    def exit_button(self) -> CButton:
        return self._exit_button

    @property
    def active_orders_button(self) -> CButton:
        return self._active_orders_button

    @property
    def history_button(self) -> CButton:
        return self._history_button

    @property
    def settings_button(self) -> CButton:
        return self._settings_button

    def add_order(self):
        self.add_order_button._disable()
        self.model.call_after_delay(self.add_order_button._enable, 1.0)
        
        self.model.add_order()

    def show_active_orders(self):
        if not self.body.is_active_orders_shown():
            self.body.show_active_orders_view()
        else:
            self.body.show_add_order_view()

    def show_history(self):
        # if not self.body.is_history_shown():
        #     self.body.show_history_view()
        # else:
        #     self.body.show_add_order_view()
        pass

    def show_settings(self):
        # if not self.body.is_settings_shown():
        #     self.body.show_settings_view()
        # else:
        #     self.body.show_add_order_view()
        pass

    def on_cycle(self):
        # UPDATE CURRENT TIME
        self._footer_clock.config(text=self.model.current_time)

        # UPDATE CONTENT TITLE
        curr_title = self._footer_title.cget("text")
        new_title = self.body.active_view().title()
        if not curr_title is new_title:
            self._footer_title.config(text=new_title)

    def terminate(self):
        self.model._cancel_timer()
        exit()
