
import mraa

class TemperatureMonitor:
    def __init__(self):
        self.dev = mraa.Spi(0)
        self.dev.frequency(1000000)

    def get_temperature(self):
        raw = self.dev.writeWord(1)
        # Bits 0, 1, 2 and 15 are 0s.
        return float((( (raw & 0x7F) << 8) | raw >> 8) >> 3) / 4.0
