import random
from math import *

BOARD_SIZE=21

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
        self.map[self.x][self.y]=self.map[self.x][self.y] & (~self.kind)
        self.x=x%BOARD_SIZE
        self.y=y%BOARD_SIZE
        self.sprite.moveTo(self.x,self.y)
        self.map[self.x][self.y]=self.map[self.x][self.y] | self.kind

    def getPosition(self):
        return (self.x,self.y)
    def aroundInfo(self):
        return self.board.aroundInfo(self.x,self.y);

    def remove(self):
        self.map[self.x][self.y]=self.map[self.x][self.y] & (~self.kind)
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
        if board.map[x][y] & APPLE:
            board.removeApple(x,y)
        else:
            board.removeSprite(x,y)
        Minion.__init__(self,board,PLAYER,texture,x,y)
    def setPosition(self,x,y):
        x=x%BOARD_SIZE
        y=y%BOARD_SIZE
        if self.map[x][y] & APPLE:
            self.score=self.score+1
            self.board.removeApple(x,y)
        elif self.map[x][y]==MONSTER:
            #here,dead
            return #dead
        Minion.setPosition(self,x,y)


class Board():
    def __init__(self,playerPos=None,monster1Pos=None,monster2Pos=None):
        self.map=[]
        self.sprites=[]
        self.applesOnBoard=0
        for i in range(0,BOARD_SIZE):
            self.map.append([])
            self.sprites.append([])
            for j in range(0,BOARD_SIZE):
                self.map[i].append(EMPTY)
                self.sprites[i].append(None)
        self.createWalls()
        self.fillWithApples()
        if playerPos!=None:
            self.setSpritesPosition(playerPos,monster1Pos,monster2Pos)

    def setSpritesPosition(self,playerPos,monster1Pos,monster2Pos):
        self.player=Player(self,"player",playerPos[0],playerPos[1])
        self.monsters=[Minion(self,MONSTER,"draco green",monster1Pos[0],monster1Pos[1]),
                       Minion(self,MONSTER,"draco black",monster2Pos[0],monster2Pos[1])]

    def reset(self,playerPos=None,monster1Pos=None,monster2Pos=None):
        removeAllSprites()
        if playerPos!=None:
            self.__init__(playerPos,monster1Pos,monster2Pos)
        else:
            self.__init__()

    def getMonster(self,pos):
        for m in self.monsters:
            if m.getPosition()==pos:
                return m
        return None

    def mapCopy(self):
        cp=[]
        for i in range(0,BOARD_SIZE):
            cp.append([])
            for j in range(0,BOARD_SIZE):
                cp[i].append(self.map[i][j])
        return cp

    def getSprite(self,pos):
        return self.sprites[pos[0]][pos[1]]

    def positionInfo(self,x,y):
        if not (0<=x<BOARD_SIZE and 0<=y<BOARD_SIZE):
            return OUTSIDEMAP;
        else:
            return self.map[x][y]

    def positionHas(self,x,y,has):
        p=self.positionInfo(x%BOARD_SIZE,y%BOARD_SIZE);
        return ( p & has ) or ( p == 0 )

    def randomFind(self,target):
        x=random.randint(0,20)
        y=random.randint(0,20)
        if self.map[x][y]==target:
            return (x,y)
        else:
            return self.randomFind(target)

    def fillWithApples(self):
        for x in range(0,BOARD_SIZE):
            for y in range(0,BOARD_SIZE):
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
            self.map[x][y]=self.map[x][y] & (~APPLE)
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
    for i in range(0,BOARD_SIZE):
        map.append([])
        for j in range(0,BOARD_SIZE):
            map[i].append(None)
    return map

def adjacentPos(x,y):
    return [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]

def findPath(node,record):
    def getNext(record,pos,path):
        ((px,py),cost)=record[pos[0]][pos[1]]
        if px==pos[0] and py==pos[1]:
            return path
        else:
            path.insert(0,pos)
        return getNext(record,(px,py),path)
    (x,y)=node['end']
    return getNext(record,(x,y),[])

