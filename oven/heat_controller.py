
from datetime import datetime

class HeatController:
    def __init__(self):
        self.is_on = False

    def heat_on(self):
        if self.is_on:
            return
        print("Heat ON")
        self.is_on = True

    def heat_off(self):
        if not self.is_on:
            return
        print("Heat OFF")
        self.is_on = False

    def on_temp_change(self):
        # This is only needed for dummy controller
        pass
