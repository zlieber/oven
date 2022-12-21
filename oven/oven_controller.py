
from curve import Curve
import time

import logging

class OvenController:
    def __init__(self, heat_controller):
        self.heat_controller = heat_controller
        self.logger = logging.getLogger("OvenController")

    def start(self, curve):
        self.curve = curve
        self.start_time = time.monotonic()

        self.logger.info("Starting curve %s, time is %.03f" % (curve.name, self.start_time))
        return self.start_time

    def stop(self):
        self.logger.info("Stopping curve %s" % self.curve.name)
        self.heat_controller.heat_off()

    def on_temp_data(self, temp):
        target = self.curve.target_value_now(self.start_time)
        self.logger.info("%.01f -> %.01f" % (temp, target))
        delta = target - temp
        if delta > 1.0:
            self.heat_controller.heat_on()
            res = "ON"
        elif delta < -1.0:
            self.heat_controller.heat_off()
            res = "OFF"
        else:
            res = "No change"

        # This is for simulations only
        self.heat_controller.on_temp_change()
        return res
