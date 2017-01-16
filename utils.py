import RPi.GPIO as GPIO
import time


class Pixel(object):
	UP = (1, 0)
	LEFT = (0, -1)
	DOWN = (-1, 0)
	RIGHT = (0, 1)
	CORE_STEPS = (UP, RIGHT, DOWN, LEFT)

	UP_RIGHT = (-1, 1)
	DOWN_RIGHT = (1, 1)
	DOWN_LEFT = (1, -1)
	UP_LEFT = (-1, -1)
	ALL_STEPS = (
		UP, UP_RIGHT, RIGHT, DOWN_RIGHT, 
		DOWN, DOWN_LEFT, LEFT, UP_LEFT)

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def step(self, direction):
		self.x += direction[0]
		self.y += direction[1]

	def can_step_inbound(self, direction, xBound, yBound, occupied=None):
		test = (self.x + direction[0], self.y + direction[1])
		if occupied is not None and test in occupied:
			return False
		return (0 <= self.x + direction[0] < xBound) and \
			(0 <= self.y + direction[1] < yBound)

	@staticmethod
	def add_step(s1, s2):
		return (s1[0] + s2[0], s1[1] + s2[1])

	@property
	def as_t(self):
		return (self.x, self.y)

	def direction_to_previous(self, previous):
		return (self.x - previous[0], self.y - previous[0])

class BinaryUtility(object):

	@staticmethod
	def convert_to_binary(num):
		power = 0
		while 2 ** power <= num:
			power += 1
		power -= 1

		base_10 = 0
		while power >= 0:
			current_p = 2 ** power
			if current_p <= num:
				base_10 += 10 ** power 
				num -= current_p
			power -= 1

		return base_10

	@staticmethod
	def as_string(binary):
		if type(binary) is str:
			binary = "".join(
				b for b in binary 
				if b in ("0", "1"))
		elif type(binary) is int:
			binary = str(binary)
		else:
			raise Exception("Unable to serialize %s to binary" % binary)
		
		return binary

	@classmethod
	def convert_binary_to_hex(cls, binary):
		binary_string = cls.as_string(binary)
		
		all_sum = 0
		power = len(binary_string) - 1
		for bit in binary_string:
			if bit == '1':
				all_sum += (2 ** power)
			power -= 1

		return int(hex(all_sum), 16)


class HC595(object):
	DEFAULT_SLEEP_TIME = 0.1

	def __init__(self, serial_input, storage_clock_input, shift_register_clock_input, sleeptime=None):
		self.serial_input = serial_input
		self.storage_clock_input = storage_clock_input
		self.shift_register_clock_input = shift_register_clock_input
		self.sleeptime = self.DEFAULT_SLEEP_TIME
		if type(sleeptime) is int:
			self.sleeptime = sleeptime

	def pulse_state(self, states, sleeptime=None):
		for state in states:
			self.store_bits(state)
		self.release_memory()

	def store_bits(self, byte):
		for bit in range(0, 8):
			GPIO.output(self.serial_input, 0x80 & (byte << bit)) 
			self.pulse_clock_pin(self.shift_register_clock_input)

	def release_memory(self):
		self.pulse_clock_pin(self.storage_clock_input)

	def pulse_clock_pin(self, pin):
		GPIO.output(pin, GPIO.HIGH)
		time.sleep(0)
		GPIO.output(pin, GPIO.LOW)

