#!/usr/bin/python3


from mainui import MainUI
from oven_controller import OvenController
from heat_controller import HeatController
from temp_monitor import TemperatureMonitor

ptmw = """
2 50 8
1 65 3
1 80 3
1 95 3
1 110 3
1 120 4
"""

xpreg_long = """
2 60 6
2 80 6
"""

xpreg_med = """
2 60 6
2 100 4
"""

curves_config = {
    "PTMW post cure slow": ptmw,
    "XPreg cure slow": xpreg_long,
    "XPreg cure fast": xpreg_med
    }


heat_controller = HeatController()
oven_controller = OvenController(heat_controller)
temp_monitor = TemperatureMonitor()
heat_controller.set_temp_monitor(temp_monitor);

ui = MainUI(curves_config, oven_controller, temp_monitor)
ui.run()
