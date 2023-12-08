from platform import node
from Map.Position import Position
from random import shuffle
width = 34
heigth = 59
class Gamemap():

    def __ini__(self):
        self.width = 34
        self.heigth = 59
        self.saved_positions = {
            'gold': [], # its length increases as the bot finds gold and saves its position
            'void': [], 
            'powerup': [], 
            'blocked': [], 
            'safe': [], 
            'unsafe': [], 
            'notvisited': self.setNotVisitedPositions(),  # its length decreases as the bot explores the map and must contain all the positions that have not been visited
            'visited': [],  # its length increases as the bot explores the map and must contain all the positions that have been visited
            'auxGold': []  # it increases as the bot finds gold and catches it
        }
    
    def addPosition(self,type, x,y):
        if type == "gold":
            self.saved_positions['gold'].append((x,y))
        elif type == "unsafe":
            self.saved_positions['unsafe'].append((x,y))
            if ((x,y) in self.saved_positions['notvisited']):
                self.saved_positions['notvisited'].remove((x,y))
        elif type == "safe":
            self.saved_positions['safe'].append((x,y))
        elif type == "block":
            self.saved_positions['blocked'].append((x,y))
            if ((x,y) in self.saved_positions['notvisited']):
                self.saved_positions['notvisited'].remove((x,y))
        elif type == "powerup":
            self.saved_positions['powerup'].append((x,y))

    def setNotVisitedPositions(self):
        self.saved_positions['notvisited'] = []
        for i in range(self.width):
            for j in range(self.heigth):
                position = Position.getPosition(i, j)
                self.saved_positions['notvisited'].append(position)
        return self.saved_positions['notvisited']

    def getGoldPos(self):
        return self.saved_positions['gold']

    def getVoidPos(self):
        return self.saved_positions['void']
    
    def getSafePos(self):
        return self.saved_positions['safe']

    def getBlockedPos(self):
        return self.saved_positions['blocked']
    
    def getPowerupPos(self):
        return self.saved_positions['powerup']
    
    def getUnsafePos(self):
        return self.saved_positions['unsafe']
    
    def getNotVisit(self):
        return self.saved_positions['notvisited']
    
    def getAuxGold(self):
        return self.saved_positions['auxGold']
    
    def populateAuxGoldPos(self,xi,yi):
        goldcopy = self.saved_positions['gold'].copy()
        goldcopy = sorted(goldcopy, key=lambda x: self.manhattan(x[0],x[1],xi,yi))
        first = goldcopy.pop(0)
        self.saved_positions['auxGold'] = goldcopy.copy()
        self.saved_positions['auxGold'].append(first)

    def getNearNode(self,x,y,type):
        if type == "notVisit":
            lista = self.saved_positions['notvisited']
        elif type == "powerup":
            lista = self.saved_positions['powerup']
        elif type == "gold":
            if ((x,y) in self.saved_positions['gold']):
                lista = self.saved_positions['gold'].copy()
                lista.remove((x,y))
                if lista == []:
                    return (10,10)
            else:
                lista = self.saved_positions['gold']
        nearest = lista[0]
        menorValor = self.manhattan(nearest[0],nearest[1],x,y)
        if menorValor == 0 and type == "notVisit":
            self.saved_positions['notvisited'].remove(nearest)
        if menorValor == 1:
            return nearest
        for i in lista[1:]:
            if (not self.isBadPos(i[0],i[1])):
                valor=self.manhattan(i[0],i[1],x,y)
                if valor<menorValor:
                    menorValor = valor
                    nearest = i
                    if menorValor == 0 and type == "notVisit":
                        self.saved_positions['notvisited'].remove(nearest)
                    if menorValor == 1:
                        return nearest
        return nearest

    def nodeCost(self,x,y):
        if(self.isBadPos(x,y)):
            return 5000
        return 1

    def isBadPos(self,x,y):
        return ((x,y) in self.getBlockedPos() or (x,y) in self.getUnsafePos())

    def manhattan(self,x1,y1,x2,y2):
        return abs(x1-x2)+abs(y1-y2)
    
    '''
    A* funciona dando como parametro as coordenadas iniciais, e depois as coordenadas finais, 
    os pesos e custos estão na funçao nodeCost(não deu tempo de fazer direito).
    '''
    def aStar(self,xi,yi,xf,yf):
        aberta=[]
        fechada=[]
        initialNode = Node(xi,yi,0,xf,yf)
        aberta.append(initialNode)
        current = initialNode
        while aberta:
            current = pegaMenor(aberta)
            if (current.x == xf and current.y == yf):
                return current.getPath()
            aberta.remove(current)
            fechada.append(current)
            vizinhos = current.getVizinhos(self.saved_positions['blocked'],self.saved_positions['unsafe'])
            for nextNode in vizinhos:

                inFechada = False
                inAberta = False
                for i in fechada:
                    if(nextNode.x == i.x and nextNode.y == i.y):
                        inFechada = True
                if(not(inFechada)):
                    for i in aberta:
                        if(nextNode.x == i.x and nextNode.y == i.y):
                            inAberta = True
                            if(nextNode.f<i.f):
                                i.f=nextNode.f
                                nextNode.partner = current
                    if(inAberta==False):
                        aberta.append(nextNode)
                        nextNode.partner = current
        print("Caminho não encontrado")
        return None

def pegaMenor(lista):
    menor = lista[0]
    for i in lista[1:]:
        if menor.f > i.f:
            menor = i
    return menor

class Node:
    def __init__(self,x,y,g,xf,yf):
        self.x=x
        self.y=y
        self.xf = xf
        self.yf = yf
        self.h=self.manhattan(xf,yf)
        self.g=g
        self.f = self.g + self.h
        self.partner = None
    
    def manhattan(self,xf,yf):
        return abs(self.x-xf)+abs(self.y-yf)
    
    def isValid(self,x,y):
        return(x>=0 and x<heigth and y>=0 and y<width) 

    def getVizinhos(self, blockedPos, unsafedPos):

        ret = []
        if (self.isValid(self.x-1,self.y)):
            if ((self.x-1,self.y) in blockedPos or (self.x-1,self.y) in unsafedPos):
                cost = 50
            else:
                cost = 1
            ret.append(Node(self.x-1,self.y,self.g+cost,self.xf,self.yf))
        if (self.isValid(self.x+1,self.y)):
            if ((self.x+1,self.y) in blockedPos or (self.x+1,self.y) in unsafedPos):
                cost = 50
            else:
                cost = 1
            ret.append(Node(self.x+1,self.y,self.g+cost,self.xf,self.yf))
        if (self.isValid(self.x,self.y+1)):
            if ((self.x,self.y+1) in blockedPos or (self.x,self.y+1) in unsafedPos):
                cost = 50
            else:
                cost = 1
            ret.append(Node(self.x,self.y+1,self.g+cost,self.xf,self.yf))
        if (self.isValid(self.x,self.y-1)):
            if ((self.x,self.y-1) in blockedPos or (self.x,self.y-1) in unsafedPos):
                cost = 50
            else:
                cost = 1
            ret.append(Node(self.x,self.y-1,self.g+cost,self.xf,self.yf))
        return ret

    def getPath(self):
        temp=self
        pathList = list()
        while(temp.partner!=None):
            pathList.append(temp)
            temp=temp.partner
        return pathList[::-1]