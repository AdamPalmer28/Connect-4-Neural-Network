"""
Connect 4 game engine

handles the game logic
"""
import numpy as np

class gamestate():
    
    
    def __init__(self):
        
        self.dimensions = (6,7)
        self.board = np.zeros(self.dimensions)
        
        self.move_count = 0
        self.game_over = False
        
    def make_move(self,col):
        # checks move is legal
        assert col in list(range(7)), "Col must be 0 to 6"
        
        selected = self.board[:,col]
        
        col_empty = np.where(self.board[:,col] == 0)[0]
        
        if len(col_empty) == 0:
            # early exit
            print("Move not possible")
            return False
        else:
            min_index = min(col_empty)
            self.update_gs(min_index,col)
            return True

    def update_gs(self,row,col):
        # move updates
        counter = (1 if self.move_count % 2 == 0 else -1)
        self.board[row,col] = counter

        if self.win(counter):
            #print("win")
            self.game_over = True
            self.winner = ('Red' if counter == 1 else 'Yellow')
        else:
            #print('No win')
            self.move_count += 1
        
        
        
    def win(self,player):
        "Checks the current board to see if the player has won"
    
        # horizontal win
        for row in range(self.dimensions[0]):
            count = 0 # reset count
            for col in range(self.dimensions[1]):
                
                if count + self.dimensions[1] - col < 4: 
                    # win not possible
                    break
                
                # counter
                if self.board[row,col] == player:
                    count += 1
                else:
                    count = 0
                    
                if count >= 4: # win
                    return True
                    
        # vertical win
        for col in range(self.dimensions[1]):
            count = 0 # reset count
            for row in range(self.dimensions[0]):
            
                if count + self.dimensions[0] - row < 4: 
                    # win not possible
                    break
                
                # counter
                if self.board[row,col] == player:
                    count += 1
                else:
                    count = 0
                    
                if count >= 4: # win
                    return True
                
                
        # == diagonal win (Right to left) ==
        
        # list of all starting index for diagonal search
        aval_r_start = self.dimensions[0] - (4 - 1) 
        aval_c_start = self.dimensions[1] - (4 - 1)
        aval_start = []
        for r in range(aval_r_start):
            aval_start.append((r,0))
        for c in range(aval_c_start):
            aval_start.append((0,c))
        
        for start in aval_start:
            count = 0 
            pos_square = min(self.dimensions[0]-start[0] , self.dimensions[1]-start[1])
            for i in range(pos_square):
                if count + pos_square - i < 4: 
                    # win not possible
                    break
                
                # counter
                if self.board[ start[0]+i , start[1]+i ] == player:
                    count += 1
                else:
                    count = 0
                    
                if count >= 4: # win
                    return True
        
        
        # == diagonal win 2 (Left to Right) == 
        
        # list of all starting index for diagonal search
        aval_r_start = self.dimensions[0] - (4 - 1)
        aval_c_start = self.dimensions[1] - (4 - 1)
        aval_start = []
        for r in range(aval_r_start):
            aval_start.append(((self.dimensions[0]-1)-r,0))
        for c in range(aval_c_start):
            aval_start.append((self.dimensions[0]-1,c))
            
        for start in aval_start:
            count = 0 
            pos_square = min(start[0] + 1, self.dimensions[1]-start[1])
            
            for i in range(pos_square):
                if count + pos_square - i < 4: 
                    # win not possible
                    break
                
                # counter
                if self.board[ start[0]-i , start[1]+i ] == player:
                    count += 1
                else:
                    count = 0
                    
                if count >= 4: # win
                    return True
        
        
        return False
        
if __name__ == '__main__':
    # for back testing
    gs = gamestate()
    
    ref = np.ndarray(gs.board.shape,dtype=object) 
    for r in range(ref.shape[0]):
        for c in range(ref.shape[1]):
            ref[r,c] = (r,c)
            