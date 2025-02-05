import pygame as pg
from snake import Snake, vec2, deg_to_rad, rad_to_deg, get_vector
from math import atan2, pi, cos, sin

resolution = vec2((1920, 1080))



class Game:
    def __init__(self):
        self.display = pg.display.set_mode((resolution.x, resolution.y))
        self.clock = pg.time.Clock()
        self.tick_rate = 165
        self.is_running = True
        self.delta = 0.004

        self.snake = Snake((resolution.x / 2, resolution.y / 2))
        for _ in range(20):
            self.snake.add_segment()

        self.left_clicking = False

    def draw(self):
        self.display.fill('black')
        self.snake.draw(self.display)
        pg.display.update()

    def run_game_loop(self):
        
        while self.is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.is_running = False
                    pg.quit()
                    quit()
                elif event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                    self.left_clicking = True
                elif event.type == pg.MOUSEBUTTONUP and pg.mouse.get_pressed()[0] == False:
                    self.left_clicking = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_o:
                    self.snake.add_segment()

            # Add snake acceleration
            if self.left_clicking:
                # Turn snake head
                mouse_pos = vec2(pg.mouse.get_pos())
                direction = get_vector(self.snake.position, mouse_pos)
                new_angle = atan2(-direction.y, direction.x)
                self.snake.target_angle = rad_to_deg(new_angle) + 90.0
                self.snake.current_movement_speed += self.snake.acceleration
            else:
                self.snake.current_movement_speed -= 1.0 * self.snake.acceleration

            # Clamp movement speed
            self.snake.current_movement_speed = max(min(self.snake.max_movement_speed, self.snake.current_movement_speed), 0)

            # Move snake head
            self.snake.position = vec2((
                self.snake.position.x + self.snake.current_movement_speed * cos(deg_to_rad(self.snake.angle - 90.0)),
                self.snake.position.y + self.snake.current_movement_speed * sin(deg_to_rad(self.snake.angle - 90.0))
            ))

            self.snake.update()
            self.draw()
            self.delta = self.clock.tick(self.tick_rate)
            fps = (1 / self.delta) * 1000.0
            pg.display.set_caption(f"FPS: {fps: 0.2f}")