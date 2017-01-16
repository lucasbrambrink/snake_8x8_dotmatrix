from dot_matrix import DotMatrix
from utils import Pixel
from snake import SnakeGame
import time
import threading
import game_state
import readchar


# Run 2 additional threads

def increment_game_state():
    # after GAME_SPEED seconds, step into next state
    while True:
        game_state.snake_game.increment()
        time.sleep(game_state.GAME_SPEED)
        if game_state.stop_flag:
            break


def display_dot_matrix_frames():
    # constantly refresh display ~15ms
    while True:
        if game_state.queue.empty():
            game_state.dm.display_matrix()
        else:
            pixels = game_state.queue.get()
            game_state.dm.update_binaries(pixels)

        if game_state.stop_flag:
            break


def listen_for_keychange():
    # propagate user input to game singleton
    # run in main thread (for input)
    while True:
        char = readchar.readchar()
        try:
            direction = SnakeGame.KEYS[char]
            game_state.last_key_press.put(direction)
        except KeyError:
            print 'Wrong key. Use {w, s, a, d}'
            if game_state.stop_flag:
                break
        except KeyboardInterrupt:
            game_state.stop_flag = True
            break


if __name__ == "__main__":
    game_state.initialize_game_variables()
    frames = threading.Thread(target=display_dot_matrix_frames)
    game = threading.Thread(target=increment_game_state)
    frames.start()
    game.start()
    listen_for_keychange()
