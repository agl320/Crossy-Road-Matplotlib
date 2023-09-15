import pygame as pg
import numpy as np


def main():
    # initialize pygame
    pg.init()
    # set window size
    screen = pg.display.set_mode((800, 600))
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        pg.display.update()

        # movement function called
        # movement()


def movement(posx, posy, rot, keys):
    pass


if __name__ == "__main__":
    main()
    pg.quit()
