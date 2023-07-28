import pygame
from pygame.locals import K_SPACE, K_u, K_r
from typing import List

l = 20
ws = 600
wsl = (int)(ws/l)
window_size = (ws,ws)

running = True

pygame.init()
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Game of Life | Paused")

class cell:
    x = 0
    y = 0
    rect = [0,0,0,0]
    state = False
    next_state = False
    name = ""
    
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.rect = [x*l,y*l,l,l]
        self.name = f"({x}, {y})"
    
    def get_name(self) -> str:
        return self.name
    
    def get_x(self) -> int:
        return self.x
    
    def get_y(self) -> int:
        return self.y
    
    def get_state(self) -> bool:
        return self.state
    
    def get_next_state(self) -> bool:
        return self.next_state
    
    def set_next_state(self, state: bool) -> None:
        self.next_state = state
        
    def set_state(self, state: bool) -> None:
        self.state = state
        
    def change_state(self) -> None:
        self.state = not self.state
    
    def draw(self) -> None:
        pygame.draw.rect(window, (255,255,255), self.rect, 1-self.state)
        
    def update_state(self) -> None:
        self.state = self.next_state
        
    def reset(self):
        self.state = False
        self.next_state = False
        

cells:List[cell] = []

def initalize() -> None:
    for w in range(wsl):
        cells.append([])
        for h in range(wsl):
            cells[w].append(cell(w,h))
    draw_cells()
            
def draw_cells() -> None:
    window.fill((0,0,0))
    for w in range(wsl):
        for h in range(wsl):
            cells[w][h].draw()
    pygame.display.update()

def check_neighbors(c: cell) -> int:
    n_active = 0
    wo = -1
    ho = -1
    if c.get_x() == 0:
        wo = 0
    if c.get_y() == 0:
        ho = 0

    for w in range(wo,2):
        for h  in range(ho,2):
            try:
                neighbor = cells[c.get_x()+w][c.get_y()+h]
                if c!=neighbor and neighbor.get_state():
                    n_active += 1
            except:
                continue
    return n_active

def advance():
    for w in range(wsl):
        for h in range(wsl):
            c = cells[w][h]
            n = check_neighbors(c)
            if (c.get_state() == False) and (n==3):
                c.set_next_state(True)
            if (c.get_state() == True) and (1<n<4):
                c.set_next_state(True)
            elif (c.get_state() == True) and (n < 2 or n > 3):
                c.set_next_state(False)
    for w in range(wsl):
        for h in range(wsl):
            cells[w][h].update_state()
    draw_cells()

def reset():
    for w in range(wsl):
        for h in range(wsl):
            cells[w][h].reset()
    draw_cells()

if __name__ == "__main__":
    
    initalize()
    play = False
    
    while running:
        if play == True:
            advance()
            pygame.time.delay(50)
            
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos()
                i = (int)(m_pos[0]/l)
                j = (int)(m_pos[1]/l)
                clicked = cells[i][j]
                if pygame.mouse.get_pressed() == (True, False, False):
                    clicked.change_state()
                    draw_cells()
                elif pygame.mouse.get_pressed() == (False, False, True):
                    print(f"Cell: {clicked.get_name()}\nState:{clicked.get_state()}\nFuture state:{clicked.get_next_state()} \nActive neighbors: {check_neighbors(clicked)}\n")
            
            elif event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    advance()
                    print("Space")
                elif event.key == K_r:
                    reset()
                elif event.key == K_u:
                    play = not play
                    if play:
                        pygame.display.set_caption("Game of Life | Playing")
                    else:
                        pygame.display.set_caption("Game of Life | Paused")
                    
            elif event.type == pygame.QUIT:
                running = 0