
from datetime import datetime

class HeatController:
    def __init__(self):
        self.is_on = False
        self.dev = "/sys/devices/platform/pinctrl/gpio/gpio71/value"

    def heat_on(self):
        if self.is_on:
            return
        print("Heat ON")
        with open(self.dev, "w") as f:
            f.write("0")
        self.is_on = True

    def heat_off(self):
        if not self.is_on:
            return
        print("Heat OFF")
        with open(self.dev, "w") as f:
            f.write("1")
        self.is_on = False

    def on_temp_change(self):
        # This is only needed for dummy controller
        pass
