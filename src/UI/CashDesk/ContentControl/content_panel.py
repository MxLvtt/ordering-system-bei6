from tkinter import *
from ContentControl.content_template import ContentTemplate
from ContentControl.add_order_view import AddOrderView
from ContentControl.active_orders_view import ActiveOrdersView
from Templates.cbutton import CButton

class ContentPanel(Frame):
    """ Represents the main view of the cash desk UI. Holds and manages the different views of the UI
    and provides useful functionality. It acts as a container for the views.
    """
    def __init__(self, parent, width=0, height=0, background="#EFEFEF"):
        super().__init__(
            master=parent,
            cnf={},
            width=width,
            height=height,
            background=background
        )

        # The list of all available views
        self.VIEWS = []

        # To prevent the content panel from collapsing because of the added views. 
        self.pack_propagate(0)

        ## ------- ADD ORDER VIEW ------- ##

        self.add_order_content: AddOrderView = AddOrderView(
            parent=self,
            background=CButton.WHITE,
            shown=True # Set this view to be shown at the beginning
        )
        # Add the view to the list
        self.VIEWS.append(self.add_order_content)

        # Set this view to be the currently active one
        self._active_view = self.add_order_content

        ## ------- ACTIVE ORDERS VIEW ------- ##

        self.active_orders_content: ActiveOrdersView = ActiveOrdersView(
            parent=self,
            background=CButton.WHITE
        )
        # Add the view to the list
        self.VIEWS.append(self.active_orders_content)

    ### ------------------- PROPERTIES ------------------- ###

    @property
    def active_view(self):
        return self._active_view

    ### ------------------- MAIN METHODS ------------------- ###

    def show_add_order_view(self):
        self._show_content(self.add_order_content)

    def show_active_orders_view(self):
        self._show_content(self.active_orders_content)

    ### ------------------- CHECK METHODS ------------------- ###

    def is_add_order_shown(self) -> bool:
        return self.add_order_content.is_shown

    def is_active_orders_shown(self) -> bool:
        return self.active_orders_content.is_shown

    ### ------------------- HELPER METHODS ------------------- ###

    def _show_content(self, content: ContentTemplate):
        for _view in self.VIEWS:
            if not _view is content:
                _view.hide_view()
        content.show_view()
        self._active_view = content
