"""
GameEngine: owns the helicopter and all obstacles.

Each frame the helicopter is checked against every obstacle; touching
either wall ends the game, and R starts a new one. Distance travelled
is the score and goes up by the scroll speed every frame. S turns on a
shield that absorbs exactly one hit and then switches off.
"""

import random

import pygame

from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 90
GAP_HEIGHT = 150
WALL_WIDTH = 60
SCROLL_SPEED = 3
PIXELS_PER_METRE = 10


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.helicopter = Helicopter(x=100, y=HEIGHT / 2)
        self.obstacles = []
        self.frames_until_spawn = 0
        self.game_over = False
        self.distance = 0   # in pixels scrolled
        self.shield_active = False

    def distance_m(self):
        return self.distance // PIXELS_PER_METRE

    def _spawn_obstacle(self):
        margin = 60
        gap_y = random.randint(margin + GAP_HEIGHT // 2, HEIGHT - margin - GAP_HEIGHT // 2)
        self.obstacles.append(Obstacle(
            x=WIDTH, gap_y=gap_y, gap_height=GAP_HEIGHT,
            wall_width=WALL_WIDTH, screen_height=HEIGHT, speed=SCROLL_SPEED,
        ))

    def handle_input(self, keys_pressed):
        if not self.game_over:
            self.helicopter.handle_input(keys_pressed)

    def handle_keydown(self, key):
        if key == pygame.K_r and self.game_over:
            self.reset()
        elif key == pygame.K_s and not self.game_over:
            self.shield_active = True

    def update(self):
        if self.game_over:
            return

        self.helicopter.update(HEIGHT)
        self.distance += SCROLL_SPEED

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_obstacle()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for obstacle in self.obstacles:
            obstacle.update()
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

        self._check_collisions()

    def _check_collisions(self):
        heli_rect = self.helicopter.get_rect()
        for obstacle in self.obstacles:
            if obstacle.absorbed or not obstacle.collides_with(heli_rect):
                continue
            if self.shield_active:
                # shield takes this hit; ignore this wall from now on so the
                # helicopter doesn't crash into it again on the next frame
                self.shield_active = False
                obstacle.absorbed = True
            else:
                self.game_over = True
                return

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.helicopter, self.obstacles, self.shield_active)
        if self.game_over:
            renderer.draw_game_over(surface, font, [
                "GAME OVER",
                f"Distance: {self.distance_m()} m",
                "Press R to play again",
            ])
        else:
            renderer.draw_text(surface, font, f"Distance: {self.distance_m()} m", (10, 10))
            if self.shield_active:
                renderer.draw_text(surface, font, "Shield: ON", (10, 36), renderer.COLOR_SHIELD)
            else:
                renderer.draw_text(surface, font, "Shield: OFF (press S)", (10, 36))
