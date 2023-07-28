import pygame

from pygame.locals import K_SPACE

width = 20
height = 20
margin = 5
ws = 100
window_size=(ws,ws)
m_pos = [0,0]

running = True

cells = []

pygame.init()
window = pygame.display.set_mode(window_size)

class cell:
    x_index = 0
    y_index = 0
    rectinfo = [0,0,0,0]
    state = False
    name = ""
    next_state = False
    
    def __init__(self,x,y) -> None:
        self.x_index = x
        self.y_index = y
        self.rectinfo = [x*width,y*height,width,height]
        self.name = f"{x}, {y}"

    def get_name(self) -> str:
        return self.name
    
    def get_x(self) -> int:
        return self.x_index
    
    def get_y(self) -> int:
        return self.y_index
    
    def draw(self) -> None:
        pygame.draw.rect(window, (255,255,255), self.rectinfo, 1-self.state)

    def change_state(self) -> None:
        self.state = not self.state
        
    def get_state(self) -> None:
        return self.state
    
    def get_future_state(self):
        return self.next_state
    
    def set_future_state(self, s: bool) -> None:
        self.next_state = s
    
    def update_state(self) -> None:
        self.state = self.next_state

def draw_cells() -> None:
    window.fill((0,0,0))
    for w in range((int)(ws/width)):
        for h in range((int)(ws/height)):
            cells[w][h].draw()
    pygame.display.update()
    
def initalize() -> None:
    for w in range((int)(ws/width)):
        cells.append([])
        for h in range((int)(ws/height)):
            cells[w].append(cell(w,h))
    draw_cells()
    
def check_neighbors(c: cell) -> int:
    #print(f"cell: {c.get_name()}")
    active_neighbors = 0
    try:
        for w in range(-1,2):
            for h in range(-1,2):
                if w == 4:
                    pass
                neighbor = cells[c.get_x()+w][c.get_y()+h]
                if neighbor.get_state()==True:
                    #print(f"{neighbor.get_name()}: {neighbor.get_state()}")
                    active_neighbors += 1
    except:
        pass
    return active_neighbors

def advance():
    for w in range((int)(ws/width)):
        for h in range((int)(ws/height)):
            c = cells[w][h]
            n = check_neighbors(c)
            if(w == 0 and h == 0):
                pass
            if (c.get_state() == True) and (n < 2 or n>3):
                c.set_future_state(False)
            if (c.get_state() == True) and (2 < n < 4):
                c.set_future_state(True)
            if (c.get_state() == False) and (n == 3):
                c.set_future_state(True)    
            
    for w in range((int)(ws/width)):
        for h in range((int)(ws/height)):
            cells[w][h].update_state()
            
    draw_cells()
            
if __name__ == "__main__":
    initalize()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos()
                clicked = cells[(int)(m_pos[0]/width)][(int)(m_pos[1]/height)]
                if pygame.mouse.get_pressed() == (True, False, False):
                    clicked.change_state()
                    draw_cells()
                elif pygame.mouse.get_pressed() == (False, False, True):
                    print(f"Cell: {clicked.get_name()}\nState:{clicked.get_state()}\nFuture state:{clicked.get_future_state()} \nActive neighbors: {check_neighbors(clicked)}\n")
                
            elif event.type == pygame.KEYDOWN:
                advance()
        
            elif event.type == pygame.QUIT:
                running = 0