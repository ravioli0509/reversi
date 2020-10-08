import time
import random

class Reversi:
    WHITE = "w"
    BLACK = "b"
    EMPTY = "."
    SIZE = 8
    board = []
    showvalid =[]
    move=0
    player = "w"
    computer = "b"
    time = random.randint(1,8)
    white_score = 2
    black_score = 2
    def __init__(self):
      pass

    def newGame(self):
        print("Start a new game of REVERSI!")
        print("Black goes first, then white")
        self.player = input("Enter 'b' to choose to play black, 'w' to choose white: ")
        if self.player == "b":
            self.computer = "w"
        while (self.player != "b" and self.player != "w"):
            self.player = input("Invalid Colour, try again: ")

        for _ in range (0, 8):
            temp = []
            for __ in range (0, 8):
                temp.append('.')
            self.board.append(temp)

        self.board[3][3] = 'w'
        self.board[3][4] = 'b'
        self.board[4][3] = 'b'
        self.board[4][4] = 'w'

    def displayBoard(self):
        print('   0  1  2  3  4  5  6  7')
        for x in range(8):
            print(x,end = '  ')
            for y in range(8):
                print(self.board[x][y], end = '  ')
            print(' ')
        print ({'Black Score':self.black_score, 'White Score':self.white_score})

    def processInput(self):
        self.move = input("Enter your move in two digit form from (00 - 77) or Enter 'q' to Quit: ")
        while (int(self.move) < 00 or int(self.move) > 77):
            self.move = input("Invalid Move, try again: ")
        if self.move.upper() == 'Q':
            print("Thanks for Playing")
            quit()

        x = int(self.move[0])
        y = int(self.move[1])
        self.makeMovePlayer((x,y)) #adds the 1st and 2nd digit form of the input into coordinate. 

    def resetBoard(self):
        self.board = []
        self.newGame()

    def onBoard(self, position): #code done
        if position[0] >= 0 and position[0] < self.SIZE: # x entry check
            if position[1] >= 0 and position[1] < self.SIZE: # y entry check
                return True
        return False

    def whoGoesFirst(self): #decides who goes first
        if self.player == 'w'.upper():
            self.computer == 'b'
        elif self.player == 'b'.upper():
            self.computer == 'w'

    def isPositionValid(self, position, colour): #code done
        if colour=="w":
            opponent="b"
        else:
            opponent="w"
        px = position[0]
        py = position[1]
        if(not self.onBoard((px,py))):
            return []
        if(self.board[px][py] != "." and self.board[px][py]!= "*"):
            return []
        surrounding = []
        for x in range(-1,2):
            for y in range(-1,2):
                if(self.onBoard((px+x, py+y))):
                    if(self.board[px+x][py+y] != colour and self.board[px+x][py+y]!="." and self.board[px+x][py+y]!= "*"):
                        surrounding.append((x,y))

        #surrounding now has list of elements around given position that are of the opposite tile color.
        connectors = []
        for (dx,dy) in surrounding:
            jumpcoord = (px+dx+dx,py+dy+dy) #coordinate after the surrounding tile

            while(self.onBoard(jumpcoord)):
                if (self.board[jumpcoord[0]][jumpcoord[1]] == colour):
                    connectors.append(jumpcoord)
                    break
                elif(self.board[jumpcoord[0]][jumpcoord[1]] == opponent):
                    jumpcoord = (jumpcoord[0]+dx,jumpcoord[1]+dy)

                else:#empty tile "."
                    break
        return connectors

    def ShowValidMoves(self):
        self.showvalid=[] 
        for x in range(self.SIZE): 
            for y in range(self.SIZE):
                 if self.isPositionValid((x,y), self.player) :
                    self.showvalid.append((x,y))
        for element in self.showvalid:
            self.board[element[0]][element[1]] = "*" #replaces . with *

    def updateScore(self):
        self.bscore=0
        self.wscore=0
        for x in range(0, self.SIZE):
            for y in range(0, self.SIZE): 
                if self.board[x][y] == self.BLACK:
                    self.bscore += 1 #updates the bscore
                elif self.board[x][y] == self.WHITE:
                    self.wscore += 1 #updates the wscore
                else:
                    pass
        self.white_score = self.wscore
        self.black_score = self.bscore

    def isGameOver(self):
        for x in range(0, self.SIZE):
            for y in range(0, self.SIZE):
                if self.board[x][y] == ".":  #checks if theres . , returns False. 
                    return False 
                else:
                    return True #its True because every tile shouldn't have a . 

    def makeMovePlayer(self, position):
        result = self.isPositionValid(position, self.player)
        #stores the the position under the the player turns into result
        for tile in result:
            fromtile= tile
            flipping = True
            if(fromtile[0] > position[0]):
                dx=1 #checks infront horizontally
            elif(fromtile[0] < position[0]):
                dx=-1 #checks behind horizontally
            else: dx=0 #everything else fails then its on the same tile
            if(fromtile[1] > position[1]):
                dy=1 #checks above vertically
            elif(fromtile[1] < position[1]):
                dy=-1 #checks down vertically as well
            else: dy=0 #everything else fails then its on the same tile.

            new = (position[0]+dx, position[1] +dy)
            while(flipping): #flipping happens
                self.board[new[0]][new[1]] = self.player
                new = (new[0]+dx, new[1] +dy)
                if(new==fromtile):
                    flipping= False #flipping doesnt happen if its the previous tile.
            self.board[position[0]][position[1]] = self.player
        for x in range(0,self.SIZE):
            for y in range(0,self.SIZE):
                if self.board[x][y] == "*":
                    self.board[x][y] = "."
        self.updateScore()
    
    def makeComputerMove(self):
        for x in range(self.SIZE):
            for y in range(self.SIZE):
                result = self.isPositionValid((x,y), self.computer)
                #stores the position of the computer
                for tile in result:
                    self.board[x][y] =self.computer
                    flipping = True
                    fromtile = tile
                    if(fromtile[0] < x):
                        dx=-1
                    elif(fromtile[0] >x):
                        dx=1
                    else: dx=0
                    if(fromtile[1] < y):
                        dy=-1
                    elif(fromtile[1] > y):
                        dy=1
                    else: dy=0
                    new = (x+dx, y+dy)
                    while(flipping):
                        time.sleep(self.time)
                        self.board[new[0]][new[1]] = self.computer
                        new = (new[0]+dx, new[1] +dy)
                        if(new==fromtile):
                            flipping= False
                            return
            self.updateScore()

def main():
    game = Reversi()
    game.newGame()
    while(not game.isGameOver()):
        game.ShowValidMoves()
        game.displayBoard()
        game.processInput()
        game.displayBoard()
        game.makeComputerMove()

main()
