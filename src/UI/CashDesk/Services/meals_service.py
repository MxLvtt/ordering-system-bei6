from tkinter import messagebox
import Templates.references as REFS
from Templates.meals import Category, Meal
from Handlers.database_handler import DatabaseHandler


class MealsService:
    NO_SPLIT = 0    # Does not split the meals into their categories at all
    SPLIT_MAIN = 1  # Splits the meals only within the first layer of categories
    SPLIT_ALL = 2   # Splits the meals among all listed categories

    COLUMN_NAMES = []
    NUM_COLUMNS = 0

    initialized = False

    def __init__(self):
        # Getting the column information for the 'meals' table
        (MealsService.NUM_COLUMNS, MealsService.COLUMN_NAMES) = DatabaseHandler.get_table_information(
            table_name=REFS.MEALS_TABLE_NAME)

        MealsService.initialized = True
    
    @staticmethod
    def meal_content_to_text(meal: Meal, indent: str = "    ") -> (str,str):
        """ Converts a string representation of the given meal and returns a tupel of two strings.

        (title,content) = MealsService.meal_content_to_text(meal)
        title: A string containing the name and (opt.) the size of the meal
        content: A multiline string containing the included extras and excluded ingredients.
        """
        size_text = ""
        if len(meal.size_objects) != 0 and meal.size_objects[0] != None and meal.size_objects[0].name != "":
            size_text = f" ({meal.size_objects[0].name})"

        amount_text = ""
        if meal.amount > 1:
            amount_text = f"{meal.amount}x "
        
        meal_title = f"{amount_text}{meal.name}{size_text}"

        meal_text = ""

        for ingredient in meal.ingredient_objects:
            if ingredient != None and ingredient.name != '':
                meal_text = f"{meal_text}{indent}- OHNE {ingredient.name}\n"

        for addon in meal.addon_objects:
            if addon != None and addon.name != '':
                meal_text = f"{meal_text}{indent}+ MIT {addon.name}\n"

        if meal_text != "" and meal_text[-1] == '\n':
            meal_text = meal_text[0:-1]

        return (meal_title, meal_text)

    @staticmethod
    def create_new_meal(category: str, name: str, base_price: float, ingredients: [], addons: [], sizes: []):
        """ ingredients, addons and sizes must be arrays of type "NamePricePair"
        """
        if not MealsService.initialized:
            return None

        # Defining sql query contents
        columns = [
            REFS.MEALS_TABLE_KATEGORIE_COLUMN,
            REFS.MEALS_TABLE_NAME_COLUMN,
            REFS.MEALS_TABLE_ZUTATEN_COLUMN,
            REFS.MEALS_TABLE_ADDONS_COLUMN,
            REFS.MEALS_TABLE_GROESSEN_COLUMN,
            REFS.MEALS_TABLE_PRICE_COLUMN
        ]

        # TODO
        ingredients_string = "NULL"
        addons_string = "NULL"
        sizes_string = "NULL"

        values = [
            f"'{category}'",
            f"'{name}'",
            f"'{ingredients_string}'", 
            f"'{addons_string}'",
            f"'{sizes_string}'",
            f"{base_price}"
        ]

        # Insert new order into the database table
        DatabaseHandler.insert_into_table(
            table_name=REFS.MEALS_TABLE_NAME,
            columns=columns, 
            values=values)

    @staticmethod
    def delete_from_table(condition: str = "", confirm: bool = True) -> bool:
        if not MealsService.initialized:
            return None

        confirmed = True

        if confirm:
            confirmed = messagebox.askyesno(
                title="Delete meal",
                message="Are you sure you want to delete this meal?",
                default='no'
            )

        if confirmed:
            DatabaseHandler.delete_from_table(
                table_name=REFS.MEALS_TABLE_NAME,
                row_filter=condition
            )
        else:
            print(f"Deleting from table '{REFS.ORDERS_TABLE_NAME}' canceled.")
            
        return confirmed

    @staticmethod
    def get_meal_by_name(name: str):
        return DatabaseHandler.select_from_table(REFS.MEALS_TABLE_NAME, row_filter=f"name={name}")

    @staticmethod
    def get_meal_by_id(id: int):
        return DatabaseHandler.select_from_table(REFS.MEALS_TABLE_NAME, row_filter=f"id={id}")

    @staticmethod
    def get_raw_meals(order_by: str = ""):
        """ Returns an array of all meals in the database in their raw form.
        """
        return DatabaseHandler.select_from_table(REFS.MEALS_TABLE_NAME, order_by=order_by)

    @staticmethod
    def get_meal_objects(order_by: str = ""):
        meal_objects = []
        raw_meals = MealsService.get_raw_meals(order_by=order_by)
        for raw_meal in raw_meals:
            meal_obj = Meal(raw_meal, MealsService.COLUMN_NAMES)
            meal_objects.append(meal_obj)
        return meal_objects

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
