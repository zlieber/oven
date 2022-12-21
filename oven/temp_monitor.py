
import mraa

import logging

class TemperatureMonitor:
    def __init__(self):
        self.dev = mraa.Spi(0)
        self.dev.frequency(4300000)
        self.dev.lsbmode(lsb=False)
        self.logger = logging.getLogger("TempMonitor")

    def get_temperature(self):
        raw = self.dev.writeWord(1)

        # Swap bytes
        raw = (raw << 8 & 0xFFFF) | raw >> 8

        # Make sure bits 1, 2 and 15 are 0s.
        if raw & 0x8006:
            self.logger.warning("Invalid temperature reading: 0x%04x", raw)

        temp = float(raw >> 3) / 4.0
        self.logger.info("0x%04x %.01f" % (raw, temp))
        return temp
