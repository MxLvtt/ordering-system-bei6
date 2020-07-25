class Event(object):                                                       
    def __init__(self):
        self.callbacks = set()

    def __call__(self, *args, **kwargs):
        response = None
        
        for callback in self.callbacks:
            cb_resp = callback(*args, **kwargs)

            if cb_resp != None:
                response = cb_resp

        return response

    def add(self, listener):
        self.callbacks.add(listener)

    def remove(self, listener):
        self.callbacks.remove(listener)