from Handlers.meals_handler import Meal

class Category():
    def __init__(self, name: str):
        self._name = name
        self._subcategories = []
        self._parent = None
        self._meal = None

    def name(self) -> str:
        return self._name

    def subcategories(self):
        return self._subcategories

    def parent(self):
        return self._parent

    def has_subcategory(self, name: str) -> (bool, Category):
        for sub in self._subcategories:
            if sub.name() is name:
                return (True, sub)
        
        return (False, None)

    def has_meal(self) -> (bool, Meal):
        """ Return true, if this category contains the meal object and no further subcategories.
        """
        exists = (len(self._subcategories) == 0) and (self._meal != None)

        return (exists, self._meal)

    def insert_meal(self, meal: Meal) -> Meal:
        if self._meal != None:
            print("[WARN] This category already has a meal asserted to it!")
        else:
            self._meal = meal

        return self._meal

    def insert(self, subcategory: Category) -> Category:
        """ Adds the given category as a subcategory.
        Sets the subcategories parent to itself. 
        Returns: the given subcategory.
        """
        subcategory.set_parent(self)
        self._subcategories.append(subcategory)
        return subcategory

    def add(self, subcategory: str) -> Category:
        """ Search in array, if subcategory already exists.
        If so: just return it, otherwise: create and return it.
        """
        (exists, subcat) = self.has_subcategory(subcategory)
        
        if exists:
            return subcat

        new_subcat = Category(subcategory)
        return self.insert(new_subcat)

    def set_parent(self, parent: Category) -> Category:
        """ Updates the parent category with the given Category object
        """
        self._parent = parent
        return self