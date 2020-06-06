
class Meal(object):
    def __init__(self, database_content):
        # TODO: generate object of class meal from the given meal database-data
        
        self._db_content = database_content

    @property
    def database_content(self) -> str:
        return self._db_content

class Category():
    def __init__(self, name: str):
        self._name = name
        self._subcategories = []
        self._parent = None
        self._meal = None

    def printc(self, level: str = "", wire: str = "", print_db_content: bool = False):
        mealcontent = ""

        if self.has_meal() and print_db_content:
            mealcontent = f" {self._meal.database_content()}"

        print(f"{level}{wire}-- {self._name}{mealcontent}")
        
        if wire == "'":
            new_level = f"{level}     "
        else:
            new_level = f"{level}{wire}    "

        for idx,subcat in enumerate(self._subcategories):
            if idx == len(self._subcategories) - 1:
                subcat.printc(new_level, "'")
            else:
                subcat.printc(new_level, "|")

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
