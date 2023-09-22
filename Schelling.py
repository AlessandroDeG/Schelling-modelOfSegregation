import pygame
import random
import sys

##STRATEGY
#1. row by row or random sequence of agents
ROW_BY_ROW=False
RANDOM_SEQUENCE=True
#2. if unhappy, find a new place
RANDOM_EMPTY_CELL= False
NEAREST_EMPTY_CELL=False
RANDOM_DIRECTION=True
#3. if happy, do nothing

DELAY = 15
SAVE_SCREENSHOT = False

GRID_SIZE = 100
SCREEN_SIZE=800

EMPTY_PERCENTAGE = 10
RED_PERCENTAGE = 45
BLUE_PERCENTAGE = 45

#EMPTY_PERCENTAGE = 34
#RED_PERCENTAGE = 33
#BLUE_PERCENTAGE = 33

#EMPTY_PERCENTAGE = 98
#RED_PERCENTAGE = 1
#BLUE_PERCENTAGE = 1

N_CELLS=GRID_SIZE*GRID_SIZE

N_EMPTY= N_CELLS*(EMPTY_PERCENTAGE/100)
N_RED= N_CELLS*(RED_PERCENTAGE/100)
N_BLUE= N_CELLS*(BLUE_PERCENTAGE/100)


class Cell:
    happy_cells=0
    H = 4 #number of same color cells to be happy

    allCellsMap={}    #(x,y) ->self

    EMPTY = 0
    RED = 1
    BLUE = 2

    SIZE= SCREEN_SIZE//GRID_SIZE
    
    ADJACENCY_DISTANCE=1  
    
    def __init__(self, posX, posY, type):
        self.type=type
        self.posX=posX
        self.posY=posY
        if(type==Cell.EMPTY):
            self.color = (0,0,0)
        if(type==Cell.RED):
            self.color = (255,0,0)
        if(type==Cell.BLUE):
            self.color = (0,0,255)
        
        Cell.allCellsMap[(self.posX,self.posY)]= self

    def isHappy(self):
        #print("cell: ", (self.posX,self.posY))
        if(self.type==Cell.EMPTY):
            return False
        
        same=0
        for dx in range(-Cell.ADJACENCY_DISTANCE, Cell.ADJACENCY_DISTANCE+1):
            for dy in range(-Cell.ADJACENCY_DISTANCE, Cell.ADJACENCY_DISTANCE+1):
                
                if(dx != 0 or dy!=0):
                    x=self.posX+dx
                    y=self.posY+dy

                    x = (self.posX + dx) % GRID_SIZE
                    y = (self.posY + dy) % GRID_SIZE

                    #print((x,y,dx,dy))
                    
                    if(Cell.allCellsMap[(x,y)].type==self.type):
                        same+=1
        if(same<Cell.H):
            #print("unhappy= ", same)
            return False
        if(same>=Cell.H):
            #print("happy= ", same)
            return True
    
    def findNearestEmptyCell(self):
        
        distance=1
        foundEmptyCell=False
        emptyCells=[]
        while(foundEmptyCell==False):
            for dx in range(-distance, distance+1):
                for dy in range(-distance, distance+1):
                    if dx == 0 and dy == 0: 
                        continue
                    x = (self.posX + dx) % GRID_SIZE
                    y = (self.posY + dy) % GRID_SIZE
                    if abs(dx) + abs(dy) == distance:
                        if(Cell.allCellsMap[(x,y)].type==Cell.EMPTY):
                            emptyCells.append((x,y))
                            foundEmptyCell=True
            distance+=1 
        
        return random.choice(emptyCells)
    
    def findEmptyCellInRandomDirection(self): 
        foundEmptyCell=False
        
        
        """only horizontal or vertical
        vh=random.choice([0,1])
        if(vh==0):
            dx=random.choice([-1,1])
            dy=0
        else:
            dx=0
            dy=random.choice([-1,1])
        """
        d=1
        dx=0
        dy=0
        while(round(d*dx)==0 and round(d*dy)==0):
            dx=random.uniform(-1,1)
            dy=random.uniform(-1,1)
            #print(int(dx),int(dy))

        while(foundEmptyCell==False):
            
            x = (self.posX + round(d*dx)) % GRID_SIZE
            y = (self.posY + round(d*dy)) % GRID_SIZE
            #print(x,y)
            if(Cell.allCellsMap[(x,y)].type==Cell.EMPTY):
                return (x,y)
            d+=1
            if(d>=GRID_SIZE): #try another direction
                #print("no empty cell found")
                #return (self.posX,self.posY)
                return self.findEmptyCellInRandomDirection()
             
