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
        self.x=x%21
        self.y=y%21
        self.sprite.moveTo(self.x,self.y)
        self.map[self.x][self.y]=self.kind
    def getPosition(self):
        return (self.x,self.y)
    def aroundInfo(self):
        return self.board.aroundInfo(self.x,self.y);
    def move(self,cmd):
        if cmd=='up':
            self.setPosition(self.x,self.y-1)
        elif cmd=='down':
            self.setPosition(self.x,self.y+1)
        elif cmd=='left':
            self.setPosition(self.x-1,self.y)
        elif cmd=='right':
            self.setPosition(self.x+1,self.y)
    def okToMove(self,cmd,okToLand):
        if cmd=='up':
            return self.board.positionHas(self.x,self.y-1,okToLand)
        elif cmd=='down':
            return self.board.positionHas(self.x,self.y+1,okToLand)
        elif cmd=='left':
            return self.board.positionHas(self.x-1,self.y,okToLand)
        elif cmd=='right':
            return self.board.positionHas(self.x+1,self.y,okToLand)

class Player(Minion):
    def __init__(self,board,texture,x,y):
        Minion.__init__(self,board,PLAYER,texture,x,y)
    def setPosition(self,x,y):
        self.map[self.x][self.y]=EMPTY
        self.x=x%21
        self.y=y%21
        self.sprite.moveTo(self.x,self.y)
        if self.map[self.x][self.y]==APPLE:
            self.board.removeApple(self.x,self.y)
        self.map[self.x][self.y]=self.kind


class Board():
    def __init__(self,playerPos,monster1Pos,monster2Pos):
        self.map=[]
        self.sprites=[]
        for i in range(0,21):
            self.map.append([])
            self.sprites.append([])
            for j in range(0,21):
                self.map[i].append(EMPTY)
                self.sprites[i].append(None)
        self.createWalls()
        self.player=Player(self,"player",playerPos[0],playerPos[1])
        self.monsters=[Minion(self,PLAYER,"draco green",monster1Pos[0],monster1Pos[1]),
                       Minion(self,PLAYER,"draco black",monster2Pos[0],monster2Pos[1])]
        self.fillWithApples()
    def positionInfo(self,x,y):
        if not (0<=x<21 and 0<=y<21):
            return OUTSIDEMAP;
        else:
            return self.map[x][y]

    def positionHas(self,x,y,list):
        return self.positionInfo(x,y) in list

    def randomFind(self,target):
        x=random.randint(0,20)
        y=random.randint(0,20)
        if self.map[x][y]==target:
            return (x,y)
        else:
            return self.randomFind(target)

    def fillWithApples(self):
        for x in range(0,21):
            for y in range(0,21):
                if self.map[x][y]==EMPTY:
                    self.addApple(x,y)

    def addApple(self,x,y):
        self.sprites[x][y]=Sprite('apple',x,y)
        self.map[x][y]=APPLE

    def removeApple(self,x,y):
        self.sprites[x][y].remove()
        print "removeApple!"
        self.map[x][y]=EMPTY


    def aroundInfo(self,x,y):
        return {'up':self.positionInfo(x,y-1),
                'down':self.positionInfo(x,y+1),
                'left':self.positionInfo(x-1,y),
                'right':self.positionInfo(x+1,y)}
    def createWall(self,x,y):
        self.sprites[x][y]=Sprite('wall',x,y)
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

board=Board((1,1),(1,18),(3,3))

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
#id=asyncLoop(test,0.1)
# def clearLoop():
#     print "loop stoped!"
#     clearAsyncLoop(id)
# async(clearLoop,5)

def key(k,id):
    print k,id
    if id=="Up":
        if board.player.okToMove("up",[EMPTY,APPLE]):
            board.player.move("up")
    elif id=="Down":
        if board.player.okToMove("down",[EMPTY,APPLE]):
            board.player.move("down")
    elif id=="Left":
        if board.player.okToMove("left",[EMPTY,APPLE]):
            board.player.move("left")
    elif id=="Right":
        if board.player.okToMove("right",[EMPTY,APPLE]):
            board.player.move("right")

keydown(key)
