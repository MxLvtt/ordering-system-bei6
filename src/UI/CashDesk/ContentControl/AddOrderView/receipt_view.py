import os

from tkinter import *
from tkinter import messagebox
from functools import partial
from ContentControl.AddOrderView.added_meal_tile import AddedMealTile
from EventHandler.Event import Event
from Templates.radio_button import RadioButton, RadioButtonGroup
from Templates.fonts import Fonts
from Templates.scroll_list import ScrollList
from Templates.scrollable import Scrollable
from Services.orders_service import OrdersService
from Templates.images import IMAGES 
import Templates.references as REFS 


class ReceiptView(Frame):
    def __init__(self, parent, background, shown: bool = False, order = None):
        super().__init__(
            master=parent,
            cnf={},
            background='#696969'
        )

        self.parent = parent
        self.table = None
        self.scrolllist = None

        # Assure that the frame won't resize with the contained widgets
        self.pack_propagate(0)
        self.grid_propagate(0)

        # Private members
        self._is_hidden = shown
        self._background = background

        self._right_container = Frame(
            master=self,
            background='#696969'
        )
        self._right_container.pack(side=RIGHT, fill='y')

        self._export_img = IMAGES.create(IMAGES.EXPORT)

        self._export_button = Button(
            master=self._right_container,
            image=self._export_img,
            command=self._export_receipt,
            background=REFS.LIGHT_GRAY
        )
        self._export_button.pack(side=TOP, padx=5, pady=5)

        # Initialize visibility-state
        if not shown:
            self.hide_view()
        else:
            self.show_view(order)

    @property
    def is_shown(self) -> bool:
        return not self._is_hidden

    @property
    def receipt(self):
        return self._receipt

    def _export_receipt(self):
        try:
            filename = f"{os.curdir}/{REFS.RECEIPTS_FOLDER_NAME}/rcpt_{self.receipt.order.id}_{self.receipt.order.timestamp}.txt"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            fd = open(filename, "w+")
            for line in self.receipt.raw_lines:
                fd.write(f"{line}\n")
            fd.close()

            self._export_button.config(background=REFS.LIGHT_GREEN)
        except OSError as err:
            messagebox.showerror("Export failed", err.strerror)

    def _update_view(self, order):
        self._export_button.config(background=REFS.LIGHT_GRAY)

        if self.scrolllist == None or self.table == None:
            self.update()
            width = self.parent.winfo_width()

            self.table = Frame(
                master=self, 
                background='#696969', 
                width=int(width/3)
            )

            self.scrolllist = ScrollList(
                parent=self.table,
                spacing=0,
                background='#696969'
            )
        else:
            self.scrolllist.remove_all()

        self._receipt = Receipt(
            parent=self.scrolllist,
            order=order
        )

        self._receipt.height = self._receipt.winfo_reqheight()

        self.table.config(width=self._receipt.winfo_reqwidth())
        self.table.pack(side=TOP, fill='y', expand=1, pady=10)

        self.scrolllist.add_row(self._receipt, update=False)
        self.scrolllist.update_view()

    def hide_view(self):
        if self._is_hidden:
            return
        
        self.pack_forget()
        self._is_hidden = True

    def show_view(self, order):
        if not self._is_hidden:
            return

        if order == None:
            raise RuntimeError("Order must not be of Nonetype.")

        self._update_view(order)

        self.pack(side=TOP, expand=1, fill='both')
        self._is_hidden = False