def bfs(map,start,lookingFor,finishMap=False):
    found=[]
    frontier=[(start,0)]
    record=recordMap()
    record[start[0]][start[1]]=(start,0)

    lookingForTypes=0
    for t in lookingFor:
        lookingForTypes = lookingForTypes | t

    if lookingForTypes ==0 and (not finishMap):
        return (found,record)

    # check the if target is right at start
    for t,v in lookingFor.items():
        if (t & map[start[0]][start[1]]) and (v>0):
            found.append( { 'start':start,'end':start,'kind':t } )
            lookingFor[t] -= 1
            if lookingFor[t] == 0 :
                lookingForTypes = lookingForTypes & (~t)

    while len(frontier)!=0:
        (pos,cost)=frontier.pop(0)
        for (x,y) in adjacentPos(pos[0],pos[1]):
            if (not (0<=x<BOARD_SIZE and 0<=y<BOARD_SIZE)) or record[x][y]!=None:
               pass
            elif map[x][y] & lookingForTypes:
                record[x][y]=(pos,cost+1)
                for t,v in lookingFor.items():
                    if (t & map[x][y]) and (v>0):
                        found.append( { 'start':start,'end':(x,y),'kind':t } )
                        lookingFor[t] -= 1
                        if lookingFor[t] == 0 :
                            lookingForTypes = lookingForTypes & (~t)
                if lookingForTypes==0 and (not finishMap):
                    return (found,record)
                frontier.append(((x,y),cost+1))
            elif not (map[x][y] & WALL):
                record[x][y]=(pos,cost+1)
                frontier.append(((x,y),cost+1))
    return (found,record)

def costToPlayer(pos):
    (x,y)=pos
    if record[x][y] != None:
        return record[x][y][1]
    else:
        return -1



#board=Board((1,1),(1,18),(3,3))

board=Board()

def monstersAgent():
    (res,record)=bfs(board.map,board.player.getPosition(),{MONSTER:2})
    for m in res:
#        print m,findPath(m,record)
        if m['kind']!=MONSTER:
            continue;
        path=findPath(m,record)
        monster=board.getMonster(m['end'])
        if len(path)<2:
            monster.setPosition(m['start'][0],m['start'][1]) 
            if not board.player.isDead:
                async(resetAfterDead,0.2)
            board.player.setToDead()
            break # dead
        if board.map[path[-2][0]][path[-2][1]] & MONSTER:
            continue
        monster.setPosition(path[-2][0],path[-2][1])

def HvsC_keyDetect(k,id):
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



#keydown(key)


def mapCopy(map):
    cp=[]
    for i in range(0,BOARD_SIZE):
        cp.append([])
        for j in range(0,BOARD_SIZE):
            cp[i].append(map[i][j])
    return cp

def stateHeuristic(state,map):
    (px,py)=state[0][-1]
    (mx1,my1)=state[1][-1]
    (mx2,my2)=state[2][-1]


    if ( px==mx1 and py==my1 ) or ( px==mx2 and py==my2 ):
        return (-1000000,state) #dead

    v=min(distance((px,py),(mx1,my1)),4)+min(distance((px,py),(mx2,my2)),4)
    if map[px][py]==APPLE:
        v+=3
    (res,record)=bfs(map,(px,py),{APPLE:3})
    appleCount=0.0
    applesWeight=0.0
    for ap in res:
        applesWeight-=distance((px,py),ap['end'])
    v+=applesWeight/max(1,appleCount)
    return (v,state)

def validActions(pos,map):
    actions=[]
    for (x,y) in adjacentPos(pos[0],pos[1]):
        if map[x][y]!=WALL and (0<=x<BOARD_SIZE and 0<=y<BOARD_SIZE):
            actions.append((x,y))
    return actions

