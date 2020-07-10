import ControlPanelBackground as bg
from tkinter import font as tkFont
from tkinter import *
import os


class ControlPanel(Frame):
    def __init__(self, parent, panelheight, panelbackground):
        super().__init__(
            master=parent,
            #  width=panelwidth,
            cnf={},
            height=panelheight,
            background=panelbackground
        )
        self.update()
        panelwidth = self.winfo_screenwidth()

        helv36 = tkFont.Font(family='Helvetica', size=20, weight='bold')
        base_folder = os.path.dirname(__file__)

        NUM_BUTTONS = 6

        # previous button
        image_path1 = os.path.join(base_folder, 'arrowleft.gif')
        self.image_previous = PhotoImage(file=image_path1)
        self._previous_button = Button(self, text="Previous", image=self.image_previous, width=int(panelwidth / NUM_BUTTONS), font=helv36,
                              height=panelheight, background="LightBlue4", compound="left")
        self._previous_button.grid(row=0, column=0)

        # next button
        image_path2 = os.path.join(base_folder, 'arrowright.gif')
        self.image_next = PhotoImage(file=image_path2)
        self._next_button = Button(self, text="Next", image=self.image_next, width=int(panelwidth / NUM_BUTTONS), font=helv36,
                          height=panelheight, background="LightBlue4", compound="right")
        self._next_button.grid(row=0, column=5, sticky=E)

        # done button
        image_path3 = os.path.join(base_folder, 'Transparent.gif')
        self.image_tresparent = PhotoImage(file=image_path3)
        self._done_button = Button(self, width=int(panelwidth / NUM_BUTTONS), height=panelheight, image=self.image_tresparent,
                            text="Done", background="green", font=helv36, compound="left", command=bg.set_done)
        self._done_button.grid(row=0, column=1)

        # cancel button
        self._cancel_button = Button(self, text="Cancel", width=int(panelwidth / NUM_BUTTONS), image=self.image_tresparent,
                              height=panelheight, background="red", compound="left", font=helv36, command=bg.cancel_order)
        self._cancel_button.grid(row=0, column=2)
        # summary button
        self._summary_button = Button(self, text="Summary", width=int(panelwidth / NUM_BUTTONS), image=self.image_tresparent,
                               height=panelheight, background="yellow", compound="left", font=helv36, command=bg.open_summary)
        self._summary_button.grid(row=0, column=3)

        # add button
        self._add_button = Button(self, text="+", height=panelheight, width=int(panelwidth / NUM_BUTTONS),
                             background="blue", image=self.image_tresparent)
        self._add_button.grid(row=0, column=4)

        self.update()



    def set_command_add_button(self, callback):
       self._add_button.config(command=callback)

    def set_command_next_button(self, callback):
       self._next_button.config(command=callback)

    def set_command_previous_button(self, callback):
        self._previous_button.config(command=callback)