
from curve import Curve
from datetime import datetime

class OvenController:
    def __init__(self, heat_controller):
        self.heat_controller = heat_controller

    def start(self, curve):
        self.curve = curve
        self.start_time = datetime.now()

        print("Starting curve %s" % curve.name)

    def stop(self):
        print("Stopping curve %s" % self.curve.name)
        self.heat_controller.heat_off()

    def on_temp_data(self, temp):
        target = self.curve.target_value_now(self.start_time)
        delta = target - temp
        if delta > 1.0:
            self.heat_controller.heat_on()
            res = "ON"
        elif delta < -1.0:
            self.heat_controller.heat_off()
            res = "OFF"
        else:
            res = "No change"
        self.heat_controller.on_temp_change()
        return res
