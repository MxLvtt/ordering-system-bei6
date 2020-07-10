from tkinter import *


class RadioButton(Button):
    def __init__(
        self,
        master,
        text,
        group,
        highlight,
        background = None,
        font = None,
        command = None,
        initial_state = False,
        height=None,
        width=None
    ):
        super().__init__(
            master=master,
            text=text,
            command=self._button_command,
            width=width, height=height,
            cnf={}
        )

        if font != None:
            self.config(font=font)

        self._unselect_background = self.cget('background')

        if background != None:
            self._unselect_background = background
            self.config(background=background)

        self._select_background = highlight

        self._state: bool = True
        self._update_colors()

        self._group: RadioButtonGroup = group

        if group != None:
            group.add(self)

            if initial_state:
                self._state = True
                self._update_colors()
                group.update_buttons(self)

        self._external_callback = command

    @property
    def state(self) -> bool:
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state
        self._update_colors()

    def _update_colors(self):
        if self._state == True:
            self.config(background=self._select_background)
        else:
            self.config(background=self._unselect_background)

    def _button_command(self):
        # If button is already active/selected -> return
        if self._state == True:
            return

        self._state = True
        self._update_colors()
        
        if self._group != None:
            self._group.update_buttons(set_button=self)
            
        if self._external_callback != None:
            # On button press: call function/command that was given with the constructor
            self._external_callback()

class RadioButtonGroup():
    """ If you add radio buttons to a radio button group,
    then only (exactly) one can be active at a time.
    """
    def __init__(self):
        self._radio_buttons = []
        self._one_set = False

    def add(self, button: RadioButton):
        # Is the new button's state 'selected'?
        if button.state == True:
            # Is there already a button in this group that is 'selected'?
            if self._one_set:
                # Yes -> Unselect the new button
                button.state = False
            else:
                # No -> Remember that we now have a button in this group that is selected
                self._one_set = True
        
        self._radio_buttons.append(button)

    def update_buttons(self, set_button: RadioButton):
        for button in self._radio_buttons:
            if button != set_button:
                button.state = False

    def get_selected_button(self) -> RadioButton:
        for button in self._radio_buttons:
            if button.state == True:
                return button

        raise RuntimeError("No button in this radio button group is selected!")
