# Minesweeper

# import libraries
import random
from tkinter import *
from tkinter import messagebox
import random

# create classes

### FINISHED ###
class Square(Label):
    '''Square object--> repr. a square in Minesweeper'''

    def __init__(self, master, pos):
        '''creates a square with 'pos' position
        pos --> tuple'''
        Label.__init__(self,master,height = 1, width = 2, text = '',\
                       bg = 'grey', font=('Monospace',20), relief = RAISED,fg = 'yellow')
        self.grid(column = pos[0], row = pos[1])
        #all squares start out unexposed
        self.num = 0
        self.exposed = False
        self.colormap = ['white','blue','darkgreen','red','purple','maroon','cyan','black','dim gray']
        self.blank = self.num == 0
        self.bomb = False
        self.flagged = False    #not flagged in beginning
        self.pos = pos
        self.disabled = False
        self.bind('<Button-1>', self.expose)
        self.bind('<Button-2>', self.toggle_flag)
        self.bind('<Button-3>', self.toggle_flag)
        
    def toggle_flag(self,n):
        '''toggles the flag on self'''
        if self.master.get_flags() == 0 and not self.flagged or self.exposed or self.disabled:
            return # if no more flags and trying to add one don't do anything
        self.flagged = not self.flagged
        if self.flagged:
            self['text'] = '*'
            self.master.flags.set(self.master.flags.get() - 1)
        else:
            self['text'] = ''
            self.master.flags.set(self.master.flags.get() + 1)

    def reveal(self):
        '''reveals if a bomb - turns red if not flagged, green if flagged
        automatically freezes'''
        if self.bomb:
            if self.flagged:
                bg = 'green'
            else:
                bg = 'red'
            self['bg'] = bg
        self.disabled = True
        
    def expose(self,n):
        '''exposes the square; if bomb ends the game'''
        if self.flagged or self.exposed or self.disabled:
            return # lock if self.flagged or already exposed
        elif self.bomb:
            # if a bomb
            self.master.lose_game()    #end game if bomb
        else:    # no problems
            self['text'] = self.num
            self['bg'] = 'white'
            self['relief'] = 'sunken'
            self['fg'] = self.colormap[self.num]
            self.exposed = True
            if self.num == 0:
                self.master.auto_expose(self.pos)  #auto expose all squares around blanks
            self.master.update()
            self.master.check_win()
        
    def set_bomb(self,value = False):
        '''sets bomb'''
        self.bomb = value

    def is_bomb(self):
        '''returns Ture if self is bomb'''
        return self.bomb

    def get_num(self):
        '''returns num'''
        return self.num

    def set_num(self,val):
        '''sets num to val'''
        self.num = val

    def get_pos(self):
        '''returns pos'''
        return self.pos
    
    def is_exposed(self):
        '''return true if self is exposed'''
        return self.exposed
        
    def is_flagged(self):
        '''returns if flagged'''
        return self.flagged


class Field(Frame):
    '''field class'''

    def __init__(self,master, width, height, numBombs):
        '''Field(master,width,height,numBombs) --> Tkinter Frame
        width, height --> dimensions of minesweeper field
        numBombs --> number bombs in field; random'''
        Frame.__init__(self, master)
        self.grid()
        self.dims = (width,height)
        self.fieldGrid = []  #the grid
        self.numBombs = numBombs
        #create grid of width x height
        for x in range(width):
            column = []
            for y in range(height):
                column.append(Square(self,(x,y))) #give pos -- set num later after choosing bombs

            self.fieldGrid.append(column)
                
        # select bombs
        n = 0
        while n < numBombs:
            randSquare = random.choice(random.choice(self.fieldGrid))
            if not randSquare.is_bomb():
                randSquare.set_bomb(True)
                n += 1
        #add numbers
        self.create_numbers()
        self.flags = IntVar()
        self.flags.set(numBombs)
        self.counter = Label(master, textvariable = self.flags, bg = 'white')
        self.counter.grid(column = 0, row = height,columnspan = width)
        self.restartButton = Button(master, text = 'Restart', command = self.restart)
        self.restartButton.grid(column = 0, row = height+1, columnspan = width)
        self.widgets = [self.counter,self.restartButton]
        
    def lose_game(self):
        '''end the game with a loss'''
        messagebox.showerror('Minesweeper', 'KABOOM! You stepped on a mine and got destroyed.', parent = self)
        for row in self.fieldGrid:
            for cell in row:
                cell.reveal()
        self.counter.grid_remove()
        self.restartButton['text'] = 'Retry'
        
    def restart(self):
        for w in self.widgets:
            w.grid_remove()
        self.grid_remove()
        newgame = Field(self.master,self.dims[0],self.dims[1],self.numBombs)
        newgame.mainloop()
        
    def win_game(self):
        '''end game with a win'''
        messagebox.showinfo('Minesweeper', 'Good Job! You found out all the mines!', parent = self)
        for row in self.fieldGrid:
            for cell in row:
                cell.reveal()
        self.counter.grid_remove()
        self.restartButton['text'] = 'Play Again'
        self.mainloop()

    def auto_expose(self, pos):
        '''exposes all cells around pos'''
        # since the fieldGrid list is set up in columns (e.g. [ [(0,0),(0,1),(0,2)...],[...],... [...] ]
        # the first index is the 'x' and the second is the 'y'
        # the coordinates start at top right
        
        (cellx,celly) = pos
        #find all cells around
        for (changex,changey) in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]:
            (currentx,currenty) = (cellx + changex,celly+changey)
            if currentx in [x for x in range(len(self.fieldGrid))]: #if the first index is in range
                if currenty in [y for y in range(len(self.fieldGrid[currentx]))]: # if the second 'y' index is in range
                    surroundCell = self.fieldGrid[currentx][currenty]  #get the surrounding cell
                    if not surroundCell.is_bomb():  #if the cell isn't a bomb we don't want to expose it
                        #normally this is not needed since cells around a bomb will be filled, but... just in case
                        surroundCell.expose(None) # None since expose is a event handler for left click, and they need one parameter

    def get_flags(self):
        '''returns num flags left'''
        return self.flags.get()

    def create_numbers(self):
        '''creates the numbers around bombs'''
        for row in self.fieldGrid:
            for cell in row:
                if cell.is_bomb():
                    continue    # if bomb do nothing
                (cellx,celly) = cell.get_pos()
                num = 0    #num bombs around the cell
                #find all cells around
                for (changex,changey) in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]:
                    (currentx,currenty) = (cellx + changex,celly+changey)
                    if currentx in [x for x in range(len(self.fieldGrid))]: #if the first index is in range
                        if currenty in [y for y in range(len(self.fieldGrid[currentx]))]: # if the second 'y' index is in range
                            surroundCell = self.fieldGrid[currentx][currenty]  #get the surrounding cell
                            if surroundCell.is_bomb():
                                num += 1    #if a surrounding cell is a bomb, add to num
                cell.set_num(num)
                
    def check_win(self):
        '''checks if all cells except for bombs are exposed- if so, call win_game'''
        for row in self.fieldGrid:
            for cell in row:
                if cell.is_bomb():
                    continue    # if bomb do nothing
                if not cell.is_exposed():    # if the cell isn't exposed and not bomb return
                    return
        self.win_game()

def minesweeper(numMines,l=8):
    root = Tk()
    root.title('Minesweeper')
    root.resizable(0,0)
    g = Field(root, l,l , numMines)
    g.mainloop()
    
