import numpy as np
from matplotlib import pyplot as plt
import keyboard
from Obstacle import Obstacle
import random
import tkinter as tk


### INITIAL WINDOW
def save_numbers():
    global mapX, mapY
    mapX = tkIntX.get()
    mapY = tkIntY.get()
    root.destroy()

# Create the main application window
root = tk.Tk()
root.geometry("300x300")
root.title("Set map size")

escLabel = tk.Label(root, text="Press [ESC] to quit game")
escLabel.pack(expand=True)

tkIntX = tk.IntVar(root)
tkIntX.set(10)
labelx = tk.Label(root, text="Width (recommended 10):")
labelx.pack(expand=True)
entryx = tk.Entry(root, textvariable = tkIntX)
entryx.pack(expand=True)

tkIntY = tk.IntVar(root)
tkIntY.set(30)
labely = tk.Label(root, text="Length (recommended 30):")
labely.pack(expand=True)
entryy = tk.Entry(root, textvariable = tkIntY)
entryy.pack(expand=True)

tkpRoads = tk.DoubleVar(root)
tkpRoads.set(0.6)
labelRoads = tk.Label(root, text="Chance of roads (recommended 0.6):")
labelRoads.pack(expand=True)
entryRoads = tk.Entry(root, textvariable = tkpRoads)
entryRoads.pack(expand=True)

tkpWalls = tk.DoubleVar(root)
tkpWalls.set(0.1)
labelWalls = tk.Label(root, text="Chance of walls (recommended 0.1):")
labelWalls.pack(expand=True)
entryWalls = tk.Entry(root, textvariable = tkpWalls)
entryWalls.pack(expand=True)

enter_button = tk.Button(root, text="Enter", command=save_numbers)
enter_button.pack(expand=True)

# Start the main event loop
root.mainloop()


### GAME WINDOW

mapArray = []
trainArray = [0] * mapY
trainLength = 20
obsArr = []
# wall colour
wallC = [0.5,1,0.5]
obsC = [1,0.5,0]
obsCT = [0,0.5,1]


mapArray.append([1]*mapX)
for i in range(mapY-2):
    mapArray.append([1]+[0] * (mapX-2)+[1])
mapArray.append([1]*mapX)

# obstacles can only go on map == 3
# person can go on 0 or 3
# walls are 1

# approx percentage of mapArr that is roads
# roads go across entire map except wall
percentRoads = tkpRoads.get()
percentWalls = tkpWalls.get()

# first and last row are safe (not including walls)
# skip first 2 and last 2
for i in range(2,len(mapArray)-2):
    if random.random() < percentRoads:
        roadDecide = random.random()
        if roadDecide <= 0.4:
            mapArray[i] = [1]+[3] * (mapX-2)+[1]
        elif roadDecide > 0.4 and roadDecide <=0.8:
            mapArray[i] = [1]+[4] * (mapX-2)+[1]
        else:
            mapArray[i] = [1]+[5] * (mapX-2)+[1]
    else:
        # else, randomly generate walls
        wallMax = mapX - 1
        for j in range(1,len(mapArray[i])-1):
            if random.random() < percentWalls and wallMax > 0:
                mapArray[i][j] = 1
                wallMax = wallMax - 2

# checking each position in map
# for each value of each row
for i in range(len(mapArray)):
    for j in range(len(mapArray[1])):
        if mapArray[i][j] == 1:
            mapArray[i][j] = wallC
            #list(np.random.uniform(0,1,3))
        # if mapArray[i][j] == 2:
        #     mapArray[i][j] = list(np.random.uniform(0,1,3))

