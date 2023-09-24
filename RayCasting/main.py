import numpy as np
from matplotlib import pyplot as plt
import keyboard

mapArray = [[1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1]]

# starting position
posx, posy = (1,1)
exitx, exity = (3,3)
# initial rotation
# pi/4 is looking 180/4 -> 45 degrees NE
rot = np.pi/4 

carExist = False

# iterate through each degree of view
# will scan from rot - 30deg to rot + 30deg
# rot is essentially net zero (relative to view), but will be some value relative to the map
while True:
    for i in range(60):
        rot_i = rot + np.deg2rad(i-30)

        x = posx
        y = posy

        # make up the change in y_ray (sin) and x_ray (cos)
        # ray sensitivity ensures that the jump in ray checks is not too large
        ray_sens = 0.02
        height_mult = 0.5
        sin,cos = (ray_sens*np.sin(rot_i), ray_sens*np.cos(rot_i))
        n = 0
        while True:
            x = x + cos
            y = y + sin

            # increment check
            n = n + 1

            # if part of map is not empty
            # int(var) rounds the position of the ray
            if mapArray[int(x)][int(y)] != 0:
                # calculates height relative to player
                height = 1/(height_mult*ray_sens*n)
                break

        # -height to +height to make camera at a angle of 0 relative to ground
        plt.vlines(i, -height, height, lw=8)

    plt.axis('off')
    plt.tight_layout()
    # Limit plot region
    plt.axis([0,60,-1,1])
    # plot show (draw is better for iterative plots)
    plt.draw()
    # plot pause (frame)
    plt.pause(0.00001)
    # plot data cleard
    plt.clf()


    # MOVEMENT
    # same logic as ray movement (forward,back)

    key = keyboard.read_key()
    x, y = (posx, posy)

    move_sens = 0.3
    rot_sens = np.pi/20
    # same logic as ray movement (forward,back)
    if key == 'up':
        x,y = (x + move_sens*np.cos(rot), y + move_sens*np.sin(rot))
    elif key == 'down':
        x,y = (x - move_sens*np.cos(rot), y - move_sens*np.sin(rot))
    # change rotation only
    elif key == 'left':
        rot = rot - rot_sens
    elif key == 'right':
        rot = rot + rot_sens
    # exit ggame
    elif key == 'esc':
        break

    # if running into exit, leave game
    # else, movement reassignment only occurs if not a wall
    if mapArray[int(x)][int(y)] == 0:
        if int(posx) == exitx and int(posy) == exity:
            break
        posx, posy = (x,y)
    
    # spawn car
    if key == 'c':
        print("CAR CREATED")
        carExist=True
        cary,carx= (5,1)
        mapArray[int(cary)][int(carx)] = 2


    if carExist==True:
        mapArray[int(cary)][int(carx)] = 2
        carx_next = carx + 0.5
        
        print(f"Current car pos: y={cary}, x={carx}")
        print(f"Checking car pos: y={cary}, x={carx_next} with mapArray = {mapArray[int(cary)][int(carx_next)]}")

        # hit a wall
        if mapArray[int(cary)][int(carx_next)] == 1:
            carExist = False
            print("CAR DEAD")
        # if empty next path, car moves
        # will overlap (no collision between self)
        elif mapArray[int(cary)][int(carx_next)] == 0 or 2:
            mapArray[int(cary)][int(carx)] = 0
            mapArray[int(cary)][int(carx_next)] = 2
            carx = carx_next
            print("NEW CAR CREATED")


plt.close()
