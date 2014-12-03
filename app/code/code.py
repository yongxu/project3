import random
EMPTY=0
WALL=1
MONSTER=2
PLAYER=3
APPLE=4
OUTSIDEMAP=-1
class Minion():
    def __init__(self,board,kind,texture,x,y):
        self.board=board
        self.map=board.map
        self.x=x
        self.y=y
        self.sprite=Sprite(texture,x,y)
        self.kind=kind
        self.map[x][y]=kind
    def setPosition(self,x,y):
        self.map[self.x][self.y]=EMPTY
        self.x=x
        self.y=y
        self.sprite.moveTo(x,y)
        self.map[x][y]=self.kind
    def getPosition(self):
        return (self.x,self.y)
    def aroundInfo(self):
        return self.board.aroundInfo(self.x,self.y);



class Board():
    def __init__(self,playerPos,monster1Pos,monster2Pos):
        self.map=[]
        for i in range(0,21):
            self.map.append([])
            for j in range(0,21):
                self.map[i].append(EMPTY)
        self.createWalls()
        self.player=Minion(self,PLAYER,"player",playerPos[0],playerPos[1])
        self.monsters=[Minion(self,PLAYER,"draco green",monster1Pos[0],monster1Pos[1]),
                       Minion(self,PLAYER,"draco black",monster2Pos[0],monster2Pos[1])]
    def positionInfo(self,x,y):
        if not (0<=x<21 and 0<=y<21):
            return OUTSIDEMAP;
        else:
            return self.map[x][y]
    def randomFind(self,target):
        x=random.randint(0,20)
        y=random.randint(0,20)
        if self.map[x][y]==target:
            return (x,y)
        else:
            return self.randomFind(target)


    def aroundInfo(self,x,y):
        return {'up':self.positionInfo(x,y-1),
                'down':self.positionInfo(x,y+1),
                'left':self.positionInfo(x+1,y),
                'right':self.positionInfo(x-1,y)}
    def createWall(self,x,y):
        Sprite('wall',x,y)
        self.map[x][y]=1
    def createWalls(self):
        for i in range(1,22):
            self.createWall(i-1,21-1)
            self.createWall(i-1,21-1)
            self.createWall(i-1, 1-1)
        for i in [1,11,21]:
            self.createWall(i-1,20-1)
        for i in [1, 3,4,5, 7,8,9, 11, 13,14,15, 17,18,19, 21]:
            self.createWall(i-1,19-1)
        for i in [1,21]:
            self.createWall(i-1,18-1)
        for i in [1, 3,4,5, 7 ,9,10,11,12,13 ,15, 17,18,19, 21]:
            self.createWall(i-1,17-1)
        for i in [1, 7, 11, 15, 21]:
            self.createWall(i-1,16-1)
        for i in [1,2,3,4,5, 7,8,9, 11, 13,14,15, 17,18,19,20,21]:
            self.createWall(i-1,15-1)
        for i in [1,2,3,4,5, 7,  15, 17,18,19,20,21]:
            self.createWall(i-1,14-1)
        for i in [1,2,3,4,5, 7, 9,10,11,12,13, 15, 17,18,19,20,21]:
            self.createWall(i-1,13-1)
        for i in [ 9,10,11,12,13, ]:
            self.createWall(i-1,12-1)
        for i in [1,2,3,4,5, 7, 9,10,11,12,13, 15, 17,18,19,20,21]:
            self.createWall(i-1,11-1)
        for i in [1,2,3,4,5, 7,  15, 17,18,19,20,21]:
            self.createWall(i-1,10-1)
        for i in [1,2,3,4,5, 7, 9,10,11,12,13, 15, 17,18,19,20,21]:
            self.createWall(i-1,9-1)
        for i in [1,11,21]:
            self.createWall(i-1,8-1)
        for i in [1, 3,4,5, 7,8,9, 11, 13,14,15, 17,18,19, 21]:
            self.createWall(i-1,7-1)
        for i in [1 ,5, 17,21]:
            self.createWall(i-1,6-1)
        for i in [1,2,3, 5, 7, 9,10,11,12,13, 15, 17, 19,20,21]:
            self.createWall(i-1,5-1)
        for i in [1 ,7, 11, 15,21]:
            self.createWall(i-1,4-1)
        for i in [1, 3,4,5,6,7,8,9, 11, 13,14,15,16,17,18,19, 21]:
            self.createWall(i-1,3-1)
        for i in [1, 21]:
            self.createWall(i-1,2-1)

board=Board((1,1),(2,2),(3,3))

def test():
 #   (x,y)=board.player.getPosition()
#    print board.player.aroundInfo()
    (x,y)=board.randomFind(0)
    board.player.setPosition(x,y)
    (x,y)=board.randomFind(0)
    board.monsters[0].setPosition(x,y)
    (x,y)=board.randomFind(0)
    board.monsters[1].setPosition(x,y)
#    board.player.setPosition((x+1)%20,(y+1)%20)
id=asyncLoop(test,0.1)
# def clearLoop():
#     print "loop stoped!"
#     clearAsyncLoop(id)
# async(clearLoop,5)