#!/usr/bin/env python3
import pygame

fonts = pygame.font.get_fonts()
print(len(fonts))
for f in fonts:
    print(f)