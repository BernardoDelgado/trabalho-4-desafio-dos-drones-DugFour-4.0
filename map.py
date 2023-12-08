from positions import Position

class Map:

    def __ini__(self):
        self.width = 34
        self.heigth = 59
        self.saved_positions = {
            'gold': [], 
            'void': [], 
            'powerup': [], 
            'blocked': [], 
            'safe': [], 
            'unsafe': [], 
            'notvisited': []
        }

    # Calculates the distance between two points
    def distance_manhattan(self,x1,y1,x2,y2):
        return abs(x1-x2)+abs(y1-y2)

    # GET methods
    def getGoldPositions(self):
        return self.saved_positions['gold']
    
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
    
    # Updates the dict with the positions
    def update_map(self, map):
        for i in range(self.width):
            for j in range(self.heigth):
                if map[i][j] == 'G':
                    self.saved_positions['gold'].append(Position(i, j))
                elif map[i][j] == 'V':
                    self.saved_positions['void'].append(Position(i, j))
                elif map[i][j] == 'P':
                    self.saved_positions['powerup'].append(Position(i, j))
                elif map[i][j] == 'B':
                    self.saved_positions['blocked'].append(Position(i, j))
                elif map[i][j] == 'S':
                    self.saved_positions['safe'].append(Position(i, j))
                elif map[i][j] == 'U':
                    self.saved_positions['unsafe'].append(Position(i, j))
                elif map[i][j] == 'N':
                    self.saved_positions['notvisited'].append(Position(i, j))
                else:
                    pass