from functools import partial
from tkinter import *
from tkinter import font as tkFont
from Templates.cbutton import CButton
from Templates.images import IMAGES
from EventHandler.Event import Event
from Templates.fonts import Fonts
import Templates.references as REFS

class Toast():
    WIDTH = 500
    HEIGHT = 220

    FADEOUT_DELAY = 7000
    INITIAL_ALPHA = 0.8

    BACKGROUND=CButton.LIGHT
    
    def __init__(
        self,
        title,
        summary,
        id,
        remove_cb,
        remove_all_cb,
        origin = (0,0),
        margin = (15,15),
        keep_alive = False # If True, the toast won't fade out
    ):
        self._timer_id = -1
        self._fade_timer_id = -1
        self._id = id

        self._keep_alive = keep_alive

        self._visible = True
        self._stop_checking = False

        self._title = title
        self._summary = summary

        self._dest_x = origin[0]
        self._dest_y = origin[1]
        self._margin = margin

        window = Toplevel()

        window.overrideredirect(1)
        window.attributes('-topmost', 1)
        window.config(background=self.BACKGROUND)
        window.attributes("-alpha", self.INITIAL_ALPHA)

        if keep_alive:
            window.config(highlightbackground=REFS.LIGHT_YELLOW)
            window.config(highlightthickness=4)
        
        window.update()

        self._window = window

        self.update_window_geometry()

        self._header_frame = Frame(
            master=window,
            bg=self.BACKGROUND
        )
        self._header_frame.pack(side=TOP, fill='x', padx=5, pady=(5,0))

        self._title_label = Label(
            master=self._header_frame,
            text=self._title,
            font=Fonts.xlarge(bold=True),
            anchor="nw",
            justify="left",
            bg=self.BACKGROUND
        )
        self._title_label.pack(side=LEFT)

        self._button_frame = Frame(
            master=self._header_frame,
            bg=self.BACKGROUND
        )
        self._button_frame.pack(side=RIGHT)

        self.close_img = IMAGES.create(IMAGES.CLOSE)
        self.close_all_img = IMAGES.create(IMAGES.CLOSE_ALL)

        std_button_width = 20 + 20 * (not REFS.MOBILE)

        self.remove_self = partial(remove_cb, self)

        self._close_button = Button(
            master=self._button_frame,
            image=self.close_img,
            command=self.remove_self,
            width=std_button_width,
            height=std_button_width,
            bg=self.BACKGROUND
        )
        self._close_button.pack(side=RIGHT, padx=(5,0))

        self._close_all_button = Button(
            master=self._button_frame,
            image=self.close_all_img,
            command=remove_all_cb,
            width=std_button_width,
            height=std_button_width,
            bg=self.BACKGROUND
        )
        self._close_all_button.pack(side=RIGHT, padx=5)

        self._summary_label = Label(
            master=window,
            text=self._summary,
            font=Fonts.medium(),
            anchor="nw",
            justify="left",
            bg=self.BACKGROUND
        )
        self._summary_label.pack(side=TOP, fill='both', padx=5, pady=5)

    @property
    def keep_alive(self) -> bool:
        return self._keep_alive

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def visible(self) -> bool:
        return self._visible

    @property
    def stop_checking(self) -> bool:
        return self._stop_checking

    @property
    def title(self) -> str:
        return self._title

    @property
    def summary(self) -> str:
        return self._summary

    @property
    def timer_id(self):
        return self._timer_id

    @timer_id.setter
    def timer_id(self, tid):
        if self._timer_id == -1:
            self._timer_id = tid

    def hide(self):
        self._window.withdraw()
        self._visible = False

    def show(self):
        self._window.update()
        self._window.deiconify()
        self._visible = True

    def fade_out(self):
        try:
            alpha = self._window.attributes("-alpha")
            if alpha > 0:
                alpha -= .1
                self._window.attributes("-alpha", alpha)
                self._fade_timer_id = self._window.after(100, self.fade_out)
            else:
                # self.remove_toast()
                self.remove_self()
        except:
            pass

    def update_window_geometry(self):
        y_position = self._dest_y - self._id * (Toast.HEIGHT + self._margin[1])
        self._window.geometry(f"{Toast.WIDTH}x{Toast.HEIGHT}+{self._dest_x}+{y_position}")

    def remove_toast(self):
        if self._fade_timer_id != -1:
            self._window.after_cancel(self._fade_timer_id)
        
        self._stop_checking = True
        self._window.destroy()
