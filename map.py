from Map.Position import Position

class Map:

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

        return

    # GET methods
    def getGoldPositions(self):
        return self.saved_positions['gold']
    
    def getAuxGoldPositions(self):
        return self.saved_positions['auxGold']
    
    def getVoidPositions(self):  
        return self.saved_positions['void']
    
    def getPowerupPositions(self):
        return self.saved_positions['powerup']
    
    def getBlockedPositions(self):
        return self.saved_positions['blocked']
    
    def getSafePositions(self):      
        return self.saved_positions['safe']
    
    def getUnsafePositions(self):    
        return self.saved_positions['unsafe']
    
    def getNotVisitedPositions(self):
        return self.saved_positions['notvisited']
    
    def getVisitedPositions(self):
        return self.saved_positions['visited']

    # SET methods
    def setNotVisitedPositions(self):
        self.saved_positions['notvisited'] = []
        for i in range(self.width):
            for j in range(self.heigth):
                position = Position.getPosition(i, j)
                self.saved_positions['notvisited'].append(position)
        return self.saved_positions['notvisited']
    
    # Updates the dict with the positions
    def update_map(self, map):
        for i in range(self.width):
            for j in range(self.heigth):
                position = Position.getPosition(i, j)

                if map[i][j] == 'G':
                    self.saved_positions['gold'].append(position)
                    self.saved_positions['visited'].append(position)
                    self.saved_positions['notvisited'].remove(position)
                elif map[i][j] == 'V':
                    self.saved_positions['void'].append(position)
                    self.saved_positions['visited'].append(position)
                    self.saved_positions['notvisited'].remove(position)
                elif map[i][j] == 'P':
                    self.saved_positions['powerup'].append(position)
                    self.saved_positions['visited'].append(position)
                    self.saved_positions['notvisited'].remove(position)
                elif map[i][j] == 'B':
                    self.saved_positions['blocked'].append(position)
                    self.saved_positions['visited'].append(position)
                    self.saved_positions['notvisited'].remove(position)
                elif map[i][j] == 'S':
                    self.saved_positions['safe'].append(position)
                    self.saved_positions['visited'].append(position)
                    self.saved_positions['notvisited'].remove(position)
                elif map[i][j] == 'U':
                    self.saved_positions['unsafe'].append(position)
                    self.saved_positions['visited'].append(position)
                    self.saved_positions['notvisited'].remove(position)
                else:
                    pass
        return

    # Calculates the distance between two points
    def distance_manhattan(self,x1,y1,x2,y2):
        return abs(x1-x2)+abs(y1-y2)
    