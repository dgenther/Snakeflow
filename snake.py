import pygame as pg
from typing import Union
from math import cos, sin, pi, sqrt, atan2
from random import randint

POINT_COLORS = ['blue', 'red', 'cyan', 'yellow']
RIGHT_POINT = 0
FRONT_POINT = 1
LEFT_POINT = 2
BACK_POINT = 3

def deg_to_rad(angle: float) -> float:
    return angle * pi / 180

def rad_to_deg(angle: float) -> float:
    return angle * 180 / pi

def get_vector(start: 'vec2', end: 'vec2'):
    return vec2((end.x - start.x, start.y - end.y))

def shortest_angle_diff(a, b):
    # Function to calculate the shortest angle difference
    return ((a - b + 180) % 360) - 180

def lerp(a, b, t):
    return a + (b - a) * t

class vec2:
    def __init__(self, arg: Union[tuple, list, 'vec2']):
        if isinstance(arg, tuple):
            self.x, self.y = arg[0], arg[1]
        elif isinstance(arg, list):
            self.x, self.y = arg[0], arg[1]
        elif isinstance(arg, vec2):
            self.x, self.y = arg.x, arg.y
        else:
            raise ValueError("Invalid arguments for vec2 initialization")

    def __mul__(self, val):
        if isinstance(val, int):
            return vec2((self.x * val, self.y * val))
        elif isinstance(val, float):
            return vec2((self.x * val, self.y * val))
        else:
            raise ValueError("Invalid arguments for vec2 multiplication. Only float and int allowed.")

    def __add__(self, val):
        if isinstance(val, vec2):
            return vec2((self.x + val.x, self.y + val.y))
        elif isinstance(val, int):
            return vec2((self.x + val, self.y + val))
        elif isinstance(val, float):
            return vec2((self.x + val, self.y + val))
        else:
            raise ValueError("Invalid arguments for vec2 addition. Only vec2, float and int allowed.")
    
    def __sub__(self, val):
        if isinstance(val, vec2):
            return vec2((self.x - val.x, self.y - val.y))
        elif isinstance(val, int):
            return vec2((self.x - val, self.y - val))
        elif isinstance(val, float):
            return vec2((self.x - val, self.y - val))
        else:
            raise ValueError("Invalid arguments for vec2 subtraction. Only vec2, float and int allowed.")

    def normalized(self):
        magnitude = sqrt(self.x ** 2 + self.y ** 2)
        if magnitude == 0:
            magnitude = 1e-9
        self.norm_x = float(self.x / magnitude)
        self.norm_y = float(self.y / magnitude)
        return vec2((self.norm_x, self.norm_y))
    
    def __call__(self):
        return (self.x, self.y)
    
    def __iter__(self):
        return iter((self.x, self.y))

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Index out of range")

    def __repr__(self):
        return f"({self.x}, {self.y})"

"""
*args can be:
    int, int
    tuple[int, int]
    vec2[int, int]
"""
class SnakeSegment:
    def __init__(self, position: vec2|tuple|list, angle=0.0, radius=30):
        if isinstance(position, vec2):
            self.position: vec2 = position
        elif isinstance(position, tuple):
            self.position: vec2 = vec2((position[0], position[1]))
        elif isinstance(position, list):
            self.position: vec2 = vec2((position[0], position[1]))
        else:
            raise ValueError("Invalid arguments for SnakeSegment initialization")
        
        self.angle: float = angle
        self.target_angle: float = angle
        self.angular_max_speed: float = rad_to_deg(0.05)

        self.acceleration: float = 0.1
        self.current_movement_speed: float = 0.0
        self.max_movement_speed: float = 5.0

        self.radius: int = radius
        self.previous_snake_segment: SnakeSegment = None
        self.next_snake_segment: SnakeSegment = None
        right_point: vec2 = vec2((0,0))
        front_point: vec2 = vec2((0,0))
        left_point: vec2 = vec2((0,0))
        back_point: vec2 = vec2((0,0))
        self.points : list[vec2] = [right_point, front_point, left_point, back_point]
        self.point_colors : list[pg.Color] = ['blue', 'red', 'cyan', 'yellow']

        for i in range(len(self.points)):
            self.points[i] = vec2((
                self.position.x + self.radius * cos(deg_to_rad(self.angle) - i * pi / 2), 
                self.position.y + self.radius * sin(deg_to_rad(self.angle) - i * pi / 2)
            ))

    def update(self):
        
        if self.previous_snake_segment and self.next_snake_segment:
            # Calculate the average angle with wrap-around consideration
            angle_diff = shortest_angle_diff(self.next_snake_segment.angle, self.previous_snake_segment.angle)
            target_angle = (self.previous_snake_segment.angle + angle_diff / 2) % 360
            self.target_angle = target_angle
        elif self.previous_snake_segment:
            vec = get_vector(self.position, self.previous_snake_segment.position)
            self.target_angle = rad_to_deg(atan2(-vec.y, vec.x)) + 90.0

        # Move current snake segment toward previous one.
        if self.previous_snake_segment:
            dir = get_vector(self.previous_snake_segment.position, self.position)
            offset = dir.normalized() * self.previous_snake_segment.radius
            self.position = self.previous_snake_segment.position + vec2((offset.x, -offset.y))

        if self.next_snake_segment:
            self.next_snake_segment.update()

        # Normalize target angle to be between 0 and 360
        self.target_angle = self.target_angle % 360
        
        # Normalize current angle to be between 0 and 360
        self.angle = self.angle % 360

        # Calculate the shortest path
        diff = shortest_angle_diff(self.target_angle, self.angle)

        if self.previous_snake_segment:
            # Move angle towards target angle
            if abs(diff) < self.angular_max_speed * 5:
                self.angle = self.target_angle
            else:
                self.angle += diff / abs(diff) * self.angular_max_speed  # Determine direction and apply max speed
        else:
            # Move angle towards target angle
            if abs(diff) < self.angular_max_speed:
                self.angle = self.target_angle
            else:
                self.angle += diff / abs(diff) * self.angular_max_speed  # Determine direction and apply max speed

        # Ensure angle remains in range [0, 360)
        self.angle = self.angle % 360

        for i in range(len(self.points)):
            self.points[i] = vec2((
                self.position.x + self.radius * cos(deg_to_rad(self.angle) - i * pi / 2), 
                self.position.y + self.radius * sin(deg_to_rad(self.angle) - i * pi / 2)
            ))

    def draw(self, display):

        if self.next_snake_segment:
            self.next_snake_segment.draw(display)

        main_green = pg.Color(0, 150, 0)

        pg.draw.circle(display, main_green, self.position(), self.radius)
        for i in range(len(self.points)):
            varying_green = pg.Color(randint(0, 50), int(main_green.g) + randint(-60, -40), randint(0, 50))
            pg.draw.circle(display, varying_green, self.points[i](), self.radius / 5)
    
    def add_segment(self, radius=30):
        if not self.next_snake_segment:
            start_position = self.position - vec2((cos(deg_to_rad(self.angle - 90.0)), sin(deg_to_rad(self.angle - 90.0)))) * (radius)
            self.next_snake_segment = SnakeSegment(start_position, self.angle, radius=radius)
            self.next_snake_segment.previous_snake_segment = self
        else:
            self.next_snake_segment.add_segment(radius=radius)

class Snake(SnakeSegment):
    def __init__(self, position, angle=0, radius=40):
        super().__init__(position, angle=angle, radius=radius)
        
    