###########

pygame.init()

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE), 0)
#WHITE = (255,255,255)

cells_distr = [N_EMPTY, N_RED, N_BLUE]

for x in range(0, GRID_SIZE):
    for y in range(0, GRID_SIZE):
        
        type=random.choices([0,1,2],weights=cells_distr)[0]
        Cell(x,y,type)
        cells_distr[type]-=1
        #print(cells)

n_iterations=0

while(True):
    screen.fill(0)
    
    for key in Cell.allCellsMap.keys():
        cell=Cell.allCellsMap[key]
        pygame.draw.rect(screen,cell.color,(cell.posX*cell.SIZE, cell.posY*Cell.SIZE, Cell.SIZE, Cell.SIZE))

    if(n_iterations==0 and SAVE_SCREENSHOT):
         pygame.image.save(screen, f"H={Cell.H}-RED={RED_PERCENTAGE}%-BLUE={BLUE_PERCENTAGE}%-Iteration{n_iterations}.jpg")
       
    if(Cell.happy_cells < N_RED+N_BLUE):
        Cell.happy_cells=0
        n_iterations+=1
        
        if(ROW_BY_ROW):
            
            indexX= range(0, GRID_SIZE)
            indexY= range(0, GRID_SIZE)
        
        if(RANDOM_SEQUENCE):
            indexX= random.sample(range(0, GRID_SIZE), GRID_SIZE)
            indexY= random.sample(range(0, GRID_SIZE), GRID_SIZE)
            
        for x in indexX:
            for y in indexY:
                cell=Cell.allCellsMap[(x,y)]
                if(not cell.type==Cell.EMPTY):
                    if(not cell.isHappy()):   
                    #find a new place

                        if(RANDOM_EMPTY_CELL):
                            while(True):
                                newX=random.randint(0, GRID_SIZE-1)
                                newY=random.randint(0, GRID_SIZE-1)
                                if(Cell.allCellsMap[newX,newY].type==Cell.EMPTY):
                                    Cell.allCellsMap[newX,newY]=Cell(newX,newY,cell.type)
                                    Cell.allCellsMap[(x,y)]=Cell(x,y,Cell.EMPTY)
                                    break
                        
                        if(NEAREST_EMPTY_CELL):
                            newX,newY=cell.findNearestEmptyCell()
                            Cell.allCellsMap[newX,newY]=Cell(newX,newY,cell.type)
                            Cell.allCellsMap[(x,y)]=Cell(x,y,Cell.EMPTY)

                        if(RANDOM_DIRECTION):
                            newX,newY=cell.findEmptyCellInRandomDirection()
                            Cell.allCellsMap[newX,newY]=Cell(newX,newY,cell.type)
                            Cell.allCellsMap[(x,y)]=Cell(x,y,Cell.EMPTY)
                        
                    #print("cell moved")
                    else:
                        Cell.happy_cells+=1
    elif(SAVE_SCREENSHOT):
        pygame.image.save(screen, f"H={Cell.H}-RED={RED_PERCENTAGE}%-BLUE={BLUE_PERCENTAGE}%-LastIteration{n_iterations}.jpg") 

    #events
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_UP):           
                DELAY-=10                
            if(event.key == pygame.K_DOWN):            
                DELAY+=10
            if(event.key == pygame.K_SPACE):
                 pygame.image.save(screen, f"H={Cell.H}-RED={RED_PERCENTAGE}%-BLUE={BLUE_PERCENTAGE}%-Iteration{n_iterations}.jpg") 

                        
    print(f'Iteration:{n_iterations} , Happy cells:{Cell.happy_cells} , EMPTY:{N_EMPTY} , RED:{N_RED} , BLUE:{N_BLUE}', end='\r')
    pygame.display.update()     
    pygame.time.delay(DELAY)
      
