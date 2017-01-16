from utils import Pixel
import random
import game_state
import time


class Snake(object):
    def __init__(self, start):
        self.pixels = []

        for p in range(4):
            self.pixels.append(Pixel(start[0], start[1]))
            start = Pixel.add_step(start, Pixel.RIGHT)

    @property
    def core(self):
        return self.pixels[0]

    def hit_dot(self, dot):
        return self.core.x == dot.x and self.core.y == dot.y

    @property
    def occupied(self):
        return [p.as_t for p in self.pixels]

    def step(self, direction):
        """LIFO data structure ensures shape preservation"""
        lead = self.pixels[0]
        new_p = Pixel(lead.x, lead.y)
        new_p.step(direction)
        self.pixels.insert(0, new_p)
        self.last_popped = self.pixels.pop()

    def consume(self, point):
        pixels.insert(Pixel(point[0], point[1]), 0)


class SnakeGame(object):
    ROWS = 8
    COLUMNS = 7

    SPEED = 1
    KEYS = {
        'w': Pixel.RIGHT,
        'a': Pixel.DOWN,
        's': Pixel.LEFT,
        'd': Pixel.UP
    }

    def __init__(self):
        self.direction = Pixel.UP
        self.player = Snake([0, 0])
        self.dot = self.get_next_dot()
        self.move = 0
        self.update_dot_matrix(self.all_pixels)

    @property
    def all_pixels(self):
        return [self.dot] + self.player.pixels

    def get_next_dot(self):
        pxs = [(p.x, p.y) for p in self.player.pixels]
        free_pixels = [(x, y) for x in range(self.COLUMNS)
                       for y in range(self.ROWS)
                       if (x, y) not in pxs]
        choice = random.choice(free_pixels)
        return Pixel(choice[0], choice[1])

    @property
    def lost_state(self):
        pixels = []

        for x in range(8):
            pixels.append(Pixel(x, x))
            diff = 7 - x
            pixels.append(Pixel(diff, x))

        return pixels

    @property
    def out_of_bounds(self):
        return not self.player.core.can_step_inbound(
            self.direction,
            self.COLUMNS,
            self.ROWS,
            self.player.occupied)

    @staticmethod
    def update_dot_matrix(new_pixels):
        game_state.queue.put(new_pixels)

    def increment(self):
        if not game_state.last_key_press.empty():
            self.direction = game_state.last_key_press.get()

        if self.out_of_bounds:
            self.update_dot_matrix(self.lost_state)
            time.sleep(1)
            game_state.stop_flag = True
            print "Game Over"

        self.player.step(self.direction)

        if self.player.hit_dot(self.dot):
            self.player.pixels.append(self.player.last_popped)
            self.dot = self.get_next_dot()

        self.update_dot_matrix(self.all_pixels)
