import sys, os
from tkinter import *
from cashdesk_model import CashDeskModel
from ContentControl.add_order_view import AddOrderView
from ContentControl.content_panel import ContentPanel
from Handlers.network_handler import NetworkHandler
from Notification.notification_service import NotificationService
from Templates.cbutton import CButton
from Templates.images import IMAGES
from Templates.fonts import Fonts
import Templates.references as REFS

class CashDeskGUI():
    DEBUG = False

    def __init__(
        self,
        mobile_view: bool = False,
        main_station: bool = True,
        debug: bool = False,
        suppress_logs: bool = False
    ):
        CashDeskGUI.DEBUG = debug

        if not debug or suppress_logs:
            sys.stdout = open(os.devnull, 'w')

        REFS.MOBILE = mobile_view
        REFS.MAIN_STATION = main_station

        # Initializing the main window
        root = Tk()
        ## root.resizable(False, False)
        
        root.resizable(True, True)
        root.attributes('-fullscreen', True)

        root.config(background='#696969')

        #if not CashDeskGUI.DEBUG:
        #    root.attributes('-fullscreen', True)

        # Window Size: approx. 7 in
        root_bg = "#696969"
        # root.config(width=866, height=487, background=root_bg)
        #root.config(width=800, height=480, background=root_bg)

        station = 'Küche'

        #if main_station:
        #    station = 'Kasse'

        title_size = 'Mobile Ansicht (7")'

        #if not mobile_view:
        #    title_size = 'Vollbild'

        #    if CashDeskGUI.DEBUG:
        #        root.attributes('-fullscreen', True)


        root.wm_title(f"Bestellsystem - {station} - {title_size}")

        root.update()

        root.pack_propagate(0)

        self._root = root

        # The default font for the labels
        def_font = Fonts.medium()
        paddings = (5,5)

        if mobile_view:
            # The default font for the labels
            def_font = Fonts.xxsmall()
            paddings = (0,0)

        # Declaring the cash desk's model object
        self.model = CashDeskModel(root)

        ## -------- HEADER STUFF -------- ##

        self._headercontainer = Frame(root, background="#EFEFEF")
        self._headercontainer.pack(side=TOP, fill='x', padx=paddings, pady=paddings)

        self._toolbar_container = Frame(self._headercontainer, background="#EFEFEF")
        self._toolbar_container.pack(side=LEFT, fill='both', expand=1)

        if REFS.MOBILE:
            self._nav_img = IMAGES.create(IMAGES.NAVIGATION)

            self._more_button_container = Frame(
                master=self._headercontainer,
                background="#EFEFEF"
            )
            self._more_button_container.pack(side=RIGHT, fill='both')

            self._more_button = CButton(
                parent=self._more_button_container,
                image=self._nav_img,
                width=1,
                command=self.open_side_bar,
                fg=CButton.DARK, bg=CButton.LIGHT,
                row=0, column=0
            )

        # The frame at the top of the window
        # header = Frame(self._headercontainer, background="#EFEFEF")
        # header.pack(side=TOP, fill='x', padx=5, pady=5)
        # header.grid(row=0, column=0, sticky='nsew')

        ## -------- BODY STUFF -------- ##

        self.body_container = Frame(root, background=root_bg)
        self.body_container.pack(side=TOP, expand=1, fill='both', padx=paddings)

        # The content panel (container) in the middle of the window
        self.body = ContentPanel(self.body_container, self._toolbar_container) #self.model.body_content_changed_event)
        self.body.pack(side=LEFT, expand=1, fill='both')
        # Lowered to the minimum z-Layer, so that the notification toasts are visible
        self.body.lower()

        ## -------- FOOTER STUFF -------- ##
    
        # The frame at the bottom of the window that acts as a container for all the elements
        footerContainer = Frame(root, background="#EFEFEF")   

        if REFS.MOBILE:
            self.side_bar_visible = False
            self.side_bar = Frame(self.body_container, background="#EFEFEF")
            footerContainer = self.side_bar
        else:
            footerContainer.pack(side=BOTTOM, fill='x', padx=paddings, pady=paddings)

        # The frame within the container holding all the buttons
        footer = Frame(footerContainer, background="#EFEFEF")
        
        # The label within the container with the current timestamp
        self._footer_clock = Label(
            master=footerContainer,
            text="<CURRENT_TIME>",
            font=def_font,
            padx=10
        )

        self.connection_image = IMAGES.create(IMAGES.CONNECTION)
        self.connection_lost_image = IMAGES.create(IMAGES.CONNECTION_LOST)
        self.connection_ready_image = IMAGES.create(IMAGES.CONNECTION_READY)

        self._connection_symbol = Label(
            master=footerContainer,
            image=self.connection_image,
            padx=5, pady=5
        )

        if mobile_view:
            footer.pack(side=BOTTOM)

            self._footer_clock.pack(side=TOP)
            self._connection_symbol.pack(side=TOP)
        else:
            footer.pack(side=LEFT)

            # The label within the container with the title of the currently active view
            self._footer_title = Label(
                master=footerContainer,
                text="<Current Content View>",
                font=def_font,
                padx=10
            )
            self._footer_title.pack(side=LEFT)

            self._footer_clock.pack(side=RIGHT)
            self._connection_symbol.pack(side=RIGHT)

        spaceX = (0.0,1.0)
        spaceY = (0.0,0.0)

        if mobile_view:
            spaceX = (0.0,0.0)
            spaceY = (0.0,0.5)

        self._exit_img = IMAGES.create(IMAGES.EXIT)

        # The button to exit the program
        self._exit_button = CButton(
            parent=footer,
            image=self._exit_img,
            width=1 - 2 * mobile_view,
            vertical=mobile_view,
            spaceX=spaceX, spaceY=(spaceY[1], spaceY[0]),
            command=self.terminate,
            fg=CButton.WHITE, bg=CButton.DARK_RED,
            row=0, column=0 + 5 * mobile_view,
            flip_row_and_col=mobile_view
        )

        if REFS.MAIN_STATION:
            self.add_order_view_img = IMAGES.create(IMAGES.BURGER_DARK)

            # The button to bring up the add order view
            self._add_order_view_button = CButton(
                parent=footer,
                image=self.add_order_view_img,
                vertical=mobile_view,
                command=self.show_add_order,
                fg=CButton.DARK, bg=CButton.LIGHT,
                row=0, column=1,
                flip_row_and_col=mobile_view
            )

        self.in_progress_img = IMAGES.create(IMAGES.IN_PROGRESS)

        # The button to bring up the active orders view
        self._active_orders_button = CButton(
            parent=footer,
            image=self.in_progress_img,
            vertical=mobile_view,
            command=self.show_active_orders,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=2,
            flip_row_and_col=mobile_view
        )

        self.history_img = IMAGES.create(IMAGES.HISTORY)

        # The button to bring up the history view
        self._history_button = CButton(
            parent=footer,
            image=self.history_img,
            vertical=mobile_view,
            spaceX=spaceX,
            command=self.show_history,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=3,
            flip_row_and_col=mobile_view
        )

        if REFS.MAIN_STATION:
            self.settings_img = IMAGES.create(IMAGES.SETTINGS)

            # The button to bring up the settings view
            self._settings_button = CButton(
                parent=footer,
                image=self.settings_img,
                vertical=mobile_view,
                spaceX=spaceX,
                command=self.show_settings,
                fg=CButton.DARK, bg=CButton.LIGHT,
                row=0, column=4,
                flip_row_and_col=mobile_view
            )

        ## -------- ADDITIONAL STUFF -------- ##

        # Add callback functions that are called as soon as the database connection is established
        if REFS.MAIN_STATION:
            self.model.db_connection_ready_event.add(self.body.add_order_view.initialize)
        else:
            self.model.db_connection_ready_event.add(self.body.active_orders_view.update_view_and_database_content)
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
        for toolbar_child in self._toolbar_container.winfo_children():
            toolbar_child.destroy()
            # TODO

    def on_cycle(self):
        """ Callback function to be called, whenever the main event of the model is triggered.
        """
        # UPDATE CURRENT TIME
        self._footer_clock.config(text=self.model.current_time)

        # UPDATE CONNECTION SYMBOL
        if NetworkHandler.CONNECTION_READY:
            self._connection_symbol.config(image=self.connection_ready_image)
        else:
            self._connection_symbol.config(image=self.connection_lost_image)

        # UPDATE CONTENT TITLE
        curr_title = self._footer_title.cget("text")
        new_title = self.body.active_view.title
        if not curr_title is new_title:
            self._footer_title.config(text=new_title)

    def terminate(self):
        """ Exits the program properly.
        """
        self.model._notification_service.remove_all_toasts()
        self.model._cancel_timer()
        self.model.timer_handler.cancel_all_timers()
        self._root.destroy()

    def open_side_bar(self):
        if self.side_bar_visible:
            self.side_bar.pack_forget()
            self.side_bar_visible = False
        else:
            self.side_bar.pack(side=RIGHT, fill='y')
            self.side_bar_visible = True
