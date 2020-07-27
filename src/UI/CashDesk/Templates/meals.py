import Templates.references as REFS


class Meal(object):
    DB_COLUMN_NAMES = None

    def __init__(self, database_content, db_column_names: []):
        if len(database_content) != len(db_column_names):
            raise RuntimeError("Database content and column names differ in size.")

        self._db_content = database_content

        if Meal.DB_COLUMN_NAMES == None: # and db_column_names != Meal.DB_COLUMN_NAMES:
            Meal.DB_COLUMN_NAMES = db_column_names

        self._id = -1
        self._category_raw = None
        self._name = ""
        self._ingredients_raw = None
        self._addons_raw = None
        self._sizes_raw = None
        self._price = 0.0
        self._amount = 1

        try:
            self._id = int(database_content[db_column_names.index(
                REFS.MEALS_TABLE_ID_COLUMN)])
        except:
            pass

        try:
            self._category_raw = database_content[db_column_names.index(
                REFS.MEALS_TABLE_KATEGORIE_COLUMN)]
        except:
            pass

        try:
            self._name = database_content[db_column_names.index(
                REFS.MEALS_TABLE_NAME_COLUMN)]
        except:
            pass

        try:
            self._ingredients_raw = database_content[db_column_names.index(
                REFS.MEALS_TABLE_ZUTATEN_COLUMN)]
        except:
            pass

        try:
            self._addons_raw = database_content[db_column_names.index(
                REFS.MEALS_TABLE_ADDONS_COLUMN)]
        except:
            pass

        try:
            self._sizes_raw = database_content[db_column_names.index(
                REFS.MEALS_TABLE_GROESSEN_COLUMN)]
        except:
            pass

        try:
            self._price = float(database_content[db_column_names.index(
                REFS.MEALS_TABLE_PRICE_COLUMN)])
        except:
            pass

        try:
            self._amount = int(database_content[db_column_names.index(
                REFS.MEALS_AMOUNT_IDENTIFIER)])
        except:
            pass

        # CATEGORY

        if self._category_raw == None:
            self._category = []
        else:
            self._category = self._category_raw.split(REFS.CATEGORY_DELIMITER)

        # INGREDIENTS

        self._ingredients = []

        if self._ingredients_raw != None:
            self._ingredients = self._ingredients_raw.split(
                REFS.LIST_DELIMITER)

        # ADDONS

        self._addons = []

        if self._addons_raw != None:
            self._addons = self._addons_raw.split(REFS.LIST_DELIMITER)

        # SIZES

        self._sizes = []

        if self._sizes_raw != None:
            self._sizes = self._sizes_raw.split(REFS.LIST_DELIMITER)
            

    @property
    def database_content(self) -> str:
        return self._db_content

    @property
    def category_raw(self) -> str:
        return self._category_raw

    @property
    def category(self) -> []:
        return self._category

    @property
    def name(self) -> str:
        return self._name

    @property
    def ingredients_raw(self) -> str:
        return self._ingredients_raw

    @property
    def ingredients(self) -> []:
        return self._ingredients

    @property
    def ingredient_objects(self) -> []:
        self._ingredient_objects = []
        for ingr in self._ingredients:
            self._ingredient_objects.append(NamePricePair(ingr))
        return self._ingredient_objects

    @property
    def addons_raw(self) -> str:
        return self._addons_raw

    @property
    def addons(self) -> []:
        return self._addons

    @property
    def addon_objects(self) -> []:
        self._addon_objects = []
        for addon in self._addons:
            self._addon_objects.append(NamePricePair(addon))
        return self._addon_objects

    @property
    def sizes_raw(self) -> str:
        return self._sizes_raw

    @property
    def sizes(self) -> []:
        return self._sizes

    @property
    def size_objects(self) -> []:
        self._size_objects = []
        for size in self._sizes:
            self._size_objects.append(NamePricePair(size))
        return self._size_objects

    @property
    def price(self) -> float:
        return self._price

    @property
    def price_str(self) -> str:
        return "{:.2f}".format(self._price)

    @property
    def amount(self) -> int:
        return self._amount

    @amount.setter
    def amount(self, amount: int):
        self._amount = amount

    @staticmethod
    def COPY(source_meal: 'Meal') -> 'Meal':
        return Meal(source_meal.database_content, Meal.DB_COLUMN_NAMES)

    def copy(self) -> 'Meal':
        return Meal(self.database_content, Meal.DB_COLUMN_NAMES)
    
    def calculate_single_price(self) -> float:
        base_price = self.price

        if len(self._sizes) != 0 and self._sizes[0] != '':
            if self.size_objects[0].price != 0.0:
                base_price = self.size_objects[0].price

        ingr_price = 0.0

        for idx,ingr in enumerate(self._ingredients):
            if ingr != '':
                ingr_price = ingr_price + self.ingredient_objects[idx].price

        addon_price = 0.0

        for idx,addon in enumerate(self._addons):
            if addon != '':
                addon_price = addon_price + self.addon_objects[idx].price

        return (base_price + addon_price - ingr_price)

    def calculate_whole_price(self) -> float:
        return self.calculate_single_price() * self.amount

    @property
    def formatted_single_price(self) -> str:
        return "{:.2f}".format(self.calculate_single_price())
        
    @property
    def formatted_whole_price(self) -> str:
        return "{:.2f}".format(self.calculate_whole_price())
        
    def get_meal_code(self) -> str:
        """Returns the code for this meal (-configuration).

        The code contains information on the type of meal, it's removed ingredients,
        size and added extras, so that it can be easily stored in the database.

        Form: name%ingredient1;ingredient2;ingredientN%addon1;addon2;addonN%size
        """
        meal_code = f"{self.name}{REFS.MEAL_CODE_DELIMITER}"

        for idx, ingr in enumerate(self.ingredients):
            if idx == len(self.ingredients) - 1:
                meal_code = f"{meal_code}{ingr}"
            else:
                meal_code = f"{meal_code}{ingr}{REFS.LIST_DELIMITER}"

        meal_code = f"{meal_code}{REFS.MEAL_CODE_DELIMITER}"

        for idx, addon in enumerate(self.addons):
            if idx == len(self.addons) - 1:
                meal_code = f"{meal_code}{addon}"
            else:
                meal_code = f"{meal_code}{addon}{REFS.LIST_DELIMITER}"

        meal_code = f"{meal_code}{REFS.MEAL_CODE_DELIMITER}"

        if len(self.sizes) != 0:
            meal_code = f"{meal_code}{self.sizes[0]}"

        meal_code = f"{meal_code}{REFS.MEAL_CODE_DELIMITER}{self.price}"

        meal_code = f"{meal_code}{REFS.MEAL_CODE_DELIMITER}{self.amount}"

        return meal_code

    @staticmethod
    def get_meal_from_code(meal_code: str) -> 'Meal':
        return Meal(
            meal_code.split(REFS.MEAL_CODE_DELIMITER),
            [
                REFS.MEALS_TABLE_NAME_COLUMN,
                REFS.MEALS_TABLE_ZUTATEN_COLUMN,
                REFS.MEALS_TABLE_ADDONS_COLUMN,
                REFS.MEALS_TABLE_GROESSEN_COLUMN,
                REFS.MEALS_TABLE_PRICE_COLUMN,
                REFS.MEALS_AMOUNT_IDENTIFIER
            ]
        )


