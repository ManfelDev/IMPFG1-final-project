''' The goal of this game is to get the highest score you can, the score increases when the player manages to 
catch the corn that is spinning with variable speeds on the screen. The player will have to dodge obstacles while 
trying to catch the corn (hot air balloons with proximity mines that increase along their path and spinning blades) 
for each obstacle the player hits he loses one life, the player starts initially with 3 lives but during the 
a drone will drop lives at random times, which are affected by gravity and level difficulty, the player will have 
to pick up that life if he wants to gain an extra life, if the player loses all lives the game ends. 
The difficulty of the game also increases every time the player collects 10 thousands, which will cause more
obstacles on the screen, with faster spawns, the corn, obstacles, and drones will also have their speed increased. 
While the player is trying to collect the corn and dodge the obstacles, at a random moment, the wind will hinder the 
player's movement, with his resistance, the wind gets longer and longer as the level increases.

Made by: Rafael José - 22202078'''

import pygame, math, random

# Initialize pygame, create a window
pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
screen_center_x = SCREEN_WIDTH / 2
screen_center_y = SCREEN_HEIGHT / 2
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Setting clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Caption
pygame.display.set_caption("Corn Bird")

# Background stuff
bg = pygame.image.load("images/BG.png").convert()
bg_width = bg.get_width()
scroll = 0
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

# Load the lives image
heart_image = pygame.image.load("images/heart.png")


################################ PLAYER ################################
class Player(object):
    def __init__(self):
        self.image = pygame.image.load("images/bird.png")
        self.x = 0
        self.y = 250
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = 5
        self.score = 0 # Initial score
        self.lives = 3 # Initial lives
        self.difficulty = 1 # Initial difficulty
        self.update_collider()
    
    def move_right(self, wind):
        self.x += self.speed - wind.resistance
        
    def move_left(self, wind):
        self.x -= self.speed - wind.resistance
        
    def move_up(self, wind):
        self.y -= self.speed - wind.resistance
        
    def move_down(self, wind):
        self.y += self.speed - wind.resistance
        
    def update_collider(self):
        self.collider = pygame.Rect(self.x, self.y, self.width, self.height)   
        
    def update(self):
        #Checking the boundaries of the screen
        if self.x < self.image.get_width()/2:
            self.x = self.image.get_width()/2
        elif self.x > screen.get_width() - self.image.get_width()/2:
            self.x = screen.get_width() - self.image.get_width()/2
        if self.y < self.image.get_height()/2:
            self.y = self.image.get_height()/2
        elif self.y > screen.get_height() - self.image.get_height()/2:
            self.y = screen.get_height() - self.image.get_height()/2
        self.update_collider()
            
    def draw(self):
        # Draw the player image
        rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, rect)
        
    def draw_lives(self, screen, heart_image):
        x = 955
        y = 35
        for i in range(self.lives):
            screen.blit(heart_image, (x, y))
            x -= 25  # Decrement the x position for the next heart
            
    def reset(self):
        # Reset the player object to its original state
        self.__init__()
        

################################ CORN ################################
class Corn(object):
    def __init__(self):
        self.image = pygame.image.load("images/corn.png")
        self.x = 1000
        self.y = random.randint(50,450)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = random.randint(2,4) + player.difficulty # The speed increases by the difficulty
        self.angle = 0 # Initial angle
        self.spawn_timer = random.randint(1500,3000) # Random time between 1,5 to 3 seconds
        self.update_collider()
    
    def update_collider(self):
        self.collider = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self):
        self.angle += self.speed
        self.x -= self.speed
        self.rotatedScreen = pygame.transform.rotate(self.image, self.angle)
        self.rotatedRect = self.rotatedScreen.get_rect()
        self.rotatedRect.center = (self.x , self.y)
        self.update_collider()
        
    def draw(self):
        screen.blit(self.rotatedScreen, self.rotatedRect)
        

