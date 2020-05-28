from tkinter import *
from tkinter import font as tkFont
from cashdesk_model import CashDeskModel
from ContentControl.add_order_view import AddOrderView
from ContentControl.content_panel import ContentPanel
from Templates.cbutton import CButton
from Templates.images import IMAGES

class CashDeskGUI():
    def __init__(self):
        # Initializing the main window
        root = Tk()
        root.attributes('-fullscreen', True)
        root.wm_title("GUI Kasse")
        root.config(background="#696969")
        root.update()

        self._root = root

        # The default font for the labels
        helv18 = tkFont.Font(family='Helvetica', size=18)

        # Declaring the cash desk's model object
        self.model = CashDeskModel()

        ## -------- HEADER STUFF -------- ##

        # The frame at the top of the window
        header = Frame(root, background="#EFEFEF")
        header.pack(side=TOP, fill='x', padx=5, pady=5)

        # The add-order button to add a new order
        self._add_order_button = CButton(
            parent=header,
            image=self.model.checkmark_img,
            command=self.add_order,
            fg=CButton.WHITE, bg=CButton.GREEN,
            row=0, column=0
        )

        # The clear button to reset the widgets in the add-order-view to their default values
        self._clear_button = CButton(
            parent=header,
            image=self.model.trashcan_img,
            command=self.model.clear_form,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=1
        )

        ## -------- FOOTER STUFF -------- ##

        # The frame at the bottom of the window that acts as a container for all the elements
        footerContainer = Frame(root, background="#EFEFEF")
        footerContainer.pack(side=BOTTOM, fill='x', padx=5, pady=5)

        # The frame within the container holding all the buttons
        footer = Frame(footerContainer, height=100, background="#EFEFEF")
        footer.pack(side=LEFT)

        # The label within the container with the title of the currently active view
        self._footer_title = Label(
            master=footerContainer,
            text="<Current Content View>",
            font=helv18,
            padx=10
        )
        self._footer_title.pack(side=LEFT)

        # The label within the container with the current timestamp
        self._footer_clock = Label(
            master=footerContainer,
            text="<CURRENT_TIME>",
            font=helv18,
            padx=10
        )
        self._footer_clock.pack(side=RIGHT)

        # The button to exit the program
        self._exit_button = CButton(
            parent=footer,
            image=self.model.exit_img,
            width=1,
            spaceX=(0.0,1.0),
            command=self.terminate,
            fg=CButton.WHITE, bg=CButton.DARK_RED,
            row=0, column=0
        )

        # The button to bring up or close the active orders view (toggles)
        self._active_orders_button = CButton(
            parent=footer,
            image=self.model.in_progress_img,
            command=self.show_active_orders,
            fg=CButton.DARK, bg=CButton.YELLOW,
            row=0, column=1
        )

        # The button to bring up or close the history view (toggles)
        self._history_button = CButton(
            parent=footer,
            image=self.model.history_img,
            spaceX=(0.0,1.0),
            command=self.show_history,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=2
        )

        # The button to bring up or close the settings view (toggles)
        self._settings_button = CButton(
            parent=footer,
            image=self.model.settings_img,
            spaceX=(0.0,1.0),
            command=self.show_settings,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=3
        )

        ## -------- BODY STUFF -------- ##

        # The content panel (container) in the middle of the window
        self.body = ContentPanel(root)
        self.body.pack(side=TOP, expand=1, fill='both', padx=5)
        # Lowered to the minimum z-Layer, so that the notification toasts are visible
        self.body.lower()

        ## -------- ADDITIONAL STUFF -------- ##

        # Initializing the model after the GUI has finished the init process
        self.model.initialize()
        # Adding the GUI's callback function to the main periodic thread event of the model
        self.model.on_cycle_event.add(self.on_cycle)

        # Start main loop to wait for actions
        mainloop()

    ### ------------------- PROPERTIES ------------------- ###

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

    ### ------------------- MAIN METHODS ------------------- ###

    def add_order(self):
        """ Adds a new order with the information given in the add-order-view.
        """
        self.add_order_button._disable()
        self.model.call_after_delay(self.add_order_button._enable, 1.0)
        
        self.model.add_order()

    def show_active_orders(self):
        """ Show the active orders view in the body. If already shown, then this will return to the default view.
        """
        if not self.body.is_active_orders_shown():
            self.body.show_active_orders_view()
        else:
            self.body.show_add_order_view()

    def show_history(self):
        """ Show the history view in the body. If already shown, then this will return to the default view.
        """
        self.body.active_view.add_order_tile()
        # if not self.body.is_history_shown():
        #     self.body.show_history_view()
        # else:
        #     self.body.show_add_order_view()
        pass

    def show_settings(self):
        """ Show the settings view in the body. If already shown, then this will return to the default view.
        """
        # if not self.body.is_settings_shown():
        #     self.body.show_settings_view()
        # else:
        #     self.body.show_add_order_view()
        pass

    ### ------------------- PRIVATE METHODS ------------------- ###

    def on_cycle(self):
        """ Callback function to be called, whenever the main event of the model is triggered.
        """
        # UPDATE CURRENT TIME
        self._footer_clock.config(text=self.model.current_time)

        # UPDATE CONTENT TITLE
        curr_title = self._footer_title.cget("text")
        new_title = self.body.active_view.title
        if not curr_title is new_title:
            self._footer_title.config(text=new_title)

    def terminate(self):
        """ Exits the program properly.
        """
        self.model._cancel_timer()
        self._root.destroy()
