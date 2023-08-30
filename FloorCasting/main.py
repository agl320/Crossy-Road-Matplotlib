import pygame as pg
import numpy as np


def main():
    # initialize pygame
    pg.init()
    # set window size
    screen = pg.display.set_mode((800, 600))
    running = True

    # make players movement time dependent
    clock = pg.time.Clock()

    hres = 120  # horizontal resolution
    halfvres = 100  # vertical resolution/2

    # relation with horizontal resolution
    mod = hres / 60  # scaling factor (60 degree fov)

    # starting parameters x,y pos + rotation
    posx, posy, rot = 0, 0, 0

    # (80, 60, 3) resolution and dimension
    # creates 3 channels of tuple values ranging from 0-1; dimension is hres by halfvres
    frame = np.random.uniform(0, 1, (hres, halfvres * 2, 3))

    # skybox
    # imported image is a surface; must convert to type of surfarray (so we can manipulate with numpy)
    sky = pg.image.load("skybox.jpg")
    sky = pg.surfarray.array3d(pg.transform.scale(sky, (360, halfvres * 2)))
    # floor texture
    floor = pg.surfarray.array3d(pg.image.load("floor.jpg"))

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # similar to ray-casting, pass through all columns in screen
        # checking from rot-30 to rot+30, such that rot is the rotation (kinda like phase difference)
        for i in range(hres):
            rot_i = rot + np.deg2rad(i / mod - 30)
            # cos2 is used to correct fish eye effect
            sin, cos, cos2 = (
                np.sin(rot_i),
                np.cos(rot_i),
                np.cos(np.deg2rad(i / mod - 30)),
            )
            frame[i][:] = sky[int(np.rad2deg(rot_i) % 359)][:] / 255

            # closest line gets distance of 1, farther gets higher value since j increases
            for j in range(halfvres):
                n = (halfvres / (halfvres - j)) / cos2
                x, y = posx + cos * n, posy + sin * n

                xx, yy = int(x * 2 % 1 * 100), int(y * 2 % 1 * 100)

                shade = 0.2 + 0.8 * (1 - j / halfvres)

                frame[i][halfvres * 2 - j - 1] = shade * floor[xx][yy] / 255

                # calculation of position of each pixel
                # white, otherwise black
                # halfvres*2 - j - 1 to fill from bottom to top
                # merely makes a checkerboard pattern
                # if int(x) % 2 == int(y) % 2:
                #     frame[i][halfvres * 2 - j - 1] = [0, 0, 0]
                # else:
                #     frame[i][halfvres * 2 - j - 1] = [1, 1, 1]

        # turn frame into surface; make_surface
        # first make surface dictates brightness
        surf = pg.surfarray.make_surface(frame * 255)
        # scale the surface to the window resolution
        surf = pg.transform.scale(surf, (800, 600))

        # aka draw the surface onto the screen (top left)
        screen.blit(surf, (0, 0))

        pg.display.update()

        # movement function called
        posx, posy, rot = movement(posx, posy, rot, pg.key.get_pressed())


def movement(posx, posy, rot, keys):
    if keys[pg.K_LEFT] or keys[ord("a")]:
        rot = rot - 0.1

    if keys[pg.K_RIGHT] or keys[ord("d")]:
        rot = rot + 0.1

    if keys[pg.K_UP] or keys[ord("w")]:
        posx, posy = posx + np.cos(rot) * 0.1, posy + np.sin(rot) * 0.1

    if keys[pg.K_DOWN] or keys[ord("s")]:
        posx, posy = posx - np.cos(rot) * 0.1, posy - np.sin(rot) * 0.1

    return posx, posy, rot


if __name__ == "__main__":
    main()
    pg.quit()
