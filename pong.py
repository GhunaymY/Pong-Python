# Working Pong

import pygame


# User-defined functions

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((500, 400))
    # set the title of the display window
    pygame.display.set_caption('Pong')   
    # get the display surface
    w_surface = pygame.display.get_surface() 
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play() 
    # quit pygame and clean up the pygame window
    pygame.quit() 


# User-defined classes

class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('black')

        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        # === game specific objects
        self.small_ball = Ball('white', 5, [250, 200], [2, 4], self.surface)
        self.paddle = Paddle(60,150,10,50,'white',self.surface)
        self.paddle_2 = Paddle(430,150,10,50,'white',self.surface)
        self.frame_counter = 0
        self.score = 0
        self.score_2 = 0
            

    def play(self):
        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()            
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 
    
    def draw_score(self):
        string = str(self.score)
        string_2 = str(self.score_2)
        font_size = 70
        fg_color = pygame.Color('white')
        bg_color = pygame.Color('black')
        #font_name = 'Times New Roman'
        # Step 1 Create a font object
        font = pygame.font.SysFont('',font_size)
        # Step 2 render the font object
        text_box = font.render(string,True,fg_color,bg_color)
        text_box_2 = font.render(string_2,True,fg_color,bg_color)
        # Step 3 determine the location of the text_box
        location = (0,0) 
        location_2 = (472,0)
        # Step 4 blit or pin the text_box on the surface
        self.surface.blit(text_box,location)  
        self.surface.blit(text_box_2,location_2)
        
            
        

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True  
            elif event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            elif event.type == pygame.KEYUP:
                self.handle_key_up(event)
    
    def handle_key_down(self,event):
        if event.key == pygame.K_a:
            self.paddle.set_velocity(10)
        elif event.key == pygame.K_q:
            self.paddle.set_velocity(-10)
        if event.key == pygame.K_l:
            self.paddle_2.set_velocity(10)
        elif event.key == pygame.K_p:
            self.paddle_2.set_velocity(-10)        
    def handle_key_up(self,event):
        if event.key == pygame.K_a:
            self.paddle.set_velocity(0)
        elif event.key == pygame.K_q:
            self.paddle.set_velocity(0)
        if event.key == pygame.K_l:
            self.paddle_2.set_velocity(0)
        elif event.key == pygame.K_p:
            self.paddle_2.set_velocity(0)        

    def draw(self):
        self.surface.fill(self.bg_color) # clear the display surface first
        self.small_ball.draw()
        self.draw_score()
        self.paddle.draw()
        self.paddle_2.draw()
        pygame.display.update() # make the updated surface appear on the display

    def update(self):
        collision = self.small_ball.move(self.paddle.rect,self.paddle_2.rect)
        if collision == 1:
            self.score_2 = self.score_2 + 1
        if collision == 2:
            self.score = self.score + 1        
        
        self.frame_counter = self.frame_counter + 1
        self.paddle.move()
        self.paddle_2.move()

    def decide_continue(self):
        if self.score >= 11 or self.score_2 >= 11:
            self.continue_game = False

class Paddle:
    # An object in this class represents a Paddle that moves

    def __init__(self,x,y,width,height,color,surface):
        self.rect = pygame.Rect(x,y,width,height)
        self.color = pygame.Color(color)
        self.surface = surface
        self.v_velocity = 0
        self.state = 'stopped'
    def draw(self):
        pygame.draw.rect(self.surface,self.color,self.rect)
    def set_velocity(self,v_velocity):
        self.v_velocity = v_velocity
    def move(self): 
        self.rect.move_ip(0,self.v_velocity)
        if self.rect.bottom >= self.surface.get_height():
            self.rect.bottom = self.surface.get_height()
        if self.rect.top < 0 :
            self.rect.top = 0 
        
      
        
  
        
        
        
class Ball:
    def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, surface):
        self.color = pygame.Color(ball_color)
        self.radius = ball_radius
        self.center = ball_center
        self.velocity = ball_velocity
        self.surface = surface
    def move(self,paddle,paddle_2):
        size = self.surface.get_size()
        collision = 0 
        for i in range(0,2):
            self.center[i] = (self.center[i] + self.velocity[i])
            if self.center[i] <= self.radius: 
                self.velocity[i] = -self.velocity[i] 
                if i == 0:
                    collision = 1
            if self.center[i] + self.radius >= size[i]:
                self.velocity[i] = -self.velocity[i]# bounce from the edge  
                if i == 0:
                    collision = 2
            if paddle.collidepoint(self.center) and self.velocity[0] < 0 :
                self.velocity[0] = -self.velocity[0]
            if paddle_2.collidepoint(self.center) and self.velocity[0] > 0:
                self.velocity[0] = -self.velocity[0]
        return collision
    def draw(self):
        pygame.draw.circle(self.surface, self.color, self.center, self.radius)
main()