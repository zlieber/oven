#!/usr/bin/python3


from mainui import MainUI

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


ui = MainUI(curves_config)
ui.run()
