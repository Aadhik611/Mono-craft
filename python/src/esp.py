import time


class esp:
    def __init__(self, connection):
        self.client = connection

    def blink(self, delay=0.2):

        self.client.send("LED")
        time.sleep(delay)
        self.client.send("LED")

    def blink_times(self, delay=0.2, times=2):

        for i in range(times):
            self.blink(delay=delay)
