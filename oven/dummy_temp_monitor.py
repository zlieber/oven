
from random import random

class DummyTemperatureMonitor:
    def __init__(self):
        self.sim_temp = 23

    def get_temperature(self):
        return self.sim_temp + random() * 0.5
