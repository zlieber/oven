
from datetime import datetime

import logging

class HeatController:
    def __init__(self):
        self.is_on = False
        self.dev = "/sys/devices/platform/pinctrl/gpio/gpio71/value"
        self.logger = logging.getLogger("HeatController")

        # Selects high vs low trigger relay
        self.inverse = False

    def heat_on(self):
        if self.is_on:
            return
        self.logger.info("Heat ON")
        with open(self.dev, "w") as f:
            if self.inverse:
                f.write("0")
            else:
                f.write("1")
        self.is_on = True

    def heat_off(self):
        if not self.is_on:
            return
        self.logger.info("Heat OFF")
        with open(self.dev, "w") as f:
            if self.inverse:
                f.write("1")
            else:
                f.write("0")
        self.is_on = False

    def on_temp_change(self):
        # This is only needed for dummy controller
        pass