class NamePricePair():
    def __init__(self, raw: str):
        result: [] = raw.split(REFS.MEAL_PRICE_DELIMITER)

        if result == None or len(result) == 0:
            raise RuntimeError("Creating name price pair failed.") 

        self._name: str = result[0]
        self._price: float = 0.0

        if len(result) == 2:
            self._price = float(result[1])

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @property
    def price_str(self) -> float:
        return "{:.2f}".format(self._price)


class Category():
    def __init__(self, name: str, splitmode: int = -1):
        self._name = name
        self._subcategories = []
        self._parent = None
        self._meal = None
        self._splitmode = splitmode

    def printc(self, level: str = "", wire: str = "", print_db_content: bool = False):
        mealcontent = ""

        if self.has_meal() and print_db_content:
            mealcontent = f" {self._meal.database_content()}"

        print(f"{level}{wire}-- {self._name}{mealcontent}")

        if wire == "'":
            new_level = f"{level}     "
        else:
            new_level = f"{level}{wire}    "

        for idx, subcat in enumerate(self._subcategories):
            if idx == len(self._subcategories) - 1:
                subcat.printc(new_level, "'")
            else:
                subcat.printc(new_level, "|")

    @property
    def splitmode(self) -> int:
        return self._splitmode

    @property
    def name(self) -> str:
        return self._name

    @property
    def subcategories(self):
        return self._subcategories

    @property
    def parent(self):
        return self._parent

    @property
    def meal(self):
        return self._meal

    def has_subcategory(self, name: str) -> (bool, 'Category'):
        for sub in self._subcategories:
            if sub.name == name:
                return (True, sub)

        return (False, None)

    def has_meal(self) -> bool:
        """ Return true, if this category contains the meal object.
        """
        return self._meal != None

    def insert_meal(self, meal: Meal) -> Meal:
        if self._meal != None:
            print("[WARN] This category already has a meal asserted to it!")
        else:
            self._meal = meal

        return self._meal

    def insert(self, subcategory: 'Category') -> 'Category':
        """ Adds the given category as a subcategory.
        Sets the subcategories parent to itself. 
        Returns: the given subcategory.
        """
        subcategory.set_parent(self)
        self._subcategories.append(subcategory)
        return subcategory

    def add(self, subcategory: str) -> 'Category':
        """ Search in array, if subcategory already exists.
        If so: just return it, otherwise: create and return it.
        """
        (exists, subcat) = self.has_subcategory(subcategory)

        if exists:
            return subcat

        new_subcat = Category(subcategory)
        return self.insert(new_subcat)

    def set_parent(self, parent: 'Category') -> 'Category':
        """ Updates the parent category with the given Category object
        """
        self._parent = parent
        return self
