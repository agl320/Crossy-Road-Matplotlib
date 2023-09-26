import math
# Obstacle object
# carx,cary position in mapArray
# for car in carlist
#   render car
#       delete past carx,cary
#       create new carx,cary_next

class Obstacle():
    def __init__(self, obsx, obsy, obsC, wallC, dir):
        self.obsx = obsx 
        self.obsy = obsy  
        self.obsC = obsC
        self.wallC = wallC
        self.dir = dir
        self.validPos = True

    def updatePos(self, mapArray):

        mapArray[int(self.obsx)][int(self.obsy)] = [1,1,1]
        print(f"Car pos: ({int(self.obsx)},{int(self.obsy)}) wtih dir: {self.dir}")
        
        if self.dir == "R":
            obsy_next = self.obsy + 0.5
        
            # hit a wall
            if mapArray[int(self.obsx)][int(obsy_next)] == self.wallC:
                self.validPos = False
                print("CAR DEAD")
                mapArray[int(self.obsx)][int(self.obsy)] = 3
            # if empty next path, car moves
            # will overlap (no collision between self)
            elif mapArray[int(self.obsx)][int(obsy_next)] == 3 or self.obsC:
                
                mapArray[int(self.obsx)][int(self.obsy)] = 3
                mapArray[int(self.obsx)][int(obsy_next)] = self.obsC
                self.obsy = obsy_next
                print("NEW CAR CREATED")

        elif self.dir == "L":
            obsy_next = self.obsy - 0.5
        
            # hit a wall
            if mapArray[int(math.floor(self.obsx))][int(math.floor(obsy_next))] == self.wallC:
                self.validPos = False
                print("CAR DEAD")
                mapArray[int(math.floor(self.obsx))][int(math.floor(self.obsy))] = 4
            # if empty next path, car moves
            # will overlap (no collision between self)
            elif mapArray[int(math.floor(self.obsx))][math.floor(obsy_next)] == 4 or self.obsC:
                
                mapArray[int(math.floor(self.obsx))][int(math.floor(self.obsy))] = 4
                mapArray[int(math.floor(self.obsx))][math.floor(obsy_next)] = self.obsC
                self.obsy = obsy_next
                print("NEW CAR CREATED")

        elif self.dir == "RT":
            obsy_next = self.obsy + 0.5
        
            # hit a wall
            if mapArray[int(self.obsx)][int(obsy_next)] == self.wallC:
                self.validPos = False
                print("TRAIN DEAD")
                mapArray[int(self.obsx)][int(self.obsy)] = 5
            # if empty next path, car moves
            # will overlap (no collision between self)
            elif mapArray[int(self.obsx)][int(obsy_next)] == 5 or self.obsC:
                
                mapArray[int(self.obsx)][int(self.obsy)] = 5
                mapArray[int(self.obsx)][int(obsy_next)] = self.obsC
                self.obsy = obsy_next
                print("NEW TRAIN BLOCK CREATED")


        return mapArray
    
    def checkPos(self):
        return self.validPos
    