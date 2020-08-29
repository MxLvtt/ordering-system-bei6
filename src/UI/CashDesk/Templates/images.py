from tkinter import PhotoImage
from PIL import ImageTk, Image
import Templates.references as REFS
import os

class IMAGES():
    CHECK_MARK = f"checkmark.png"
    CHECK_MARK_DARK = f"checkmark_dark.png"

    EXIT = f"exit.png"
    NAVIGATION = f"nav.png"
    
    ADD = f"add.png"
    EXPORT = f"export.png"
    EDIT = f"edit.png"
    
    BURGER = f"burger.png"
    BURGER_DARK = f"burger_dark.png"
    
    BACK = f"back.png"
    NEXT = f"next.png"
    DOWN = f"down.png"
    UP = f"up.png"

    RESET_I = f"reset_i.png"

    UNDO = f"undo.png"
    UNDO_LIGHT = f"undo_light.png"

    HISTORY = f"history.png"
    IN_PROGRESS = f"in_progress.png"
    SETTINGS = f"settings.png"
    
    TRASH_CAN = f"trashcan.png"
    TRASH_CAN_LIGHT = f"trashcan_light.png"
    ORDER = f"order.png"

    CLOSE = f"close.png"
    CLOSE_ALL = f"close_all.png"
    CLOSE_LIGHT = f"close_light.png"
    CLOSE_DARK = f"close_dark.png"

    CONNECTION = f"connection.png"
    CONNECTION_READY = f"connection_ready.png"
    CONNECTION_LOST = f"connection_lost.png"

    def __init__(self):
        pass

    @staticmethod
    def create(filename: str):
        filename = f"{os.curdir}/img/{filename}"

        img_src = Image.open(filename)

        if REFS.MOBILE:
            #img = img.subsample(2,2)
            width = img_src.width
            height = img_src.height

            img_src = img_src.resize((int(width/2), int(height/2)), Image.ANTIALIAS)
        
        img = ImageTk.PhotoImage(img_src)

        return img