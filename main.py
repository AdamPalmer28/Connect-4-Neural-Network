"""
Game main - GUI to make the game "pretty"

"""

import pygame as p
import sys
import numpy as np

#game engine
from engine import gamestate

#width = height = 768
top_rib = 128
dimension = (7,6) # dimensions of board
sq_size = 128
height = dimension[1]*sq_size + top_rib
width = dimension[0]*sq_size

max_fps = 8

def main():
    """
    Handles user input and and GUI display of the game engine (connect 4)
    """
    
    p.init()
    
    screen = p.display.set_mode((width,height))
    clock = p.time.Clock()
    screen.fill(p.Color("#0C0A6C"))
    
    # intialise gamestate
    gs = gamestate()
    # draw board
    draw_board_states(screen,gs)
    
    running = True
    while running:
        "game events"
        for e in p.event.get(): 
            
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
                running = False
        
            elif e.type == p.MOUSEBUTTONDOWN:# click on screen
            
                loc_x, loc_y = p.mouse.get_pos() # (x, y) location of mouse
                
                if loc_y < top_rib:
                    # Clicked ribben area
                    
                    if (loc_y >= 10) and (loc_y <= top_rib/2):
                        # undo button  (width -110, 10, width-10 , top_rib/2 ) 
                        if (loc_x >= width -110) and (loc_x <= width-10):
                            print('Undo')
                            pass
                        # new game (width -235, 10, width - 100, top_rib/2 )
                        elif (loc_x >= width -235) and (loc_x <= width-100):
                            main()
                            
                            
                elif not gs.game_over:
                    col_input = loc_x // sq_size
                    
                    if not gs.make_move(col_input):
                        # move not possible
                        pass
                    else:
                        # update gamestate
                        draw_board_states(screen,gs)
                        
                        if gs.game_over:
                            
                            draw_win(screen,gs.winner)
                            #running = False
                
                
                
        clock.tick(max_fps)
        p.display.update()
                
                
#%% Ribben
p.font.init()

ribben_font = p.font.SysFont('Poppins', 72)
move_font = p.font.SysFont('Poppins', 48)

button_font = p.font.SysFont('Poppins',36)

def draw_ribben(screen,gs):
    """
    Ribben information and UI features
    """
    
    p.draw.rect(screen,'#393939',p.Rect(0,0,width,top_rib)) # background
    p.draw.rect(screen,'#A3A3A3',p.Rect(0.32 * width,0,2/5 * width ,top_rib)) # status bg
    p.draw.rect(screen,'Black',p.Rect(0.32 * width,0,2/5 * width ,top_rib),2) # statusboarder
    p.draw.rect(screen,'Black',p.Rect(0,0,width,top_rib),4) # boarder
    
    
    
    # next turn 
    turn_text = ribben_font.render('Turn:', False, (255, 255, 255))
    text_rect = turn_text.get_rect(center=(200/2, top_rib/2))
    screen.blit(turn_text,text_rect)
    # draw circle of move
    p.draw.circle(screen, 'Black', (220,top_rib/2), int(0.6*(top_rib/2)+5),5)
    colour = 'red' if gs.move_count % 2 == 0 else 'yellow'
    p.draw.circle(screen, p.Color(colour), (220,top_rib/2), int(0.6*(top_rib/2)))
    
    
    # move tracker 
    move_text = move_font.render(f'Move:  {gs.move_count+1}', True, (255, 255, 255))
    text_rect = move_text.get_rect(center=(width - 140, 3*top_rib/4))
    screen.blit(move_text,text_rect)
    
    draw_buttons(screen)

button_colour = '#888888'
def draw_buttons(screen):  
    # undo button  (width -110, 10, width-10 , top_rib/2 ) (x1, y1, x2, y2)
    undo_size = 80
    p.draw.rect(screen,button_colour,p.Rect(width- undo_size-10, 10 ,undo_size, top_rib/2 -10))
    p.draw.rect(screen,'Black',p.Rect(width- undo_size-10, 10 ,undo_size, top_rib/2 -10),2) 
    
    undo_text = button_font.render('Undo', True, (255, 255, 255))
    text_rect = undo_text.get_rect(center=(width - undo_size/2 -10, top_rib/4 + 5))
    screen.blit(undo_text,text_rect)
    
    # new game (width -235, 10, width - 100, top_rib/2 )
    newg_size = 135
    p.draw.rect(screen,button_colour,p.Rect(width-90- newg_size-10, 10 ,newg_size, top_rib/2 -10))
    p.draw.rect(screen,'Black',p.Rect(width-90- newg_size-10, 10 ,newg_size, top_rib/2 -10),2) 
    
    undo_text = button_font.render('New game', True, (255, 255, 255))
    text_rect = undo_text.get_rect(center=(width -90- newg_size/2 -10, top_rib/4 + 5))
    screen.blit(undo_text,text_rect)
    
#%% Board
def draw_board_states(screen,gs):
    """
    Draws the board and counters based on the current game state
    """
    draw_board(screen)
    draw_counters(screen,gs)
    draw_ribben(screen,gs)
    

def draw_board(screen):
    """Draws the board"""
    
    for w in range(dimension[0]):
        for h in range(dimension[1]):
            position = ( (w + 0.5) * sq_size, (h + 0.5)* sq_size + top_rib)
            p.draw.circle(screen, p.Color('#A3A3A3'), position, int(0.8*sq_size/2))
            p.draw.circle(screen, p.Color('#393939'), position, int(0.8*sq_size/2)+2,4)
    #pass

def draw_counters(screen,gs):
    """Draws the peices of the current game state""" 
    p1 = np.where(gs.board==1)
    red_counters = zip(p1[0],p1[1])
    
    p2 = np.where(gs.board==-1)
    yellow_counters = zip(p2[0],p2[1])
    
    for (r,c) in red_counters:
        x = sq_size*(c + 1/2)
        y = height - sq_size*(r + 1/2) 
        p.draw.circle(screen, p.Color('red'), (x,y), int(0.8*sq_size/2))
        
    for (r,c) in yellow_counters:
        x = sq_size*(c + 1/2)
        y = height - sq_size*(r + 1/2) 
        p.draw.circle(screen, p.Color('yellow'), (x,y), int(0.8*sq_size/2))

#%% End game UI


game_over_font = p.font.SysFont('Arial', 72)  

# def draw_win(screen,winner):
#     p.draw.rect(screen,'Black', p.Rect(192/2,(height-top_rib)/2,width-192, 256)) # outter retangle
#     p.draw.rect(screen,"White", p.Rect(192/2 + 8,(height-top_rib)/2 +8 ,width-192-16, 256 -16)) # inner retangle
    
#     end_text = end_screen_font.render(winner.title() + ' wins!', True, (0, 0, 0))
#     screen.blit(end_text,(192/2 + 32,(height-top_rib)/2 + 100))

def draw_win(screen,winner):
    win_text = game_over_font.render(f'{winner.title()} wins!', False, (255, 255, 255))
    text_rect = win_text.get_rect(center=(0.52 * width, top_rib/2))
    screen.blit(win_text,text_rect)
    
    
#%% __main__

if __name__=='__main__':
    
    main()