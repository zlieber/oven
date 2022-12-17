
from datetime import datetime

class DummyHeatController:
    def __init__(self, temp_monitor):
        self.is_on = False
        self.temp_monitor = temp_monitor
        self.simulating_deg_per_min = (10, -2)

    def heat_on(self):
        if self.is_on:
            return
        self.last_time = datetime.now()
        print("Heat ON")
        self.is_on = True

    def heat_off(self):
        if not self.is_on:
            return
        print("Heat OFF")
        self.is_on = False

    def on_temp_change(self):
        if self.last_time is None:
            return
        curr_time = datetime.now()
        since_last = (curr_time - self.last_time).total_seconds() / 60.0
        if self.is_on:
            sim_deg = self.simulating_deg_per_min[0]
        else:
            sim_deg = self.simulating_deg_per_min[1]
        deg_diff = since_last * sim_deg
        self.temp_monitor.sim_temp += deg_diff
        self.last_time = curr_time
