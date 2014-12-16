import random
from math import *
EMPTY=0
WALL=1
MONSTER=2
PLAYER=4
NOT_MONSTER_PLAYER=~(MONSTER+PLAYER)
MONSTER_PLAYER=(MONSTER+PLAYER)
APPLE=8
OUTSIDEMAP=1024

class Minion():
    def __init__(self,board,kind,texture,x,y):
        self.board=board
        self.map=board.map
        self.x=x
        self.y=y
        board.removeSprite(x,y)
        self.sprite=Sprite(texture,x,y)
        self.kind=kind
        self.map[x][y]=self.map[x][y] ^ kind

    def setPosition(self,x,y):
        self.map[self.x][self.y]=self.map[self.x][self.y] & (~ self.kind)
        self.x=x%21
        self.y=y%21
        self.sprite.moveTo(self.x,self.y)
        self.map[self.x][self.y]=self.map[self.x][self.y] ^ self.kind

    def getPosition(self):
        return (self.x,self.y)
    def aroundInfo(self):
        return self.board.aroundInfo(self.x,self.y);

    def remove(self):
        self.map[self.x][self.y]=self.map[self.x][self.y] & (~ self.kind)
        self.sprite.remove()

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
        self.score=0
        Minion.__init__(self,board,PLAYER,texture,x,y)
    def setPosition(self,x,y):
        x=x%21
        y=y%21
        if self.map[x][y] & APPLE:
            self.score=self.score+1
            self.board.removeApple(x,y)
        elif self.map[x][y]==MONSTER:
            #here,dead
            return #dead
        Minion.setPosition(self,x,y)


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
        self.fillWithApples()
        self.player=Player(self,"player",playerPos[0],playerPos[1])
        self.monsters=[Minion(self,MONSTER,"draco green",monster1Pos[0],monster1Pos[1]),
                       Minion(self,MONSTER,"draco black",monster2Pos[0],monster2Pos[1])]

    def reset(self,playerPos,monster1Pos,monster2Pos):
        removeAllSprites()
        self.__init__(playerPos,monster1Pos,monster2Pos)

    def getMonster(self,pos):
        for m in self.monsters:
            if m.getPosition()==pos:
                return m
        return None

    def mapCopy(self):
        cp=[]
        for i in range(0,21):
            cp.append([])
            for j in range(0,21):
                cp[i].append(self.map[i][j])
        return cp

    def getSprite(self,pos):
        return self.sprites[pos[0]][pos[1]]

    def positionInfo(self,x,y):
        if not (0<=x<21 and 0<=y<21):
            return OUTSIDEMAP;
        else:
            return self.map[x][y]

    def positionHas(self,x,y,has):
        return (self.positionInfo(x%21,y%21) & (~has))==0

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
        self.removeSprite(x,y)
        self.sprites[x][y]=Sprite('apple',x,y)
        self.map[x][y]=self.map[x][y] ^ APPLE

    def removeApple(self,x,y):
        if self.map[x][y] & APPLE:
            if self.sprites[x][y]!=None:
                self.sprites[x][y].remove()
            self.map[x][y]=self.map[x][y] & (~APPLE)

    def removeSprite(self,x,y):
        if self.map[x][y] & NOT_MONSTER_PLAYER:
            if self.sprites[x][y]!=None:
                self.sprites[x][y].remove()
            self.map[x][y]=self.map[x][y] & MONSTER_PLAYER


    def aroundInfo(self,x,y):
        return {'up':self.positionInfo(x,y-1),
                'down':self.positionInfo(x,y+1),
                'left':self.positionInfo(x-1,y),
                'right':self.positionInfo(x+1,y)}

    def createWall(self,x,y):
        self.sprites[x][y]=Sprite('wall',x,y)
        self.map[x][y]=WALL

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


def distance(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def recordMap():
    map=[]
    for i in range(0,21):
        map.append([])
        for j in range(0,21):
            map[i].append(None)
    return map

def adjacentPos(x,y):
    return [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]

# class Agent():
#     def __init__(self,board):
#         self.board=board
#         self.map=board.mapCopy()
#         self.player=board.player.getPosition()
#         self.monsters=[m.getPosition() for m in board.monsters]

#     def findClosestApples(self,obj):

def getPath(record,pos,path):
    (px,py)=record[pos[0]][pos[1]]
    if px==pos[0] and py==pos[1]:
        return path
    else:
        path.insert(0,pos)
    return getPath(record,(px,py),path)
def bfs(map,start,Lookingfor,n=-1):
    found=[]
    frontier=[start]
    record=recordMap()
    record[start[0]][start[1]]=start
    while len(frontier)!=0:
        pos=frontier.pop(0)
        for (x,y) in adjacentPos(pos[0],pos[1]):
            if (not (0<=x<21 and 0<=y<21)) or record[x][y]!=None:
               pass
            elif map[x][y] & Lookingfor:
                n=n-1
                record[x][y]=pos
                found.append( { 'start':start,'end':(x,y), 'path':getPath(record,(x,y),[]) } )
                if n==0:
                    return found
                frontier.append((x,y))
            elif not (map[x][y] & WALL):
                record[x][y]=pos
                frontier.append((x,y))
    return found

board=Board((1,1),(1,18),(3,3))
#res=bfs(board.map,(1,1),MONSTER,2)
#res=bfs(board.map,(1,1),APPLE,5)
#print res

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
        if board.player.okToMove("up",EMPTY^APPLE):
            board.player.move("up")
    elif id=="Down":
        if board.player.okToMove("down",EMPTY^APPLE):
            board.player.move("down")
    elif id=="Left":
        if board.player.okToMove("left",EMPTY^APPLE):
            board.player.move("left")
    elif id=="Right":
        if board.player.okToMove("right",EMPTY^APPLE):
            print "right"
            board.player.move("right")
    elif k==82:
        board.reset((1,1),(1,18),(3,3))
        return

    # player_pos=board.player.getPosition();
    # for m in board.monsters:
    #     if m.getPosition() in adjacentPos(player_pos[0],player_pos[1]):
    #         alert("You are dead!")
    #         board.reset((1,1),(1,18),(3,3))
    #         return

    res=bfs(board.map,board.player.getPosition(),MONSTER,len(board.monsters))
    print res
    for m in res:
        monster=board.getMonster(m['end'])
        if len(m['path'])==1:
            return # dead
        monster.setPosition(m['path'][-2][0],m['path'][-2][1])



keydown(key)
