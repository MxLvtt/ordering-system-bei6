from tkinter import *

class ContentTemplate(Frame):
    """ Template class from which the view-classes will inherit from. Handles the hide- and show-logic and holds #
    the 'title' property of the view.
    """
    def __init__(self, parent, title, background="white", shown: bool = False):
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

        # Initialize visibility-state
        if not shown:
            self.hide_view()
        else:
            self.show_view()

    ### ------------------- PROPERTIES ------------------- ###

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
            self._is_hidden = True

    def show_view(self):
        """ Shows this view (again).
        """
        if self._is_hidden:
            self.pack(side=TOP,expand=1,fill='both')#,padx=5,pady=5)
            self._is_hidden = False
