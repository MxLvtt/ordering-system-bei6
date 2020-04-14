from threading import Timer
from tkinter import *
from tkinter import font as tkFont
from Templates.cbutton import CButton
from Templates.images import IMAGES

class Toast():
    WIDTH=420
    HEIGHT=200
    TIME_TILL_FADEOUT=10

    BACKGROUND="#E3E1DD"
    
    # STATIC VARIABLES
    COUNT_TOASTS=0
    TOASTS=[]

    def __init__(
        self,
        parent,
        title,
        summary,
        pos=(0,0)
    ):
        helv22b = tkFont.Font(family='Helvetica', size=22, weight=tkFont.BOLD)
        helv18 = tkFont.Font(family='Helvetica', size=18)

        # TODO: Should only be displayed, if position is within the boundaries

        self._visible = True
        self._stop_checking = False

        self._id = Toast.COUNT_TOASTS
        self._title = f"{title} {self._id}"
        self._summary = summary

        self._dest_x = pos[0]
        self._dest_y = pos[1]

        window = Toplevel(parent)
        window.geometry(f"{self.WIDTH}x{self.HEIGHT}+{self._dest_x}+{self._dest_y - self._id * (self.HEIGHT + 15)}")
        window.overrideredirect(1)
        window.attributes('-topmost', 1)
        window.config(background=self.BACKGROUND)

        window.update()

        self._window = window

        Toast.COUNT_TOASTS += 1

        self._header_frame = Frame(
            master=window,
            bg=self.BACKGROUND
        )
        self._header_frame.pack(side=TOP, fill='x', padx=5, pady=(5,0))

        self._title_label = Label(
            master=self._header_frame,
            text=self._title,
            font=helv22b,
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

        self.close_img = PhotoImage(file=IMAGES.CLOSE)
        self.close_all_img = PhotoImage(file=IMAGES.CLOSE_ALL)

        self._close_button = Button(
            master=self._button_frame,
            image=self.close_img,
            command=self._remove_toast,
            width=40, height=40,
            bg=self.BACKGROUND
        )
        self._close_button.pack(side=RIGHT, padx=(5,0))

        self._close_all_button = Button(
            master=self._button_frame,
            image=self.close_all_img,
            command=self._remove_all,
            width=40, height=40,
            bg=self.BACKGROUND
        )
        self._close_all_button.pack(side=RIGHT, padx=5)

        self._summary_label = Label(
            master=window,
            text=self._summary,
            font=helv18,
            anchor="nw",
            justify="left",
            bg=self.BACKGROUND
        )
        self._summary_label.pack(side=TOP, fill='both', padx=5, pady=5)

        self.TOASTS.append(self)

        self._timeout_timer = Timer(self.TIME_TILL_FADEOUT, self._fade_out)
        self._timeout_timer.start()
    
        self._check_toast_count()

    @property
    def title(self) -> str:
        return self._title

    @property
    def summary(self) -> str:
        return self._summary

    def _animate(self, xpos: int):
        xpos = xpos + 2
        if xpos < self._dest_x:
            self._window.geometry(f"{self.WIDTH}x{self.HEIGHT}+{xpos}+{self._dest_y}")
            self._window.after(1, self._animate, xpos)
        else:
            self._window.geometry(f"{self.WIDTH}x{self.HEIGHT}+{self._dest_x}+{self._dest_y}")
            # Timer(self.TIME_TILL_FADEOUT, self._fade_out).start()

    def _fade_out(self):
        alpha = self._window.attributes("-alpha")
        if alpha > 0:
            alpha -= .1
            self._window.attributes("-alpha", alpha)
            self._window.after(100, self._fade_out)
        else:
            self._remove_toast()

    def _check_toast_count(self):
        if self._id != self.TOASTS.index(self):
            self._id = self.TOASTS.index(self)
            self._window.geometry(
                f"{self.WIDTH}x{self.HEIGHT}+{self._dest_x}+{self._dest_y - self._id * (self.HEIGHT + 15)}"
            )

        if self._id >= 3:
            self._window.withdraw()
            self._visible = False
        elif not self._visible:
            self._window.update()
            self._window.deiconify()
            self._visible = True

        if not self._stop_checking:
            self._window.after(100, self._check_toast_count)

    def _remove_toast(self, remove_all: bool = False):
        if self._timeout_timer.is_alive():
            self._timeout_timer.cancel()
        Toast.COUNT_TOASTS -= 1
        if Toast.COUNT_TOASTS < 0:
            Toast.COUNT_TOASTS = 0
        self._stop_checking = True
        if not remove_all:
            self.TOASTS.remove(self)
        self._window.destroy()

    def _remove_all(self):
        for toast in self.TOASTS:
            toast._remove_toast(True)
        self.TOASTS.clear()
