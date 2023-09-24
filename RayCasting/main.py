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
            [1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1]]

# checking each position in map
# for each value of each row
for i in range(len(mapArray)):
    for j in range(len(mapArray[1])):
        if mapArray[i][j] == 1:
            mapArray[i][j] = [0.1,0.1,0.1]#list(np.random.uniform(0,1,3))
        # if mapArray[i][j] == 2:
        #     mapArray[i][j] = list(np.random.uniform(0,1,3))

# starting position
posx, posy = (1,1)
# top right corner
exitx, exity = (mapArray[len(mapArray)-1],mapArray[len(mapArray)-1])
# initial rotation
# pi/4 is looking 180/4 -> 45 degrees NE
rot = np.pi/4 

carExist = False

objTick = 0 

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

        # ray pathing out
        while True:
            x = x + cos
            y = y + sin

            # increment check
            n = n + 1

            # if part of map is not empty
            # int(var) rounds the position of the ray
            if mapArray[int(x)][int(y)] != 0:
                # calculates height relative to player
                # height = 1/(height_mult*ray_sens*n)

                # colour assignment
                height = np.clip(1/(height_mult*ray_sens*n), 0, 1)
                c = np.asarray(mapArray[int(x)][int(y)]) * (0.3 + 0.7 * height**2)

                break
                

        # -height to +height to make camera at a angle of 0 relative to ground
        if mapArray[int(x)][int(y)] == [0.1,0.1,0.1]:
            plt.vlines(i, -height, height, lw=8, colors=c)
        elif mapArray[int(x)][int(y)] == [1,1,1]:
            plt.vlines(i, -height, height/2, lw=8, colors=c)

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

    # key = keyboard.read_key()
    # key = keyboard.read_key()
    x, y = (posx, posy)

    move_sens = 0.3
    rot_sens = np.pi/20

    # same logic as ray movement (forward,back)
    if keyboard.is_pressed('up'):
        x,y = (x + move_sens*np.cos(rot), y + move_sens*np.sin(rot))
    elif keyboard.is_pressed('down'):
        x,y = (x - move_sens*np.cos(rot), y - move_sens*np.sin(rot))
    # change rotation only
    elif keyboard.is_pressed('left'):
        rot = rot - rot_sens
    elif keyboard.is_pressed('right'):
        rot = rot + rot_sens
    # exit ggame
    elif keyboard.is_pressed('esc'):
        break
    # spawn car
    elif keyboard.is_pressed('v'):
        carExist=True
        carposx,carposy= (5,1)
        mapArray[int(carposx)][int(carposy)] = [1,1,1]
    else:
        pass

    # if key == 'up':
    #     x,y = (x + move_sens*np.cos(rot), y + move_sens*np.sin(rot))
    # elif key == 'down':
    #     x,y = (x - move_sens*np.cos(rot), y - move_sens*np.sin(rot))
    # # change rotation only
    # elif key == 'left':
    #     rot = rot - rot_sens
    # elif key == 'right':
    #     rot = rot + rot_sens
    # # exit ggame
    # elif key == 'esc':
    #     break
    # # spawn car
    # elif key == 'v':
    #     print("CAR CREATED")
    #     carExist=True
    #     carposx,carposy= (5,1)
    #     mapArray[int(carposx)][int(carposy)] = 2
    # else:
    #     pass


    # if running into exit, leave game
    # else, movement reassignment only occurs if not a wall
    if mapArray[int(x)][int(y)] == 0:
        print("NOT A WALL")
        if int(posx) == exitx and int(posy) == exity:
            break
        posx, posy = (x,y)
    # death if touching car
    elif mapArray[int(x)][int(y)] == [1,1,1]:
        print("=========TOUCHING CAR=========")
        break
    
    
    if carExist==True:
        mapArray[int(carposx)][int(carposy)] = [1,1,1]
        carposy_next = carposy + 0.5
        
        print(f"Current car pos: y={carposx}, x={carposy}")
    
        # hit a wall
        if mapArray[int(carposx)][int(carposy_next)] == [0.1,0.1,0.1]:
            carExist = False
            print("CAR DEAD")
            mapArray[int(carposx)][int(carposy)] = 0
        # if empty next path, car moves
        # will overlap (no collision between self)
        elif mapArray[int(carposx)][int(carposy_next)] == 0 or [1,1,1]:
            mapArray[int(carposx)][int(carposy)] = 0
            mapArray[int(carposx)][int(carposy_next)] = 2
            carposy = carposy_next
            print("NEW CAR CREATED")
        
    # checking each position in map
    # for each value of each row
    for i in range(len(mapArray)):
        for j in range(len(mapArray[1])):
            if mapArray[i][j] == 2:
                mapArray[i][j] = [1,1,1]


    objTick = objTick + 1

    # if objTick%4==0:
    #     carExist=True
    #     carposx,carposy= (5,1)
    #     mapArray[int(carposx)][int(carposy)] = [1,1,1]

plt.close()

# Obstacle object
# carx,cary position in mapArray
# for car in carlist
#   render car
#       delete past carx,cary
#       create new carx,cary_next