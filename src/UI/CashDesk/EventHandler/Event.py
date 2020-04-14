class Event(object):                                                       
    def __init__(self):
        self.callbacks = set()

    def __call__(self, *args, **kwargs):
        for callback in self.callbacks:
            callback(*args, **kwargs)

    def add(self, listener):
        self.callbacks.add(listener)

    def remove(self, listener):
        self.callbacks.remove(listener)