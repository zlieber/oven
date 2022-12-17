#!/usr/bin/python3


from mainui import MainUI
from oven_controller import OvenController
from heat_controller import HeatController
from dummy_heat_controller import DummyHeatController
from temp_monitor import TemperatureMonitor
from dummy_temp_monitor import DummyTemperatureMonitor

import argparse
import sys

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

parser = argparse.ArgumentParser(
                    prog = 'oven.py',
                    description = 'Composites oven controller')

parser.add_argument('-d', '--dummy', action='store_true',
                    help="Use dummy heat controller and temperature monitor.")

args = parser.parse_args(sys.argv[1:])

if args.dummy:
    temp_monitor = DummyTemperatureMonitor()
    heat_controller = DummyHeatController(temp_monitor)
else:
    heat_controller = HeatController()
    temp_monitor = TemperatureMonitor()

oven_controller = OvenController(heat_controller)

ui = MainUI(curves_config, oven_controller, temp_monitor)
ui.run()
