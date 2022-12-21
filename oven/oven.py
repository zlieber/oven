#!/usr/bin/python3


from mainui import MainUI
from oven_controller import OvenController
from heat_controller import HeatController
from dummy_heat_controller import DummyHeatController
from temp_monitor import TemperatureMonitor
from dummy_temp_monitor import DummyTemperatureMonitor

import argparse
import sys

import logging
from logging.handlers import RotatingFileHandler

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

test_run = """
2 60 1
2 90 1
2 100 1
"""

quick_test = """
2 50 0.5
"""

curves_config = {
    "PTMW post cure slow": ptmw,
    "XPreg cure slow": xpreg_long,
    "XPreg cure fast": xpreg_med,
    "Temperature Test": test_run,
    "Quick test": quick_test
    }

FORMAT = '%(asctime)s %(name)s %(message)s'
handlers = [
    RotatingFileHandler("/home/rock/log/oven.log", backupCount=100, maxBytes=1024*1024)
    ]
logging.basicConfig(format=FORMAT,
                    level=logging.DEBUG,
                    handlers=handlers)

logger = logging.getLogger('oven')
logger.info("Oven is starting")

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

logger.info("Oven is shutting down.")