################################ OBSTACLES ################################
# Hot air balloons with proximity mines
class Hot_Ballon(object):
    def __init__(self):
        self.image = pygame.image.load("images/Hot_Ballon.png")
        self.size = random.randint(60, 90) # Random initial size
        self.x = 1100
        self.y = random.randint(0, 440) # Random initial Y
        self.spawn_timer = random.randint(750,1500) / (player.difficulty / 2)
        self.update_collider()
        
    def update(self):
        self.x -= random.randint(1,3) + player.difficulty # The speed increases by the difficulty
        self.size += random.uniform(0.05, 0.2) # Image escalate
        self.update_collider()
        
    def update_collider(self):
        self.collider = pygame.Rect(self.x, self.y, self.size, self.size)
        
    def draw(self):
        screen.blit(pygame.transform.scale(self.image, (self.size, self.size)), (self.x, self.y))
        
# Rotating blade
class Blade(object):
    def __init__(self):
        self.image = pygame.image.load("images/blade.png")
        self.x = 1100
        self.y = random.randint(0, 275) # Random initial Y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.angle = 0 # Initial angle of rotation
        self.radius = 5 # radius of rotation
        self.spawn_timer = random.randint(7500,10000) / (player.difficulty / 4)
        self.update_collider()
        
    def update(self):
        self.x -= random.randint(1,2) + player.difficulty
        self.angle += 0.05 # increase angle of rotation
        self.x += math.cos(self.angle) * self.radius # adjust x-coordinate based on angle of rotation and radius
        self.y += math.sin(self.angle) * self.radius # adjust y-coordinate based on angle of rotation and radius
        self.update_collider()
        
    def update_collider(self):
        self.collider = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, math.degrees(self.angle)) # rotate the image of the blade
        screen.blit(rotated_image, (self.x, self.y))
        

################################ WIND ################################
class Wind:
    def __init__(self):
        self.image = pygame.image.load("images/wind.png")
        self.x = 0
        self.y = 0
        self.resistance = 0
        self.spawn_timer = random.randint(9000, 15000) # random spawn time between 9 and 15 seconds
        self.last_spawn_time = pygame.time.get_ticks() # keep track of the last spawn time
        self.activated = False
        
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_timer:
            self.last_spawn_time = current_time
            self.spawn_timer = random.randint(9000, 15000)
            self.activated = True
            self.start_time = pygame.time.get_ticks()
        if self.activated and pygame.time.get_ticks() - self.start_time < (random.randint(1000,2000) + (player.difficulty * 1000)): # The time of the wind increases by the difficulty
            screen.blit(self.image, (self.x, self.y))
            self.resistance = 2 # Resistance when the wind is up
        else:
            self.activated = False
            self.resistance = 0 # Resistance when the wind is down
        
            
################################ DRONE ################################
class Drone(object):
    def __init__(self):
        self.image = pygame.image.load("images/drone.png")
        self.x = 1100
        self.y = 0
        self.spawn_timer = random.randint(20000, 30000) # random spawn time between 20 and 30 seconds
        self.last_spawn_time = pygame.time.get_ticks() # keep track of the last spawn time
        self.activated = False

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_timer:
            self.last_spawn_time = current_time
            self.spawn_timer = random.randint(20000, 30000)
            self.activated = True
            self.start_time = pygame.time.get_ticks()
            hearts.append(Heart(self.x, self.y)) #create a heart when drone is activated
        if self.activated and self.x > -(self.image.get_width()):
            screen.blit(self.image, (self.x, self.y))
            self.x -= 3 + player.difficulty # The speed increases by the difficulty
        else:
            self.activated = False
            self.x = 1100
            
