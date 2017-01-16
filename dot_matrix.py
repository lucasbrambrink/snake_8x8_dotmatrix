import RPi.GPIO as GPIO
from utils import BinaryUtility, HC595, Pixel


class DotMatrix(object):
    SDI = 11
    RCLK = 13
    SRCLK = 12
    PINS = [SDI, RCLK, SRCLK]
    SLEEPTIME = 0.1
    FAST = 0.000002

    def __init__(self):
        self.init_gpio()
        self.hc = HC595(self.SDI, self.RCLK, self.SRCLK, self.SLEEPTIME)
        self.matrix = []
        self.indexes = []
        self.display_binaries = []
        self.clear()

    @property
    def display_rows(self):
        if not hasattr(self, '_rows'):
            setattr(self, '_rows', map(BinaryUtility.convert_binary_to_hex,
                                       ["".join("0" if x != y else "1"
                                                for x in range(8))
                                        for y in range(8)]))
        return getattr(self, '_rows')

    @property
    def FULL(self):
        return ["1" for x in range(8)]

    @property
    def BLANK(self):
        return ["0" for x in range(8)]

    def clear(self, fast=False):
        fast_arg = None if not fast else self.FAST
        self.hc.pulse_state(map(
            BinaryUtility.convert_binary_to_hex,
            ("".join(self.FULL), "".join(self.BLANK))), fast_arg)

    def init_gpio(self):
        GPIO.setmode(GPIO.BOARD)  # Number GPIOs by its physical location
        for pin in self.PINS:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def push_state(self, column, row, clear=True):
        if clear:
            self.clear(True)
        fast_arg = None if clear else self.FAST
        self.hc.pulse_state((column, row), fast_arg)

    def light_point(self, x, y):
        row = self.BLANK
        row[y] = "1"
        column = self.FULL
        column[x] = "0"
        print row, column
        self.push_state(*map("".join, (row, column)))

    def display_matrix(self):
        for row in self.indexes:
            self.push_state(
                self.display_binaries[row],
                self.display_rows[row],
                False)

    def update_binaries(self, pixels):
        matrix = [
            [0 for y in range(8)] for x in range(8)
            ]
        for p in pixels:
            matrix[p.x][p.y] = 1

        columns = []
        for row in matrix:
            columns.append("".join("1" if x == 0 else "0" for x in row))

        self.display_binaries = map(BinaryUtility.convert_binary_to_hex, columns)
        self.indexes = [z for z in range(8) if columns[z] != "11111111"]
