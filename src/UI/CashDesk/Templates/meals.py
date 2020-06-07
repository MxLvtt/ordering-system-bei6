import Templates.references as REFS


class Meal(object):
    def __init__(self, database_content, db_column_names: []):
        self._db_content = database_content

        self._id = database_content[db_column_names.index(
            REFS.MEALS_TABLE_ID_COLUMN)]
        self._category = database_content[db_column_names.index(
            REFS.MEALS_TABLE_KATEGORIE_COLUMN)]
        self._name = database_content[db_column_names.index(
            REFS.MEALS_TABLE_NAME_COLUMN)]
        self._ingredients = database_content[db_column_names.index(
            REFS.MEALS_TABLE_ZUTATEN_COLUMN)]
        self._addons = database_content[db_column_names.index(
            REFS.MEALS_TABLE_ADDONS_COLUMN)]
        self._sizes = database_content[db_column_names.index(
            REFS.MEALS_TABLE_GROESSEN_COLUMN)]

    @property
    def database_content(self) -> str:
        return self._db_content

    @property
    def category_raw(self) -> str:
        return self._category

    @property
    def category(self) -> []:
        if self._category == None:
            return []
        return self._category.split(REFS.CATEGORY_DELIMITER)

    @property
    def name(self) -> str:
        return self._name

    @property
    def ingredients_raw(self) -> str:
        return self._ingredients

    @property
    def ingredients(self) -> []:
        if self._ingredients == None:
            return []
        return self._ingredients.split(REFS.LIST_DELIMITER)

    @property
    def addons_raw(self) -> str:
        return self._addons

    @property
    def addons(self) -> []:
        if self._addons == None:
            return []
        return self._addons.split(REFS.LIST_DELIMITER)

    @property
    def sizes_raw(self) -> str:
        return self._sizes

    @property
    def sizes(self) -> []:
        if self._sizes == None:
            return []
        return self._sizes.split(REFS.LIST_DELIMITER)


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
