#!/usr/bin/env python3

# http://www.fileformat.info/format/mpeg/sample/index.dir
import pygame
import sys

FPS = 30

if len(sys.argv) < 2:
    print(f"missing 1 required param.\n\nUsage: debug/test-pygame-movie.py <path to mp4 file>")
    sys.exit(1)

file_name = sys.argv[1]

pygame.init()
clock = pygame.time.Clock()
movie = pygame.movie.Movie(file_name)
screen = pygame.display.set_mode(movie.get_size())
movie_screen = pygame.Surface(movie.get_size()).convert()

movie.set_display(movie_screen)
movie.play()


playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            movie.stop()
            playing = False

    screen.blit(movie_screen,(0,0))
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()