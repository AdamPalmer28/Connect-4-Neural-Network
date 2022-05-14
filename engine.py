"""
Connect 4 game engine

handles the game logic
"""
import numpy as np

class gamestate():
    
    
    def __init__(self):
        
        self.board = np.zeros((6,7))
        
        self.move_count = 0
        
        
    def make_move(self,col):
        # checks move is legal
        assert col in list(range(7)), "Col must be 0 to 6"
        
        selected = self.board[:,col]
        
        col_empty = np.where(gs.board[:,col] == 0)[0]
        
        if len(col_empty) == 0:
            # early exit
            print("Move not possible")
            return
        else:
            min_index = min(col_empty)
            self.update_gs(min_index,col)
        

    def update_gs(self,row,col):
        # move updates
        counter = (1 if self.move_count % 2 == 0 else -1)
        self.board[row,col] = counter
        
        self.move_count += 1
        
        print(self.board[::-1,])
        
    def win(self):
        "Checks the current board to see if a player has won"
        pass
        
if __name__ == '__main__':
    # for back testing
    gs = gamestate()