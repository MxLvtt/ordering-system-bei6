from Templates.cbutton import CButton

class ToggleButton(CButton):
    def __init__(
        self,
        parent,
        image,
        highlight_image,
        command,
        bg,
        highlight,
        initial_state: bool = False,
        group = None,
        width=2.0,
        height=1.0,
        fg=CButton.DARK,
        row=0,
        column=0,
        spaceX=(0.0,0.0), # As a multiple of the buttons standard SIZE
        spaceY=(0.0,0.0)  # As a multiple of the buttons stamdard SIZE
    ):
        super().__init__(
            parent=parent,
            image=image,
            command=self._button_command,
            width=width, height=height,
            fg=fg, bg=bg,
            row=row, column=column,
            spaceX=spaceX, spaceY=spaceY
        )

        self._unselect_background = bg
        self._unselect_image = image

        self._select_background = highlight
        self._select_image = highlight_image

        self._state: bool = not initial_state
        self.state = initial_state

        self._group: ToggleButtonGroup = group

        if group != None:
            group.add(self)

        self._external_callback = command

    @property
    def state(self) -> bool:
        return self._state

    @state.setter
    def state(self, new_state):
        if self._state != new_state:
            self._state = new_state

            if self._state == True:
                self.config(background=self._select_background)
                self.config(image=self._select_image)
            else:
                self.config(background=self._unselect_background)
                self.config(image=self._unselect_image)

    def _set_state(self):
        self.state = True

    def _reset_state(self):
        self.state = False

    def _button_command(self):
        if self._external_callback != None:
            # On button press: call function/command that was given with the constructor
            self._external_callback()

        # Then: Change the state of the toggle
        if self.state == True:
            self._reset_state()
        else:
            self._set_state()
            if self._group != None:
                self._group.update_buttons(set_button=self)

class ToggleButtonGroup():
    """ If you add toggle buttons to a toggle button group,
    then only one can be active at a time.
    """

    def __init__(self):
        self._toggle_buttons = []

    def add(self, tbutton: ToggleButton):
        self._toggle_buttons.append(tbutton)

    def update_buttons(self, set_button: ToggleButton):
        for tbutton in self._toggle_buttons:
            if tbutton != set_button:
                tbutton._reset_state()