def validPlayerActions(state):
    pos=state[0][-1] #player path last
    (mx1,my1)=state[1][-1] #monster 1 path last
    (mx2,my2)=state[2][-1] #monster 2 path last
    map=board.map

    actions=[]
    for (x,y) in adjacentPos(pos[0],pos[1]):
        x=x%BOARD_SIZE
        y=y%BOARD_SIZE
        if map[x][y]!=WALL and ( x!=mx1 or y!=my1 ) and ( x!=mx2 or y!=my2 ):
            actions.append((x,y))
    return actions

def validMonstersActions(state):
    mp1=state[1][-1]
    mp2=state[2][-1] 

    actions=[]
    for p1 in validActions(mp1,board.map):
        for p2 in validActions(mp2,board.map):
            actions.append((p1,p2))
    return actions

def alphaBetaSearch(board,depth):
    a=float('-inf')
    b=float('inf')
    map=board.map

    #player path, monster 1 path, monster 2 path
    state=([board.player.getPosition()],
            [board.monsters[0].getPosition()],[board.monsters[1].getPosition()])
    def maxValue(state,a,b,depth):
 #       print depth, 'max:',a,b,state
        if depth==0: 
            return stateHeuristic(state,map)
        v=float('-inf')
        for action in validPlayerActions(state):
            (minV,minS)=minValue( (state[0]+[action],state[1],state[2]), a,b,depth-1)
            if minV>v:
                (v,s)=(minV,minS)
            if v>=b:
                return (v,s)
            a=max(a,v)
        return (v,s)

    def minValue(state,a,b,depth):
 #       print depth, 'min:',a,b,state
        if depth==0: 
            return stateHeuristic(state,map)
        v=float('inf')
        for a1,a2 in validMonstersActions(state):
            (maxV,maxS)=maxValue( (state[0],state[1]+[a1],state[2]+[a2]), a,b,depth-1)
            if maxV<v:
                (v,s)=(maxV,maxS)
            if v<=a:
                return (v,s)
            b=min(b,v)
        return (v,s)

    (v,actions)=maxValue(state,a,b,depth)
    return actions

def playerAgent():
    actions=alphaBetaSearch(board,2)
    print actions
    board.player.setPosition(actions[0][1][0],actions[0][1][1])
    if len(validPlayerActions(actions))==0:
            if not board.player.isDead:
                async(resetAfterDead,0.2)
            board.player.setToDead()

def autoPlay():
    if board.player.isDead:
        return
    print 'player move'
    playerAgent()
    if board.applesOnBoard==0:
        async(winGame,0.2)
        return
    print 'monsters move'
    monstersAgent()
    if not board.player.isDead:
        async(autoPlay,0.2)

def resetGame():
    board.reset()
    cleanUpEvents()
    (x1,y1)=board.randomFind(APPLE)
    (x2,y2)=board.randomFind(APPLE)
    (x3,y3)=board.randomFind(APPLE)

    if ( x1!=x2 or y1!=y2 ) and ( x1!=x2 or y1!=y2 ) and ( x2!=x3 or y2!=y3 ):
        board.setSpritesPosition((x1,y1),(x2,y2),(x3,y3))
    else:
        resetGame()

def choosePlayMode():
    resetGame()
    res=prompt('Choose game mode:\n 1: Auto Play, 2: Human vs Computer','1')
    while True:
        if not res:
            return
        elif res=='1':
            autoPlay()
            return
        elif res=='2':
            keydown(HvsC_keyDetect)
            return
        res=prompt('Invalid Input!!!\n Valid input: 1 or 2.\n 1: Auto Play, 2: Human vs Computer','1')


def resetAfterDead():
    print "You are dead!\nscore:score",board.player.score
    alert("You are dead!\nscore:"+str(board.player.score))
    #board.reset((1,1),(1,18),(3,3))
    choosePlayMode()

def winGame():
    print "You win!\nscore:score",board.player.score
    alert("You win!\nscore:"+str(board.player.score))
    #board.reset((1,1),(1,18),(3,3))
    choosePlayMode()

choosePlayMode()