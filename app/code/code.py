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
        self.isDead=False
        self.x=x
        self.y=y
        self.sprite=Sprite(texture,x,y)
        self.kind=kind
        self.map[x][y]=self.map[x][y] | kind

    def setPosition(self,x,y):
        self.map[self.x][self.y]=self.map[self.x][self.y] ^ self.kind
        self.x=x%21
        self.y=y%21
        self.sprite.moveTo(self.x,self.y)
        self.map[self.x][self.y]=self.map[self.x][self.y] | self.kind

    def getPosition(self):
        return (self.x,self.y)
    def aroundInfo(self):
        return self.board.aroundInfo(self.x,self.y);

    def remove(self):
        self.map[self.x][self.y]=self.map[self.x][self.y] ^ self.kind
        self.sprite.remove()

    def setToDead(self):
        self.isDead=True
        self.sprite.setTexture("cloud fire")

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
        board.removeSprite(x,y)
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
        self.applesOnBoard=0
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
        p=self.positionInfo(x%21,y%21);
        return ( p & has ) or ( p == 0 )

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
        if self.map[x][y] & APPLE:
            return
        self.removeSprite(x,y)
        self.applesOnBoard+=1
        self.sprites[x][y]=Sprite('apple',x,y)
        self.map[x][y]=self.map[x][y] | APPLE

    def removeApple(self,x,y):
        if self.map[x][y] & APPLE:
            if self.sprites[x][y]!=None:
                self.sprites[x][y].remove()
            self.map[x][y]=self.map[x][y] ^ APPLE
            self.applesOnBoard-=1


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

def findPath(node,record):
    def getNext(record,pos,path):
        (px,py)=record[pos[0]][pos[1]]
        if px==pos[0] and py==pos[1]:
            return path
        else:
            path.insert(0,pos)
        return getNext(record,(px,py),path)
    (x,y)=node['end']
    return getNext(record,(x,y),[])

def bfs(map,start,lookingFor):
    found=[]
    frontier=[start]
    record=recordMap()
    record[start[0]][start[1]]=start

    lookingForTypes=0
    for t in lookingFor:
        lookingForTypes = lookingForTypes | t

    if lookingForTypes==0:
        return (found,record)
    while len(frontier)!=0:
        pos=frontier.pop(0)
        for (x,y) in adjacentPos(pos[0],pos[1]):
            if (not (0<=x<21 and 0<=y<21)) or record[x][y]!=None:
               pass
            elif map[x][y] & lookingForTypes:
                record[x][y]=pos
                for t,v in lookingFor.items():
                    if (t & map[x][y]) and (v>0):
                        found.append( { 'start':start,'end':(x,y),'kind':t } )
                        lookingFor[t] -= 1
                        if lookingFor[t] == 0 :
                            lookingForTypes = lookingForTypes ^ t
                if lookingForTypes==0:
                    return (found,record)
                frontier.append((x,y))
            elif not (map[x][y] & WALL):
                record[x][y]=pos
                frontier.append((x,y))
    return (found,record)

board=Board((1,1),(1,18),(3,3))

def resetAfterDead():
    print "You are dead!\nscore:score",board.player.score
    alert("You are dead!\nscore:"+str(board.player.score))
    board.reset((1,1),(1,18),(3,3))

def winGame():
    print "You win!\nscore:score",board.player.score
    alert("You win!\nscore:"+str(board.player.score))
    board.reset((1,1),(1,18),(3,3))

def monstersAgent():
    (res,record)=bfs(board.map,board.player.getPosition(),{MONSTER:2})
    for m in res:
        if m['kind']!=MONSTER:
            continue;
        path=findPath(m,record)
        monster=board.getMonster(m['end'])
        if len(path)==1:
            monster.setPosition(m['start'][0],m['start'][1])
            if not board.player.isDead:
                async(resetAfterDead,0.2)
            board.player.setToDead()
            break # dead
        monster.setPosition(path[-2][0],path[-2][1])

def key(k,id):
    print k,id
    if board.player.isDead:
        return
    if id=="Up":
        if board.player.okToMove("up",EMPTY | APPLE):
            board.player.move("up")
    elif id=="Down":
        if board.player.okToMove("down",EMPTY | APPLE):
            board.player.move("down")
    elif id=="Left":
        if board.player.okToMove("left",EMPTY | APPLE):
            board.player.move("left")
    elif id=="Right":
        if board.player.okToMove("right",EMPTY | APPLE):
            board.player.move("right")
    elif k==82:
        board.reset((1,1),(1,18),(3,3))
        return
    else:
        return

    monstersAgent()

    if board.applesOnBoard==0:
        async(winGame,0.2)



keydown(key)
