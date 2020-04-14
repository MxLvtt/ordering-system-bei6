import time
from threading import Timer
from tkinter import *
from tkinter import font as tkFont
from ContentControl.add_order_view import AddOrderView
from ContentControl.content_panel import ContentPanel
from Templates.cbutton import CButton
from Templates.images import IMAGES
from Templates.toast import Toast

class CashDeskGUI():
    def __init__(self):
        root = Tk()
        root.attributes('-fullscreen', True)
        root.wm_title("GUI Kasse")
        root.config(background="#696969")

        root.update()

        rootHeight = root.winfo_height()
        rootWidth = root.winfo_width()

        checkmark_img = PhotoImage(file=IMAGES.CHECK_MARK)
        exit_img = PhotoImage(file=IMAGES.EXIT)
        history_img = PhotoImage(file=IMAGES.HISTORY)
        in_progress_img = PhotoImage(file=IMAGES.IN_PROGRESS)
        settings_img = PhotoImage(file=IMAGES.SETTINGS)
        trashcan_img = PhotoImage(file=IMAGES.TRASH_CAN)

        helv18 = tkFont.Font(family='Helvetica', size=18)

        def _show_toast():
            Toast(
                parent=root,
                title="Notification Toast",
                summary="This is a short summary\nof the notification.",
                pos=(25, rootHeight-310)
            )

        ## HEADER STUFF ##

        header = Frame(root, height=100, background="#EFEFEF")
        header.pack(side=TOP, expand=True, fill='x', padx=5, pady=5)

        def _disable_button(custom_button: CButton, time_in_seconds: float = -1.0):
            custom_button._disable()
            if time_in_seconds != -1.0:
                Timer(time_in_seconds, custom_button._enable).start()

        def _add_order():
            _disable_button(add_order_button, 4.0)

            # TODO: Save order details
                
            _show_toast()

        def _clear_form():
            _disable_button(clear_button, 1.5)
            pass

        add_order_button = CButton(
            parent=header,
            image=checkmark_img,
            command=_add_order,
            fg=CButton.WHITE, bg=CButton.GREEN,
            row=0, column=0
        )

        clear_button = CButton(
            parent=header,
            image=trashcan_img,
            command=_clear_form,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=1
        )

        # add_order_button = CButton(
        #     parent=header,
        #     text="+",
        #     command=click_add_order_button,
        #     row=0, column=0
        # )._show()

        # add_order_button = Button(header, command=click_add_order_button, width=3, height=1, text="+",fg="black",bg="white",font=helv36)
        # add_order_button.grid(row=0,column=0)

        # finish_order_button = Button(header, command=click_finish_order_button, width=3, height=1, text="✔",fg="white",bg="darkgreen",font=helv36)
        # finish_order_button.grid(row=0,column=1)
        # finish_order_button.grid_remove()

        ## FOOTER STUFF ##

        footerContainer = Frame(root, height=100, background="#EFEFEF")
        footerContainer.pack(side=BOTTOM, expand=True, fill='x', padx=5, pady=5)

        footer = Frame(footerContainer, height=100, background="#EFEFEF")
        footer.pack(side=LEFT)

        footer_title = Label(
            master=footerContainer,
            text="<Current Content View>",
            font=helv18,
            padx=10
        )
        footer_title.pack(side=LEFT)

        footer_clock = Label(
            master=footerContainer,
            text="<CURRENT_TIME>",
            font=helv18,
            padx=10
        )
        footer_clock.pack(side=RIGHT)

        CButton( # Exit Button
            parent=footer,
            image=exit_img,
            width=1,
            spaceX=(0.0,1.0),
            command=exit,
            fg=CButton.WHITE, bg=CButton.DARK_RED,
            row=0, column=0
        )

        def _show_active_order():
            if not body.is_active_orders_shown():
                body.show_active_orders_view()
            else:
                body.show_add_order_view()
            pass

        def _show_history():
            pass

        def _open_settings():
            pass

        CButton( # Active Orders Button
            parent=footer,
            image=in_progress_img,
            command=_show_active_order,
            fg=CButton.DARK, bg=CButton.YELLOW,
            row=0, column=1
        )

        CButton( # History Button
            parent=footer,
            image=history_img,
            spaceX=(0.0,1.0),
            command=_show_history,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=2
        )

        CButton( # Settings Button
            parent=footer,
            image=settings_img,
            spaceX=(0.0,1.0),
            command=_open_settings,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=3
        )

        ## BODY STUFF ##

        body = ContentPanel(root, height=rootHeight)
        body.pack(side=TOP, expand=True, fill='both', padx=5)
        body.lower()

        # TODO:
        # The content panel should contain all the different views (= classes that inherit from Frame)
        # and the corresponding methods to show / hide each of them.
        # For this, the content panel has to have a grid inside.

        ## ADDITIONAL STUFF ##

        def _timer_thread(curtime=''):
            # UPDATE CLOCK
            newtime = time.strftime("%a, %d-%m-%Y\n%H:%M:%S")
            if newtime != curtime:
                curtime = newtime
                footer_clock.config(text=curtime)
            footer_clock.after(200, _timer_thread, curtime)

            # UPDATE CONTENT TITLE
            curr_title = footer_title.cget("text")
            new_title = body.active_view().title()
            if not curr_title is new_title:
                footer_title.config(text=new_title)

        _timer_thread()

        mainloop()
