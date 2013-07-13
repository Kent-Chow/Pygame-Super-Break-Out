"""
Author: Kent Chow
Date: May 2, 2012
Description: This file contains the main function for Super Break-Out.
Enhancements: Bricks moves down when player destroys one brick.
              Bricks are worth individual points based on colour.
              Paddle width is cut when half of bricks are destroyed.
"""

# I - IMPORT AND INITIALIZE
import pygame, sprites
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((640, 480))

def main():
    """This function defines the 'mainline logic' for the Break-Out game."""
    
    # DISPLAY
    pygame.display.set_caption("Super Break-Out!")
    
    # ENTITIES
    background = pygame.image.load("background.gif")
    background = background.convert() 
    screen.blit(background, (0, 0)) 
    
    # Load all sound files and set volume
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    lazer = pygame.mixer.Sound("lazer.wav")
    lazer.set_volume(0.2)
    death = pygame.mixer.Sound("death.ogg")
    death.set_volume(0.8)
    shrink = pygame.mixer.Sound("shrink.wav")
    shrink.set_volume(1.0)
    game_over = pygame.mixer.Sound("game_over.wav")
    game_over.set_volume(1.0)
    win_sound = pygame.mixer.Sound("win.wav")
    game_over.set_volume(1.0)
    
    #Win, Lose Labels
    font = pygame.font.Font("digital.ttf", 45)
    win_label = font.render("YOU   WIN!", 1, (0, 0, 0))
    game_over_label = font.render("GAME OVER!", 1, (0, 0, 0))
    
    # Sprites for: Player, Ball, and Bricks and StatsKeeper 
    # colours, points used to store brick info.
    colours = ["violet.gif","red.gif","yellow.gif","orange.gif","green.gif", \
               "blue.gif"]
    points = [6, 5, 4, 3, 2, 1]     
    bricks = [[], [], [], [], [], []]
    y = 30
    
    # Instantiate brick sprite for each row
    for row in range(6):
        y += 22
        x = 21
        for column in range(18):
            brick = sprites.Brick(screen, x, y, points[row], colours[row])
            x += 35
            bricks[row].append(brick)
               
    # Instantiate ball, player, end zone and stats keeper       
    ball = sprites.Ball(screen)                   
    player = sprites.Player(screen)
    end_zone = sprites.EndZone(screen)
    stats_keeper = sprites.StatsKeeper(3)
    
    # Group all sprites
    brick_group = pygame.sprite.Group(bricks)
    allSprites = pygame.sprite.Group(player, brick_group, ball, stats_keeper, \
                                     end_zone)
    
    # ASSIGN  
    clock = pygame.time.Clock() 
    keepGoing = True
      
    # Hide the mouse pointer 
    pygame.mouse.set_visible(False) 
  
    # LOOP 
    while keepGoing: 
      
        # TIME 
        clock.tick(30) 
      
        # EVENT HANDLING: Player arrow keys 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                keepGoing = False
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT: 
                    player.change_direction((1, 0)) 
                if event.key == pygame.K_RIGHT: 
                    player.change_direction((-1, 0)) 
  
        # Check if ball hits brick
        if pygame.sprite.spritecollide(ball, brick_group, False): 
            ball.change_direction()   
            lazer.play()
            #Adds value of each brick to score keeper and remove brick          
            for sprite in pygame.sprite.spritecollide(ball, brick_group, True):
                stats_keeper.scored(sprite.get_points())
                #Check if bricks are less than half
                if not player.get_size() and len(brick_group) < 55:
                    player.change_size(player.rect.centerx)
                    shrink.play()
                #Check if player has won
                #Plays sound, and display label if True
                elif len(brick_group) == 0:
                    screen.blit(win_label,(320, 240))
                    pygame.display.flip()  
                    pygame.time.delay(1500)
                    win_sound.play()
                    pygame.time.delay(4800)
                    keepGoing = False
                #Move rest of bricks down
                for sprite in (brick_group):
                    sprite.move_down()
        
        #Checks if ball hits paddle           
        if ball.rect.colliderect(player):
            ball.change_direction()
         
        #Checks if ball hits end zone
        if ball.rect.colliderect(end_zone):     
            death.play()
            ball.change_direction()
            stats_keeper.lose_life()
            #Checks if all lives are gone
            #Plays sound, and display label if True
            if stats_keeper.get_life() == 0:              
                screen.blit(game_over_label,(225, 240))
                pygame.display.flip()
                pygame.time.delay(1500)
                game_over.play()
                pygame.time.delay(1500)
                keepGoing = False
                        
        # REFRESH SCREEN 
        allSprites.clear(screen, background) 
        allSprites.update() 
        allSprites.draw(screen)        
        pygame.display.flip() 
          
    # Unhide the mouse pointer 
    pygame.mouse.set_visible(True) 
  
    # Close the game window 
    pygame.quit()      
      
# Call the main function 
main()