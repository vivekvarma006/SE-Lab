"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (140, 200, 230)
COLOR_HELI = (60, 60, 70)
COLOR_OBSTACLE = (70, 150, 80)
COLOR_TEXT = (20, 20, 20)
COLOR_BANNER = (180, 40, 40)
COLOR_PANEL = (255, 255, 255, 215)
COLOR_SHIELD = (30, 90, 220)


def draw_scene(surface, helicopter, obstacles, shield_active=False):
    surface.fill(COLOR_BG)
    for obstacle in obstacles:
        pygame.draw.rect(surface, COLOR_OBSTACLE, obstacle.get_top_rect())
        pygame.draw.rect(surface, COLOR_OBSTACLE, obstacle.get_bottom_rect())
    heli_rect = helicopter.get_rect()
    pygame.draw.rect(surface, COLOR_HELI, heli_rect, border_radius=4)
    if shield_active:
        pygame.draw.circle(surface, COLOR_SHIELD, heli_rect.center, heli_rect.width // 2 + 10, 3)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text, y_offset=0, color=COLOR_BANNER):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + y_offset))
    surface.blit(surf, rect)


def draw_game_over(surface, font, lines):
    """Light panel in the middle of the screen, first line in red."""
    line_h = font.get_linesize() + 8
    panel = pygame.Surface((360, line_h * len(lines) + 30), pygame.SRCALPHA)
    panel.fill(COLOR_PANEL)
    surface.blit(panel, panel.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2)))
    first = -(len(lines) - 1) * line_h // 2
    for i, text in enumerate(lines):
        draw_banner(surface, font, text, first + i * line_h, COLOR_BANNER if i == 0 else COLOR_TEXT)
