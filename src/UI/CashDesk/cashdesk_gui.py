from tkinter import *
from cashdesk_model import CashDeskModel
from ContentControl.add_order_view import AddOrderView
from ContentControl.content_panel import ContentPanel
from Templates.cbutton import CButton
from Templates.images import IMAGES

class CashDeskGUI():
    DEBUG = True

    def __init__(self):
        # Initializing the main window
        root = Tk()
        # root.attributes('-fullscreen', True)
        root.wm_title("GUI Kasse")
        root.config(width=1450, height=850, background="#696969")
        root.update()

        root.pack_propagate(0)

        self._root = root

        # The default font for the labels
        helv18 = ('Helvetica', '18')

        # Declaring the cash desk's model object
        self.model = CashDeskModel(root)

        ## -------- HEADER STUFF -------- ##

        self._headercontainer = Frame(root, background="#EFEFEF")
        self._headercontainer.pack(side=TOP, fill='x', padx=5, pady=5)

        # TODO: Move all of this into the add order view and finish the 
        # TODO: generic toolbar system (where the toolbar is chosen form the active view)

        # The frame at the top of the window
        # header = Frame(self._headercontainer, background="#EFEFEF")
        # header.pack(side=TOP, fill='x', padx=5, pady=5)
        # header.grid(row=0, column=0, sticky='nsew')

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

        self._exit_img = IMAGES.create(IMAGES.EXIT)

        # The button to exit the program
        self._exit_button = CButton(
            parent=footer,
            image=self._exit_img,
            width=1,
            spaceX=(0.0,1.0),
            command=self.terminate,
            fg=CButton.WHITE, bg=CButton.DARK_RED,
            row=0, column=0
        )

        self.add_order_view_img = IMAGES.create(IMAGES.BURGER_DARK)

        # The button to bring up the add order view
        self._add_order_view_button = CButton(
            parent=footer,
            image=self.add_order_view_img,
            command=self.show_add_order,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=1
        )

        self.in_progress_img = IMAGES.create(IMAGES.IN_PROGRESS)

        # The button to bring up the active orders view
        self._active_orders_button = CButton(
            parent=footer,
            image=self.in_progress_img,
            command=self.show_active_orders,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=2
        )

        self.history_img = IMAGES.create(IMAGES.HISTORY)

        # The button to bring up the history view
        self._history_button = CButton(
            parent=footer,
            image=self.history_img,
            spaceX=(0.0,1.0),
            command=self.show_history,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=3
        )

        self.settings_img = IMAGES.create(IMAGES.SETTINGS)

        # The button to bring up the settings view
        self._settings_button = CButton(
            parent=footer,
            image=self.settings_img,
            spaceX=(0.0,1.0),
            command=self.show_settings,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=4
        )

        ## -------- BODY STUFF -------- ##

        # The content panel (container) in the middle of the window
        self.body = ContentPanel(root, self._headercontainer) #self.model.body_content_changed_event)
        self.body.pack(side=TOP, expand=1, fill='both', padx=5)
        # Lowered to the minimum z-Layer, so that the notification toasts are visible
        self.body.lower()

        ## -------- ADDITIONAL STUFF -------- ##

        # Add callback functions that are called as soon as the database connection is established
        # TODO: temp exluce
        self.model.db_connection_ready_event.add(self.body.add_order_view.initialize)
        # self.body.add_order_view.initialize()

        # Initializing the model after the GUI has finished the init process
        self.model.initialize(debug=CashDeskGUI.DEBUG)

        # Adding the GUI's callback function to the main periodic thread event of the model
        self.model.on_cycle_event.add(self.on_cycle)
        self.model.body_content_changed_event.add(self.body_changed)

        # Start main loop to wait for actions
        mainloop()

    ### ------------------- PROPERTIES ------------------- ###

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

    def show_add_order(self):
        """ Show the add order view in the body.
        """
        self.body.show_add_order_view()

    def show_active_orders(self):
        """ Show the active orders view in the body.
        """
        self.body.show_active_orders_view()

    def show_history(self):
        """ Show the history view in the body.
        """
        self.body.show_history_view()

    def show_settings(self):
        """ Show the settings view in the body.
        """
        self.body.show_settings_view()

    ### ------------------- PRIVATE METHODS ------------------- ###

    def body_changed(self):
        """ Callback function to be called, whenever the body content changes
        """
        for header_child in self._headercontainer.winfo_children():
            header_child.destroy()
            # TODO

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
