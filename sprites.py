"""
Author: Kent Chow
Date: May 2, 2012
Description: This file contains classes used for Break-Out.
"""
import pygame

class Brick(pygame.sprite.Sprite):
    """This class defines the sprite for the bricks."""
    def __init__(self, screen, x, y, points, image):
        """This initializer takes a screen surface as a parameter, the x, y 
        coordinates of the brick, and the colour of the brick. It then 
        initializes the image and rect attributes accordingly."""
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Set the image and rect attributes for the Ball
        self.__x = x
        self.__y = y
        self.image = pygame.image.load(image)
        self.image = self.image.convert() 
        self.rect = self.image.get_rect() 
        self.rect.center = (self.__x, self.__y)
        self.__points = points
    
    def get_points(self):
        """This method takes no parameters. Returns value of points."""
        return self.__points
    
    def move_down(self):
        """This method takes no parameters. Moves brick down 2 pixels."""
        self.__y += 2
        self.rect.center = (self.__x, self.__y)
        
class Player(pygame.sprite.Sprite):   
    """This class defines the sprite for the player."""
    def __init__(self, screen):
        """This initializer takes a screen surface and loads the image for the
        player. It sets the position on the bottom and middle of the screen."""
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Define the image attributes for the player.
        self.image = pygame.image.load("large_paddle.gif")
        self.image = self.image.convert() 
        self.rect = self.image.get_rect() 
        self.rect.center = (screen.get_width()/2,screen.get_height() - 20)
        
        # Instance variables to keep track of the screen surface
        # and set the initial x and y vector for the ball.
        self.__screen = screen
        self.__dx = 0
        
        # Variable to keep track if paddle is small
        self.__small = False
        
    def change_size(self, x):
        """This method takes the x coordinate of the paddle as a parameter. It
        loads the small paddle and set it to the original x coordinate."""
        self.image = pygame.image.load("small_paddle.gif")
        self.image = self.image.convert() 
        self.rect = self.image.get_rect()
        self.rect.center = (x ,self.__screen.get_height() - 10)
        self.__small = True
        
    def get_size(self):
        """This method take no parameters. Returns True if paddle is short."""
        return self.__small
                       
    def change_direction(self, xy_change):
        """This method takes a (x,y) tuple as a parameter, extracts the 
        x element from it, and uses this to set the players x direction."""
        self.__dx = xy_change[0]
                       
    def update(self):
        """This method will be called automatically to reposition the
        player sprite on the screen."""
        # Check if we have reached the most right or left of the screen.
        # If not, then keep moving the player in the same x direction.
        if ((self.rect.left > 0) and (self.__dx > 0)) or\
           ((self.rect.right < self.__screen.get_width()) and (self.__dx < 0)):
            self.rect.left -= (self.__dx * 10)
        
class Ball(pygame.sprite.Sprite):
    """This class defines the sprite for our Ball."""
    def __init__(self, screen):
        """This initializer takes a screen surface as a parameter, initializes
        the image and rect attributes, and x,y direction of the ball."""
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Set the image and rect attributes for the Ball
        self.image = pygame.image.load("ball.gif")
        self.image.set_colorkey((255,255,255)) 
        self.rect = self.image.get_rect() 
        self.rect.center = (screen.get_width()/2,screen.get_height()/2) 
 
        # Instance variables to keep track of the screen surface
        # and set the initial x and y vector for the ball.
        self.__screen = screen
        self.__dx = -5
        self.__dy = 10
 
    def change_direction(self):
        """This method causes the y direction of the ball to reverse."""
        self.__dy = -self.__dy
                    
    def update(self):
        """This method will be called automatically to reposition the
        ball sprite on the screen."""
        # Check if we have reached the left or right end of the screen.
        # If not, then keep moving the ball in the same x direction.
        if ((self.rect.left > 0) and (self.__dx < 0)) or \
           ((self.rect.right < self.__screen.get_width()) and (self.__dx > 0)):
            self.rect.left += self.__dx
        # If yes, then reverse the x direction. 
        else:
            self.__dx = -self.__dx
             
        # Check if we have reached the top or bottom of the court.
        # If not, then keep moving the ball in the same y direction.
        if ((self.rect.top > 0) and (self.__dy > 0)) or \
           ((self.rect.bottom  < self.__screen.get_height()) and \
            (self.__dy < 0)):
            self.rect.top -= self.__dy
        # If yes, then reverse the y direction. 
        else:
            self.__dy = -self.__dy
            
class StatsKeeper(pygame.sprite.Sprite): 
    """This class defines a StatsKeeper sprite to display the score and
    amount of lives."""
    def __init__(self, player_life): 
        """This initializer loads the custom font "digital, and 
        sets the starting score to 0 and life to the number inputted."""
        # Call the parent __init__() method 
        pygame.sprite.Sprite.__init__(self) 
  
        # Load our custom font, and initialize the starting score. 
        self.__font = pygame.font.Font("digital.ttf", 45)
        self.__score = 0
        self.__player_life = player_life
        
    def scored(self, amount): 
        """This method adds one to the score"""
        self.__score += amount
        
    def lose_life(self):
        """This method subtracts one to the amount of lives"""
        self.__player_life -= 1
        
    def get_life(self):
        """This method returns the amount of lives"""
        return self.__player_life
         
    def update(self): 
        """This method will be called automatically to display  
        the current score and lives at the top of the game window."""
        message = "Score: " + str(self.__score) + " " * 10 + "Life: " + \
                str(self.__player_life)
        self.image = self.__font.render(message, 1, (0, 0, 0)) 
        self.rect = self.image.get_rect() 
        self.rect.center = (320, 20)

class EndZone(pygame.sprite.Sprite):
    """This class defines the sprite for our bottom zone."""
    def __init__(self, screen):
        """This initializer takes a screen surface."""
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Our endzone sprite will be a 1 pixel tall white line.
        self.image = pygame.Surface((screen.get_width(), 1))
        self.image = self.image.convert()
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
         
        # Set the rect attributes for the endzone
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/2, screen.get_height() - 1)    