# Heart dropped by the drone
class Heart(object):
    def __init__(self, drone_x, drone_y):
        self.image = pygame.image.load("images/drone_heart.png")
        self.original_image = self.image
        self.x = drone_x
        self.y = drone_y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.velocity = 0 # initial velocity
        self.gravity = 0.3 * player.difficulty # acceleration due to gravity, times the difficulty
        self.start_time = pygame.time.get_ticks()
        self.angle = 0 # initial angle
        self.rotation_speed = self.gravity * 5 # rotation speed in degrees per second
        self.update_collider()
        self.activated = True

    def update(self, drone_x, drone_y):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time)/1000 # elapsed time in seconds
        self.x = drone_x
        self.y = drone_y
        self.velocity += self.gravity * elapsed_time # update velocity
        self.y += self.velocity * elapsed_time # update y position
        self.angle += self.rotation_speed * elapsed_time # update angle
        self.image = pygame.transform.rotate(self.original_image, self.angle) # rotate
        self.update_collider()
        if self.collider.colliderect(player.collider) and self.activated:
            self.activated = False
            player.lives += 1
        rect = self.image.get_rect()
        rect.center = (self.x, self.y)
        screen.blit(self.image, rect) # blit rotated image to screen
        
    def update_collider(self):
        self.collider = pygame.Rect(self.x, self.y, self.width, self.height)
        
    
################################ GAME SCREENS ################################
while True:
################################ START SCREEN ################################
    # Create font objects
    start_font = pygame.font.Font(None, 50)
    title_font = pygame.font.Font(None, 100)

    # Create text labels for the tile, the start button and the exit button
    title_text = title_font.render("CORN BIRD", True, (240,170,18))
    title_rect = title_text.get_rect()
    title_rect.center = (screen_center_x, screen_center_y - 130)
    start_text = start_font.render("START", True, (255,255,255))
    start_rect = start_text.get_rect()
    start_rect.center = (screen_center_x, screen_center_y)
    exit_text = start_font.render("EXIT", True, (255,255,255))
    exit_rect = exit_text.get_rect()
    exit_rect.center = (screen_center_x, screen_center_y + 50)

    #Setting the start screen
    selected_button = "start"  # Start with the start button selected
    not_start = True

    while not_start:
        # Draw the start and exit buttons on the screen
        screen.blit(bg, (0,0))
        screen.blit(title_text, title_rect)
        if selected_button == "start":
            screen.blit(start_font.render("START", True, (255,165,0)), start_rect)
            screen.blit(exit_text, exit_rect)
        else:
            screen.blit(start_text, start_rect)
            screen.blit(start_font.render("EXIT", True, (255,165,0)), exit_rect)

        # Wait for a keyboard event
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            # Highligh the selected button
            if event.key == pygame.K_UP:
                # Highlight the start button
                selected_button = "start"
            elif event.key == pygame.K_DOWN:
                # Highlight the exit button
                selected_button = "exit"
            
            # Pressed a button
            if selected_button == "start":
                # If start is pressed
                if event.key == pygame.K_RETURN:
                    not_start = False
            elif selected_button == "exit":
                # If Exit is pressed
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    exit()
        
        pygame.display.flip()
    
    # Resets the start screen for when the game loop and the end of the game have finished
    not_start = True

