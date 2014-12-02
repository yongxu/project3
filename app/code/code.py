EMPTY=0
WALL=1
BADGUY=2
PLAYER=3
class Board():
    def __init__(self):
        self.map=[]
        self.player=None
        for i in range(0,21):
            self.map.append([])
            for j in range(0,21):
                self.map[i].append(EMPTY)
    def addWall(self,x,y):
        self.map[x][y]=1
    def playerPosition(self,x,y):
        self.playerPos=(x,y)
        if self.player == None:
            self.player=Sprite('player',x,y)
        else:
            self.player.moveTo(x,y)
    def getPlayerPos(self):
        return self.playerPos

board=Board()
def createWall(x,y):
    Sprite('wall',x,y)
    board.addWall(x,y)
def createObstacles():
    # create obstacles, saving the grid location of each
    for i in range(1,22):
        createWall(i-1,21-1)
        createWall(i-1,21-1)
        createWall(i-1, 1-1)
    for i in [1,11,21]:
        createWall(i-1,20-1)
    for i in [1, 3,4,5, 7,8,9, 11, 13,14,15, 17,18,19, 21]:
        createWall(i-1,19-1)
    for i in [1,21]:
        createWall(i-1,18-1)
    for i in [1, 3,4,5, 7 ,9,10,11,12,13 ,15, 17,18,19, 21]:
        createWall(i-1,17-1)
    for i in [1, 7, 11, 15, 21]:
        createWall(i-1,16-1)
    for i in [1,2,3,4,5, 7,8,9, 11, 13,14,15, 17,18,19,20,21]:
        createWall(i-1,15-1)
    for i in [1,2,3,4,5, 7,  15, 17,18,19,20,21]:
        createWall(i-1,14-1)
    for i in [1,2,3,4,5, 7, 9,10,11,12,13, 15, 17,18,19,20,21]:
        createWall(i-1,13-1)
    for i in [ 9,10,11,12,13, ]:
        createWall(i-1,12-1)
    for i in [1,2,3,4,5, 7, 9,10,11,12,13, 15, 17,18,19,20,21]:
        createWall(i-1,11-1)
    for i in [1,2,3,4,5, 7,  15, 17,18,19,20,21]:
        createWall(i-1,10-1)
    for i in [1,2,3,4,5, 7, 9,10,11,12,13, 15, 17,18,19,20,21]:
        createWall(i-1,9-1)
    for i in [1,11,21]:
        createWall(i-1,8-1)
    for i in [1, 3,4,5, 7,8,9, 11, 13,14,15, 17,18,19, 21]:
        createWall(i-1,7-1)
    for i in [1 ,5, 17,21]:
        createWall(i-1,6-1)
    for i in [1,2,3, 5, 7, 9,10,11,12,13, 15, 17, 19,20,21]:
        createWall(i-1,5-1)
    for i in [1 ,7, 11, 15,21]:
        createWall(i-1,4-1)
    for i in [1, 3,4,5,6,7,8,9, 11, 13,14,15,16,17,18,19, 21]:
        createWall(i-1,3-1)
    for i in [1, 21]:
        createWall(i-1,2-1)


createObstacles();
board.playerPosition(1,1)
print board.getPlayerPos()
