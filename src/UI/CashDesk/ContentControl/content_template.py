from tkinter import *

class ContentTemplate(Frame):
    """ Template class from which the view-classes will inherit from. Handles the hide- and show-logic and holds #
    the 'title' property of the view.
    """
    def __init__(self, parent, title, toolbar_container: Frame, background="white", shown: bool = False):
        super().__init__(
            master=parent,
            cnf={},
            background=background
        )

        # Assure that the frame won't resize with the contained widgets
        self.pack_propagate(0)
        self.grid_propagate(0)

        # Private members
        self._title = title
        self._is_hidden = shown
        self._toolbar_container = toolbar_container

        self._toolbar = Frame(master=toolbar_container,background=background)
        # self._toolbar.grid(row=0, column=0, sticky='nsew')
        self._toolbar.pack(side=TOP, fill='x')

        # Initialize visibility-state
        if not shown:
            self.hide_view()
        else:
            self.show_view()

    ### ------------------- PROPERTIES ------------------- ###

    @property
    def toolbar(self) -> Frame:
        return self._toolbar

    @property
    def title(self) -> bool:
        return self._title

    @property
    def is_shown(self) -> bool:
        return not self._is_hidden

    ### ------------------- MAIN METHODS ------------------- ###

    def hide_view(self):
        """ Hides this view from the user. Content is still active.
        """
        if not self._is_hidden:
            self.pack_forget()
            # self.toolbar.grid_forget()
            self.toolbar.pack_forget()
            self._is_hidden = True

    def show_view(self):
        """ Shows this view (again).
        """
        if self._is_hidden:
            self.pack(side=TOP,expand=1,fill='both')#,padx=5,pady=5)
            # self.toolbar.grid(row=0, column=0, sticky='nsew')
            self._toolbar.pack(side=TOP, fill='x')
            self._is_hidden = False
