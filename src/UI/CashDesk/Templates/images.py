from tkinter import PhotoImage
from PIL import ImageTk, Image
import Templates.references as REFS

class IMAGES():
    BASE_PATH = REFS.BASEPATH + r"/img/"

    CHECK_MARK = f"{BASE_PATH}checkmark.png"
    CHECK_MARK_DARK = f"{BASE_PATH}checkmark_dark.png"

    EXIT = f"{BASE_PATH}exit.png"
    NAVIGATION = f"{BASE_PATH}nav.png"
    
    ADD = f"{BASE_PATH}add.png"
    EXPORT = f"{BASE_PATH}export.png"
    EDIT = f"{BASE_PATH}edit.png"
    
    BURGER = f"{BASE_PATH}burger.png"
    BURGER_DARK = f"{BASE_PATH}burger_dark.png"
    
    BACK = f"{BASE_PATH}back.png"
    NEXT = f"{BASE_PATH}next.png"
    DOWN = f"{BASE_PATH}down.png"
    UP = f"{BASE_PATH}up.png"

    RESET_I = f"{BASE_PATH}reset_i.png"

    UNDO = f"{BASE_PATH}undo.png"
    UNDO_LIGHT = f"{BASE_PATH}undo_light.png"

    HISTORY = f"{BASE_PATH}history.png"
    IN_PROGRESS = f"{BASE_PATH}in_progress.png"
    SETTINGS = f"{BASE_PATH}settings.png"
    
    TRASH_CAN = f"{BASE_PATH}trashcan.png"
    TRASH_CAN_LIGHT = f"{BASE_PATH}trashcan_light.png"
    ORDER = f"{BASE_PATH}order.png"

    CLOSE = f"{BASE_PATH}close.png"
    CLOSE_ALL = f"{BASE_PATH}close_all.png"
    CLOSE_LIGHT = f"{BASE_PATH}close_light.png"
    CLOSE_DARK = f"{BASE_PATH}close_dark.png"

    CONNECTION = f"{BASE_PATH}connection.png"
    CONNECTION_READY = f"{BASE_PATH}connection_ready.png"
    CONNECTION_LOST = f"{BASE_PATH}connection_lost.png"

    def __init__(self):
        pass

    @staticmethod
    def create(filename: str):
        img_src = Image.open(filename)

        if REFS.MOBILE:
            #img = img.subsample(2,2)
            width = img_src.width
            height = img_src.height

            img_src = img_src.resize((int(width/2), int(height/2)), Image.ANTIALIAS)
        
        img = ImageTk.PhotoImage(img_src)

        return img