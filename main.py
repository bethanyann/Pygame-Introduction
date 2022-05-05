import pygame
from sys import exit
from random import randint

#Functions
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'score: {current_time}', False,(64,64,64))
    score_rectangle = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rectangle)
    print(current_time)

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
                obstacle_rect.x -= 5 #every obstacle will be moved to the left a little bit on each game loop

                if obstacle_rect.bottom == 300: 
                    screen.blit(snail_surface, obstacle_rect)
                else:
                    screen.blit(fly_surface, obstacle_rect)
                
        #check to see if any snails are too far to the left and only add them to the list if their x attribute (left position) is greater than zero (off the screen)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -30 ] 

        return obstacle_list #return the list to make this not just local but also global back to the main obstacle list
    else: return [] #at the start of the game, return an empty list so that the obstacle_rect_list is not null      

#loop through all of the obstacles and see if the player is colliding with any of them
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles: 
                if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    global player_surface, player_index

    #display jumping image when player is not on floor
    if player_rectangle.bottom < 300 :
        player_surf = player_jump

    #display walking animation if player is on the floor
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surface = player_walk[int(player_index)]


pygame.init() 

#create display surface (the game window) where the game will be & set it to a variable for access
width = 800
height = 400
screen = pygame.display.set_mode((width,height))  #pass a tuple of width and height to the screen
pygame.display.set_caption('Runner Test')

#create a clock object to help with time and also to set the framerate
clock = pygame.time.Clock()

#creating text: a bit complicated with a few steps
#1. create a font (text size and style)
test_font = pygame.font.Font('font/Pixeltype.ttf', 50) #font type, font size
#2. write text on a surface
#3. blit the text surface
game_active = True
start_time = 0
#plain color test game surface - different than the display surface that is the game window
#test_surface = pygame.Surface((100,200))
#test_surface.fill('coral4')

sky_surface = pygame.image.load('graphics/Sky.png').convert() #convert changes the .png into a more python-friendly image format
ground_surface = pygame.image.load('graphics/ground.png').convert()
#text_surface = test_font.render('My Game', False, 'Black') #text, color, antialiasing

#score_surface = test_font.render('My Game', False, 'Black') 
#score_rectangle = score_surface.get_rect(center = (400, 50))

player_index = 0
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surface = player_walk[player_index]
#create a rectangle that is the same size as the surface - this gets the surface and then draws a rect around it
player_rectangle = player_surface.get_rect(midbottom = (80,300)) #define specfic place for the rect - grabs midbottom point of rect and places it where the ground begins @ 300
player_gravity = 0

#Obstacles
snail_frame_index = 0
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha() #convert alpha maintains the background transparency of a .png
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha() #convert alpha maintains the background transparency of a .png
snail_frames = [snail_frame_1, snail_frame_2]
snail_surface = snail_frames[snail_frame_index]


fly_frame_index = 0
fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []



#Intro Screen
player_standing = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_standing = pygame.transform.rotozoom(player_standing, 0, 2)
player_standing_rectangle = player_standing.get_rect(center = (400,200))

game_name = test_font.render('Pixel Runner', False, (111,196,169))
game_name_rectangle = game_name.get_rect(center = (400, 85))

game_message = test_font.render('Press spacebar to run', False, (111,196,169))
game_message_rectangle = game_message.get_rect(center = (400, 320))


#Timers
obstacle_timer = pygame.USEREVENT + 1 #weird but add a +1 to the end of every event to keep them unique?
pygame.time.set_timer(obstacle_timer, 1500) #timer event to set, milliseconds

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

#this while loop is to keep the game running instead of flashing on the screen for one minute
while True:
    #this is called the game's event loop
    for event in pygame.event.get(): #this gets all of the events of player input 
        if event.type == pygame.QUIT:
            pygame.quit() #this is the opposite of .init()
            exit() #this will stop the code execution and close the loop
        
        if game_active:
            #can check for any key pressed here in the event loop
            if event.type == pygame.KEYUP: 
                print('key up')

            if event.type == pygame.KEYDOWN:
                #check for specfic key
                if event.key == pygame.K_SPACE: 
                    #only allow the player to jump if it's already touching the floor
                    if player_rectangle.bottom == 300:
                        player_gravity = -20
                        print('spacebar pressed')

            if event.type == obstacle_timer:
                if randint(0,2): #simple random number thats either 0 (true) or false (1)
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900,1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(900,1100), 210)))   

            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0  
                snail_surface = snail_frames[snail_frame_index]
                
            if event.type == fly_animation_timer: 
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                #snail_rectangle.left = 800
                start_time = int(pygame.time.get_ticks() / 1000)

       


       


#GAME LOOP
    #draw all game elements here and update everything only if the game is currently active
    if game_active:
        #attach game surface to display surface 
        screen.blit(sky_surface, (0,0)) #blit = block image transfer, put one surface on the other surface
        screen.blit(ground_surface,(0, 300))
        #pygame.draw.rect(screen, 'pink', score_rectangle) #display surface, color, actaual rectangle to draw
        #screen.blit(score_surface, score_rectangle)
        display_score()

        #Player
        player_gravity += 1
        player_rectangle.y += player_gravity
        #player_rectangle.left += 1 #you don't move the surface, you move the rectangle that contains the surface in pygame
        if player_rectangle.bottom >= 300:player_rectangle.bottom = 300 # everytime the player hits the top of the ground at 300, we get the bottom of the player and set it on top of the ground
        player_animation()     
        screen.blit(player_surface, player_rectangle) #take the player surface and put it in the position of the rectangle

        #Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #Collisions
        game_active = collisions(player_rectangle, obstacle_rect_list)

        #every time the game loop runs it will decrement the snail's position and make it move to the left 
        #snail_x_position -= 2
        #if(snail_x_position < -20): snail_x_position = 810
        #if snail_rectangle.right <= 0: snail_rectangle.left = 800
        #snail_rectangle.left -= 2
        #screen.blit(snail_surface, snail_rectangle)

        #check for collisions between rectangles 
        #if player_rectangle.colliderect(snail_rectangle): #this returns a bool with either a 0 or 1 value
        #    print('collision')

        #the other way to get the player's keyboard interaction outside of the event loop
        #keys = pygame.key.get_pressed() #this returns an object with all of the keys in it and their current "state" (pressed or not)
        #if keys[pygame.K_SPACE]:  #checks to see if the spacebar is being pressed (key names are in pygame documentation)
        #    print('Jump')

        #collision between player and snail
        #if snail_rectangle.colliderect(player_rectangle): 
        #    game_active = False

    else: 
        screen.fill((94,129,162))
        screen.blit(player_standing, player_standing_rectangle)
        #empty out obstacle list after game ends to prevent collisons from happening right after restarting the game
        obstacle_rect_list.clear()
        screen.blit(game_name, game_name_rectangle)
        screen.blit(game_message, game_message_rectangle)
    pygame.display.update() #updateds the screen display surface
    clock.tick(60) #setting the framerate ceiling to 60fps to prevent the game from running too fast 