################################ MAIN GAME LOOP ################################
    # Essential variables
    player = Player()
    wind = Wind()
    drone = Drone()
    corns = []
    Hot_Ballon_list = []
    Blade_list = []
    hearts = []
    font = pygame.font.Font(None, 30) # Setting the font

    # Set the initial corn, hot ballon and blade spawn times
    last_corn_spawn_time = pygame.time.get_ticks()
    last_Hot_Ballon_spawn_time = pygame.time.get_ticks()
    last_Blade_spawn_time = pygame.time.get_ticks()
    
    # Setting alive
    alive = True
    
    while alive:
        # Setting the FPS
        clock.tick(FPS)
        # Get the current time
        current_time = pygame.time.get_ticks()
        # Set the score text
        score_text = font.render("Score: " + str(player.score), 1, (255,255,255))
        # Set the level text
        level_text = font.render("Level: " + str(player.difficulty), 1, (255,255,255))
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False

        # Get the keys
        keys = pygame.key.get_pressed()
        # Player movements are affected by the wind resistance
        if keys[pygame.K_LEFT]:
            player.move_left(wind)
        if keys[pygame.K_RIGHT]:
            player.move_right(wind)
        if keys[pygame.K_UP]:
            player.move_up(wind)
        if keys[pygame.K_DOWN]:
            player.move_down(wind)
        
        # Draw scrolling background
        for i in range (0, tiles):
            screen.blit(bg, (i * bg_width + scroll,0))
        scroll -= 1 + player.difficulty
        if abs(scroll) > bg_width:
            scroll = 0
            
        # Update player
        player.update()
        
        # New corn update and draw
        new_corn = Corn()
        if current_time - last_corn_spawn_time > new_corn.spawn_timer and len(corns) < 3:
            corns.append(new_corn)
            last_corn_spawn_time = current_time
        for c in corns:
            c.update()
            if c.x < 0:
                corns.pop(corns.index(c))
            if c.collider.colliderect(player.collider):
                corns.pop(corns.index(c))
                player.score += 1
                if player.score % 10 == 0:
                    player.difficulty += 1
            c.draw()
            
        # New hot ballon update and draw
        new_Hot_Ballon = Hot_Ballon()
        if current_time - last_Hot_Ballon_spawn_time > new_Hot_Ballon.spawn_timer and len(Hot_Ballon_list) < 1 + player.difficulty:
            Hot_Ballon_list.append(new_Hot_Ballon)
            last_Hot_Ballon_spawn_time = current_time
        for o in Hot_Ballon_list:
            o.update()
            if o.x < -(o.image.get_width()):
                Hot_Ballon_list.pop(Hot_Ballon_list.index(o))
            if o.collider.colliderect(player.collider):
                Hot_Ballon_list.pop(Hot_Ballon_list.index(o))
                player.lives -= 1
            o.draw()
            
        # New blade update and draw
        new_Blade = Blade()
        if current_time - last_Blade_spawn_time > new_Blade.spawn_timer and len(Blade_list) < 0 + player.difficulty:
            Blade_list.append(new_Blade)
            last_Blade_spawn_time = current_time
        for b in Blade_list:
            b.update()
            if b.x < -(b.image.get_width()):
                Blade_list.pop(Blade_list.index(b))
            if b.collider.colliderect(player.collider):
                Blade_list.pop(Blade_list.index(b))
                player.lives -= 1
            b.draw()
            
        # Update and draw drone
        drone.update()
        
        # Update and draw hearts
        hearts = [heart for heart in hearts if heart.activated]
        for heart in hearts:
            heart.update(drone.x, drone.y)
        
        # Draw player
        player.draw()
                
        # Update and draw wind
        wind.update()
        
        # Shows the level
        screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 915, 10))
        
        # Shows the score
        screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 25, 10))
        
        # Show the lives
        player.draw_lives(screen, heart_image)
        
        # Check if the player have more lives
        if player.lives == 0:
            alive = False
            
        # Update the display
        pygame.display.flip()
        
################################ GAME OVER SCREEN ################################
    # Set the background
    screen.blit(bg, (0,0))
    
    # Display the game over message
    game_over_font = pygame.font.Font(None, 120)
    score_font = pygame.font.Font(None, 50)
    text = game_over_font.render("GAME OVER", True, (0,0,0))
    text_rect = text.get_rect()
    text_rect.centerx = screen_center_x
    text_rect.centery = screen_center_y - 50
    text_score = score_font.render("SCORE: " + str(player.score), True, (255,255,255))
    text_score_rect = text.get_rect()
    text_score_rect.centerx = 675
    text_score_rect.centery = screen_center_y + 50
    screen.blit(text, text_rect)
    screen.blit(text_score, text_score_rect)
    
    # Update the display
    pygame.display.flip()
    
    # Wait for 2 seconds
    pygame.time.delay(4000)
    
    # RESET THE GAME
    player.reset()
    scroll = 0