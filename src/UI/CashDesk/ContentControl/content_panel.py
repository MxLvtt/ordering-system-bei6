from tkinter import *
from ContentControl.content_template import ContentTemplate
from ContentControl.add_order_view import AddOrderView
from ContentControl.active_orders_view import ActiveOrdersView

class ContentPanel(Frame):
    def __init__(self, parent, width=0, height=0, background="#EFEFEF"):
        super().__init__(
            master=parent,
            cnf={},
            width=width,
            height=height,
            background=background
        )

        self.VIEWS = []

        self.pack_propagate(0)

        self.add_order_content: AddOrderView = AddOrderView(
            parent=self,
            background="gray",
            shown=True
        )
        self.VIEWS.append(self.add_order_content)

        self._active_view = self.add_order_content

        self.active_orders_content: ActiveOrdersView = ActiveOrdersView(
            parent=self,
            background="yellow"
        )
        self.VIEWS.append(self.active_orders_content)

    def active_view(self):
        return self._active_view

    def _show_content(self, content: ContentTemplate):
        for _view in self.VIEWS:
            if not _view is content:
                _view.hide_view()
        content.show_view()
        self._active_view = content

    def show_add_order_view(self):
        self._show_content(self.add_order_content)

    def is_add_order_shown(self) -> bool:
        return self.add_order_content.is_shown()

    def show_active_orders_view(self):
        self._show_content(self.active_orders_content)

    def is_active_orders_shown(self) -> bool:
        return self.active_orders_content.is_shown()
