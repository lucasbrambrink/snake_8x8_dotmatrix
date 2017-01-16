from dot_matrix import DotMatrix
from utils import Pixel
import Queue


def initialize_game_variables():
	from snake import SnakeGame

	global queue
	queue = Queue.Queue()

	# API for dotmatrix singleton
	global dm
	dm = DotMatrix()

	global snake_game
	snake_game = SnakeGame()
	
	# global flag to halt all threads
	global stop_flag
	stop_flag = False

	# last provided key input
	global last_key_press
	last_key_press = Queue.Queue()
	last_key_press.put(Pixel.UP)
	
	global GAME_SPEED
	GAME_SPEED = 0.3

