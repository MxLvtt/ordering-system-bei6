from tkinter import *
from Notification.toast import Toast
from Handlers.timer_handler import TimerHandler
import Templates.references as REFS

class NotificationService():
    GLOBAL_DEACTIVATION=False

    ROOT = None
    MARGIN = (15, 15)

    MAX_NUMBER_OF_DISPLAYED_TOASTS=3
    CHECK_INTERVAL = 300

    TOASTS=[]

    initialized = False

    def __init__(self, root):
        window_height = root.winfo_height()
        window_width = root.winfo_width()

        Toast.HEIGHT = int(window_height / 4)
        Toast.WIDTH = int(window_width / 3)

        NotificationService.ROOT = root
        NotificationService.initialized = True

    @staticmethod
    def show_toast(title, text, keep_alive: bool = False):
        if NotificationService.GLOBAL_DEACTIVATION or not NotificationService.initialized:
            return

        root_x = NotificationService.ROOT.winfo_x()
        root_y = NotificationService.ROOT.winfo_y()
        root_h = NotificationService.ROOT.winfo_height()

        _id = len(NotificationService.TOASTS)

        new_toast = Toast(
            title=title,
            summary=text,
            id=_id,
            remove_cb=NotificationService.remove_toast,
            remove_all_cb=NotificationService.remove_all_toasts,
            origin=(
                root_x + NotificationService.MARGIN[0],
                root_y - NotificationService.MARGIN[1] + root_h - Toast.HEIGHT - 85 * (not REFS.MOBILE) + 40 * REFS.MOBILE
            ),
            margin=NotificationService.MARGIN,
            keep_alive=keep_alive
        )
        
        NotificationService.TOASTS.append(new_toast)

        if _id < NotificationService.MAX_NUMBER_OF_DISPLAYED_TOASTS:
            NotificationService.start_fadeout(new_toast)

        NotificationService.start_check_loop()

    @staticmethod
    def start_fadeout(toast: Toast):
        if not toast.keep_alive:
            toast.timer_id = TimerHandler.start_timer(
                callback=toast.fade_out,
                delay_ms=Toast.FADEOUT_DELAY
            )

    @staticmethod
    def start_check_loop():
        for index, toast in enumerate(NotificationService.TOASTS):
            if toast.id != index:
                toast.id = index
                toast.update_window_geometry()

            if index >= NotificationService.MAX_NUMBER_OF_DISPLAYED_TOASTS:
                toast.hide()
            elif not toast.visible and not toast.stop_checking:
                toast.show()
                NotificationService.start_fadeout(toast)

        if not NotificationService.GLOBAL_DEACTIVATION:
            TimerHandler.start_timer(
                callback=NotificationService.start_check_loop,
                delay_ms=NotificationService.CHECK_INTERVAL,
                store_id=False
            )

    @staticmethod
    def remove_toast(toast: Toast):
        try:
            TimerHandler.cancel_timer(toast.timer_id)
        except:
            pass

        NotificationService.TOASTS.remove(toast)

        toast.remove_toast()

    @staticmethod
    def remove_all_toasts():
        for toast in NotificationService.TOASTS:
            try:
                TimerHandler.cancel_timer(toast.timer_id)
            except:
                pass

            toast.remove_toast()

        NotificationService.TOASTS.clear()
