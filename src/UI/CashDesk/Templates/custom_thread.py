import threading

class CustomThread(threading.Thread): 
    def __init__(self, threadID, name, callback):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.callback = callback

    def run(self):
        self.callback()
