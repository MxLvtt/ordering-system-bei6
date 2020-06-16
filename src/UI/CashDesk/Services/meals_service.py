import Templates.references as REFS
from Templates.meals import Category, Meal
from Handlers.database_handler import DatabaseHandler


class MealsService:
    NO_SPLIT = 0    # Does not split the meals into their categories at all
    SPLIT_MAIN = 1  # Splits the meals only within the first layer of categories
    SPLIT_ALL = 2   # Splits the meals among all listed categories

    COLUMN_NAMES = []
    NUM_COLUMNS = 0

    def __init__(self):
        # Getting the column information for the 'meals' table
        (MealsService.NUM_COLUMNS, MealsService.COLUMN_NAMES) = DatabaseHandler.get_table_information(
            table_name=REFS.MEALS_TABLE_NAME)

    @staticmethod
    def get_meal_by_name(name: str):
        return DatabaseHandler.send_sql_command(
            f"SELECT * FROM {REFS.MEALS_TABLE_NAME} WHERE name = {name}")

    @staticmethod
    def get_meal_by_id(id: int):
        return DatabaseHandler.send_sql_command(
            f"SELECT * FROM {REFS.MEALS_TABLE_NAME} WHERE id = {id}")

    @staticmethod
    def get_raw_meals():
        """ Returns an array of all meals in the database in their raw form.
        """
        return DatabaseHandler.select_from_table(REFS.MEALS_TABLE_NAME)

    @staticmethod
    def split_meals_by_categories(meals, splitmode: int) -> Category:
        """ Splits the given list of meals (in raw format) up into their categories
        and return the root category.

        splitmode: NO_SPLIT, SPLIT_MAIN, SPLIT_ALL
        """
        root: Category = Category("root", splitmode)

        # Create Category-Tree by adding subcategories to root and so on
        for meal in meals:
            category_value = meal[1]
            name_value = meal[2]

            # Extract subcategories and split up into a separate array -> ['Getraenke', 'Kalt', 'Alkoholfrei']
            prev_cat = root

            # Create subcategory tree if needed/wanted
            if category_value != None and splitmode != MealsService.NO_SPLIT:
                subcats_arr = category_value.split('/')

                # For every category in subcategories
                for index, subcat in enumerate(subcats_arr):
                    # Skip all deeper categories if in "SPLIT_MAIN" mode
                    if index < 1 or splitmode != MealsService.SPLIT_MAIN:
                        # Add the subcategory to the previous category (ignore if existant)
                        # And set the previous category to the current subcategory
                        prev_cat = prev_cat.add(subcat)

            # Create object of class Meal with the data given from the database (-> 'meal')
            meal_object: Meal = Meal(meal, MealsService.COLUMN_NAMES)

            # Create on last subcategory named like the meal itself
            # And add the meal object to this new subcategory
            prev_cat.add(name_value).insert_meal(meal_object)

        return root