# starting position
posx, posy = (1,1)
# top right corner
exitx = len(mapArray)-1
# initial rotation
# pi/4 is looking 180/4 -> 45 degrees NE
rot = np.pi/4 

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
            if mapArray[int(x)][int(y)] != 0 and mapArray[int(x)][int(y)] != 3 and mapArray[int(x)][int(y)] != 4 and mapArray[int(x)][int(y)] != 5:
                # calculates height relative to player
                # height = 1/(height_mult*ray_sens*n)

                # colour assignment
                height = np.clip(1/(height_mult*ray_sens*n), 0, 1)
                c = np.asarray(mapArray[int(x)][int(y)]) * (0.3 + 0.7 * height**2)

                break
                

        # -height to +height to make camera at a angle of 0 relative to ground
        if mapArray[int(x)][int(y)] == wallC:
            plt.vlines(i, -height, height, lw=8, colors=c)
        elif mapArray[int(x)][int(y)] == obsC or mapArray[int(x)][int(y)] == obsCT:
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
    if mapArray[int(x)][int(y)] == 0 or mapArray[int(x)][int(y)] == 3 or mapArray[int(x)][int(y)] == 4 or mapArray[int(x)][int(y)] == 5:
        if np.ceil(posx) == exitx:
            ### ENDING WINDOW
            root = tk.Tk()
            root.geometry("300x300")
            root.title("Congratulations!")
            finLabel = tk.Label(root, text="You reached salvation...")
            finLabel.pack(expand=True)
            root.mainloop()

            break

        posx, posy = (x,y)
    # death if touching car
    elif mapArray[int(x)][int(y)] == obsC or mapArray[int(x)][int(y)] == obsCT:
        ### ENDING WINDOW
        root = tk.Tk()
        root.geometry("300x300")
        root.title("Unfortunate...")
        finLabel = tk.Label(root, text="Your life was stolen.")
        finLabel.pack(expand=True)
        root.mainloop()

        break
    
    # Checking and updating obs positions
    for obs in obsArr:
        # will update positions plus indicate whether or not to remove from obs arr
        # obs arr has positions of obs, mapArray is merely the rendering
        mapArray = obs.updatePos(mapArray)

    # if valid, do not remove
    obsArr = [obs for obs in obsArr if obs.checkPos()]

    # if carExist==True:
    #     mapArray[int(carposx)][int(carposy)] = [1,1,1]
    #     carposy_next = carposy + 0.5
        
    #     print(f"Current car pos: y={carposx}, x={carposy}")
    
    #     # hit a wall
    #     if mapArray[int(carposx)][int(carposy_next)] == [0.1,0.1,0.1]:
    #         carExist = False
    #         print("CAR DEAD")
    #         mapArray[int(carposx)][int(carposy)] = 0
    #     # if empty next path, car moves
    #     # will overlap (no collision between self)
    #     elif mapArray[int(carposx)][int(carposy_next)] == 0 or [1,1,1]:
    #         mapArray[int(carposx)][int(carposy)] = 0
    #         mapArray[int(carposx)][int(carposy_next)] = [1,1,1]
    #         carposy = carposy_next
    #         print("NEW CAR CREATED")
        
    # OBSTACLE SPAWN

    # for each row
    for i in range(len(mapArray)):
        # if a road

        # 10% chance of obstacle spawning per tick
        percentObs = random.randrange(2)*0.02
        percentObsSpawn = random.random()
        # spawn car
        if percentObsSpawn < percentObs:
            # car going right
            if mapArray[i][2] == 3:
                mapArray[i][1] = obsC
                # creates car object, no check for collisions yet
                obsArr.append(Obstacle(i,1,obsC,wallC,"R"))
            # car going left
            elif mapArray[i][len(mapArray[i])-3] == 4:
                mapArray[i][len(mapArray[i])-2] = obsC
                # creates car object, no check for collisions yet
                obsArr.append(Obstacle(i,len(mapArray[i])-2,obsC,wallC,"L"))
            # if entire train road empty
            elif trainArray[i] <= 0 and mapArray[i][len(mapArray[i])-3] == 5:
                trainArray[i] = trainLength
            
    for i in range(len(trainArray)):
        # checking if train reaminds on rail
        if trainArray[i] > 0:
            print("TRAIN REMAINS -> ADDING NEW TRAIN BLOCK")
            trainArray[i] = trainArray[i] - 1
            mapArray[i][1] = obsCT
            # creates car object, no check for collisions yet
            obsArr.append(Obstacle(i,1,obsCT,wallC,"RT"))

    # checking each position in map
    # for each value of each row
    for i in range(len(mapArray)):
        for j in range(len(mapArray[1])):
            # in case map array entry is == 2, change to proper colour
            if mapArray[i][j] == 2:
                mapArray[i][j] = obsC

    # if objTick%4==0:
    #     carExist=True
    #     carposx,carposy= (5,1)
    #     mapArray[int(carposx)][int(carposy)] = [1,1,1]

plt.close()