class Receipt(Scrollable):
    DEL = "$"
    LARGE = "L"
    SMALL = "S"
    BOLD = "B"
    SEPARATOR = "==="
    EXPANDER = "..."
    EXPANDER_CHAR = "."

    def __init__(self, parent, order, background='white'):
        super().__init__(
            parent=parent,
            height=800,
            background=background
        )

        self._order = order

        self._timestamp_str = OrdersService.convert_timestamp(
            timestamp=order.timestamp,
            extended=True
        )

        self._background = background

        ########## COLUMNS ##########

        self.text_container = Frame(
            master=self,
            background=background
        )
        self.text_container.pack(side=TOP, fill='x', padx=5, pady=5)

        receipt_text_lines = self.create_text(order, raw_array=True)
        self._raw_lines = []

        Fonts.family(family="Consolas", sustain=True)

        for line in receipt_text_lines:
            self.row_frame = Frame(
                master=self.text_container,
                background=background
            )
            self.row_frame.pack(side=TOP, fill='x')
            
            content = line
            line_components = line.split(Receipt.DEL)
            bold = False
            size = 1

            if len(line_components) >= 1:
                content = line_components[len(line_components) - 1]
                for index,comp in enumerate(line_components):
                    if index != (len(line_components) - 1):
                        if comp == Receipt.LARGE:
                            size = 2
                        elif comp == Receipt.SMALL:
                            size = 0
                        elif comp == Receipt.BOLD:
                            bold = True

            font = Fonts.medium(bold=bold)

            if size == 0:
                font = Fonts.small(bold=bold)
            elif size == 2:
                font = Fonts.xxlarge(bold=bold)

            self._raw_lines.append(content)
            
            self._text = Label(
                master=self.row_frame,
                text=content,
                background=background,
                font=font
            )
            self._text.pack(side=LEFT)#, padx=5, pady=(5,0))

        Fonts.family(family=Fonts.DEFAULT_FAMILY, sustain=False)

        self.update()

    @property
    def raw_lines(self) -> []:
        return self._raw_lines

    @property
    def order(self):
        return self._order

    def create_text(self, order, raw_array: bool = False):
        """ A line is constructed like this:

        "L%B%===" -> Separator line with large and bold letters

        "S%Hello World." -> "Hello World." with a small font
        """
        self.longest_line = 0
        self.lines: [] = []
        self.separator_lines: [] = []
        self.separator_lines_slim: [] = []
        self.expander_lines: [] = []
        self.expander_lines_space: [] = []

        def _attach(line, modifier: str = "") -> int:
            self.lines.append(f"{modifier}{line}")

            if len(line) > self.longest_line:
                self.longest_line = len(line)

            return len(self.lines) - 1

        def _attach_separator(modifier: str = "", slim: bool = False) -> int:
            if slim:
                self.separator_lines_slim.append(len(self.lines))
            else:
                self.separator_lines.append(len(self.lines))
            return _attach(f"{Receipt.SEPARATOR}", modifier=modifier)

        def _attach_expander(left: str, right: str, modifier: str = "", space: bool = False) -> int:
            if space:
                self.expander_lines_space.append(len(self.lines))
            else:
                self.expander_lines.append(len(self.lines))

            return _attach(f"{left} {Receipt.EXPANDER} {right}", modifier=modifier)

        #### GENERATING CONTENT

        # TITLE
        _attach(f"{REFS.RESTAURANT_NAME}", f"{Receipt.LARGE}{Receipt.DEL}" \
            f"{Receipt.BOLD}{Receipt.DEL}")
        _attach_expander(
            left=f"{REFS.EMPLOYEE_NAME}",
            right=f"{self._timestamp_str}",
            modifier=f"{Receipt.BOLD}{Receipt.DEL}",
            space=True
        )

        # ORDER TYPE
        _attach_expander(
            left="",
            right=f"{OrdersService.convert_form(order.form)}, #{order.id}",
            space=True
        )

        # SEPARATOR
        _attach_separator()

        indent = "   "

        # MEALS
        for meal in order.meals:
            # Meal amount, name and whole price
            _attach_expander(
                left=f"{meal.amount}x {meal.name}",
                right=f"{meal.formatted_whole_price} {REFS.CURRENCY}",
                modifier=f"{Receipt.BOLD}{Receipt.DEL}"
            )

            if meal.calculate_whole_price() != meal.calculate_single_price():
                _attach_expander(
                    left=f"{indent}{REFS.MEALS_SINGLE_PRICE_SHORT}",
                    right=f"{meal.formatted_single_price} {REFS.CURRENCY}"
                )

            # Only show base price, if it's different from the whole price for this meal
            if meal.price != meal.calculate_whole_price():
                # Meal base price, with default size and no extras etc.
                _attach_expander(
                    left=f"{indent}{REFS.MEALS_BASE_PRICE_SHORT}",
                    right=f"{meal.price_str} {REFS.CURRENCY}"
                )

            # Show ingredients
            for ingr_obj in meal.ingredient_objects:
                ingr_price = ""
                if ingr_obj.price != 0.0:
                    ingr_price = f"-{ingr_obj.price_str} {REFS.CURRENCY}"
                _attach_expander(
                    left=f"{indent}- {ingr_obj.name}",
                    right=f"{ingr_price}"
                )

            # Show extras
            for add_obj in meal.addon_objects:
                addon_price = ""
                if add_obj.price != 0.0:
                    addon_price = f"{add_obj.price_str} {REFS.CURRENCY}"
                _attach_expander(
                    left=f"{indent}+ {add_obj.name}",
                    right=f"{addon_price}"
                )

        # SEPARATOR
        _attach_separator(slim=True)

        # TOTAL PRICE
        order_price = order.calculate_price()
        order_price_str = "{:.2f}".format(order_price)

        _attach_expander(
            left=f"{REFS.MEALS_TOTAL_PRICE_SHORT}",
            right=f"{order_price_str} {REFS.CURRENCY}",
            modifier=f"{Receipt.BOLD}{Receipt.DEL}",
            space=True
        )

        _attach(line="")

        # MWST ANTEIL
        mswt_anteil = order_price * (REFS.MWST_PROZENT / 100.0)
        mswt_anteil_str = "{:.2f}".format(mswt_anteil)

        _attach_expander(
            left=REFS.MWST_TEXT_RECEIPT.format(REFS.MWST_PROZENT),
            right=f"{mswt_anteil_str} {REFS.CURRENCY}",
            space=True
        )

        # NETTO PRICE
        netto_price = order_price - mswt_anteil
        netto_price_str = "{:.2f}".format(netto_price)

        _attach_expander(
            left=REFS.MEALS_NETTO_PRICE_SHORT,
            right=f"{netto_price_str} {REFS.CURRENCY}",
            space=True
        )

        # SEPARATOR
        _attach_separator()

        #### ADAPT SEPARATOR AND EXPANDER LINES
        separator_line = ''.join([char*self.longest_line for char in "="])
        for sep_id in self.separator_lines:
            self.lines[sep_id] = separator_line
            
        separator_line_slim = ''.join([char*self.longest_line for char in "-"])
        for sep_id in self.separator_lines_slim:
            self.lines[sep_id] = separator_line_slim

        def _expand_line(exp_id, _exp_char):
            line_split = self.lines[exp_id].split(Receipt.DEL)

            line_length = len(self.lines[exp_id]) - len(Receipt.EXPANDER)
            split_line = self.lines[exp_id].split(Receipt.EXPANDER)
            missing_space = self.longest_line - line_length + ((len(line_split) - 1) * 2)

            _expander = ''.join([char*missing_space for char in _exp_char])

            expander_line = f"{split_line[0]}{_expander}{split_line[1]}"
            self.lines[exp_id] = expander_line

        for exp_id in self.expander_lines:
            _exp_char = Receipt.EXPANDER_CHAR
            _expand_line(exp_id, _exp_char)

        for exp_id in self.expander_lines_space:
            _exp_char = " "
            _expand_line(exp_id, _exp_char)

        if raw_array:
            return self.lines
        else:
            return "\n".join(self.lines)

