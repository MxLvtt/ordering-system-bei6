from tkinter import PhotoImage

class IMAGES():
    BASE_PATH = r"D:\dev\ordering-system-bei5\src\UI\CashDesk\img\\"

    CHECK_MARK = f"{BASE_PATH}checkmark.png"
    CHECK_MARK_DARK = f"{BASE_PATH}checkmark_dark.png"

    EXIT = f"{BASE_PATH}exit.png"
    
    ADD = f"{BASE_PATH}add.png"
    EDIT = f"{BASE_PATH}edit.png"
    
    BURGER = f"{BASE_PATH}burger.png"
    BURGER_DARK = f"{BASE_PATH}burger_dark.png"
    
    BACK = f"{BASE_PATH}back.png"
    NEXT = f"{BASE_PATH}next.png"
    DOWN = f"{BASE_PATH}down.png"
    UP = f"{BASE_PATH}up.png"

    UNDO = f"{BASE_PATH}undo.png"
    UNDO_LIGHT = f"{BASE_PATH}undo_light.png"

    HISTORY = f"{BASE_PATH}history.png"
    IN_PROGRESS = f"{BASE_PATH}in_progress.png"
    SETTINGS = f"{BASE_PATH}settings.png"
    
    TRASH_CAN = f"{BASE_PATH}trashcan.png"
    ORDER = f"{BASE_PATH}order.png"

    CLOSE = f"{BASE_PATH}close.png"
    CLOSE_ALL = f"{BASE_PATH}close_all.png"
    CLOSE_LIGHT = f"{BASE_PATH}close_light.png"
    CLOSE_DARK = f"{BASE_PATH}close_dark.png"

    def __init__(self):
        pass

    @staticmethod
    def create(filename: str):
        img = PhotoImage(file=filename)
        return img