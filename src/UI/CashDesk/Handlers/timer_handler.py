

class TimerHandler():
    DEBUG = False
    ROOT_OBJECT = None
    TIMER_IDS = []

    def __init__(self, root_object):
        TimerHandler.ROOT_OBJECT = root_object

    def __del__(self):
        tid_list_copy = TimerHandler.TIMER_IDS.copy()
        for tid in tid_list_copy:
            TimerHandler.cancel_timer(tid)
    
    @staticmethod
    def start_timer(callback, delay_ms: int, store_id = True) -> int:
        if TimerHandler.ROOT_OBJECT == None:
            raise RuntimeError("Timer could not be started. Root object in References is Nonetype.")

        tid = TimerHandler.ROOT_OBJECT.after(delay_ms, callback)
        
        if TimerHandler.DEBUG:
            print(f"Started timer #{tid} with delay of {delay_ms} ms ...")

        if store_id:
            TimerHandler.TIMER_IDS.append(tid)

        return tid

    @staticmethod
    def cancel_timer(timer_id):
        if TimerHandler.ROOT_OBJECT == None:
            raise RuntimeError("Timer could not be started. Root object in References is Nonetype.")

        try:
            TimerHandler.TIMER_IDS.index(timer_id)
        except:
            print(f"Timer id {timer_id} not registered.")
            return

        TimerHandler.ROOT_OBJECT.after_cancel(timer_id)
        TimerHandler.TIMER_IDS.remove(timer_id)
        
        if TimerHandler.DEBUG:
            print(f"Canceled timer #{timer_id}")
