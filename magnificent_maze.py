#-------------------------------------------------------------------------------
# Name: magnificent_maze.py
# Purpose:  a maze game, where the player has to find a trophy while shooting
#           enemies to avoid being killed with a surprise level at the end

# Created:     13/01/2017
# Copyright:   K. Santos
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

def main():
    pass

if __name__ == '__main__':
    main()

#import libraries
import pygame
import math
import random

#define colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

#initialize pygame
pygame.init()

#if the player is near a hidden first aid kit show this clue
clue = pygame.image.load("mark.png")

# ---- Classes ---- #

#builds the walls
class Wall(pygame.sprite.Sprite):
    """This class represents the bar at the bottom that the player controls """

    def __init__(self, x, y, width, height, color):
        """ Constructor function """

        # Call the parent's constructor
        super(Wall, self).__init__()

        # Make a wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#enemy sprites
class Enemy(pygame.sprite.Sprite):

    def __init__(self, filename):
        # Call the parent class (Sprite) constructor
        super(Enemy, self).__init__()

        # image loaded from the disk
        self.image = pygame.image.load(filename).convert()

        # Set background color
        self.image.set_colorkey(BLACK)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

        # Instance variables that control the edges of where we bounce
        self.left_boundary = 0
        self.right_boundary = 0
        self.top_boundary = 0
        self.bottom_boundary = 0

        # Instance variables for our current speed and direction
        self.change_x = 0
        self.change_y = 0

    def update(self):
        """ Called each frame. """
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.right >= self.right_boundary or self.rect.left <= self.left_boundary:
            self.change_x *= -1

        if self.rect.bottom >= self.bottom_boundary or self.rect.top <= self.top_boundary:
            self.change_y *= -1

#final level, enemy sprite
class Dragon(pygame.sprite.Sprite):

    def __init__(self, filename):
        super(Dragon, self).__init__()

        #
        # image loaded from the disk.
        self.image = pygame.image.load(filename).convert()

        # Set background color
        self.image.set_colorkey(BLACK)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

        # Instance variables that control the edges of where we bounce
        self.left_boundary = 0
        self.right_boundary = 0
        self.top_boundary = 0
        self.bottom_boundary = 0

        # Instance variables for our current speed and direction
        self.change_x = 0
        self.change_y = 0

        #health for each dragon
        self.hp = 100

    def update(self):
        """ Called each frame. """
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.right >= self.right_boundary or self.rect.left <= self.left_boundary:
            self.change_x *= -1

        if self.rect.bottom >= self.bottom_boundary or self.rect.top <= self.top_boundary:
            self.change_y *= -1

#trophy sprites (player needs to collect this to go to the final round)
class Trophy(pygame.sprite.Sprite):

    def __init__(self, filename):
        # Call the parent class (Sprite) constructor
        super(Trophy, self).__init__()

        # image loaded from the disk.
        self.image = pygame.image.load(filename).convert()

        # Set background color
        self.image.set_colorkey(BLACK)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

        # Instance variables that control the edges of where we bounce
        self.left_boundary = 0
        self.right_boundary = 0
        self.top_boundary = 0
        self.bottom_boundary = 0

        # Instance variables for our current speed and direction
        self.change_x = 0
        self.change_y = 0

    def update(self):
        """ Called each frame. """
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.right >= self.right_boundary or self.rect.left <= self.left_boundary:
            self.change_x *= -1

        if self.rect.bottom >= self.bottom_boundary or self.rect.top <= self.top_boundary:
            self.change_y *= -1

#first aid kit sprite
class Aid(pygame.sprite.Sprite):

    def __init__(self, filename):
        # Call the parent class (Sprite) constructor
        super(Aid, self).__init__()

        # image loaded from the disk.
        self.image = pygame.image.load(filename).convert()

        # Set background color
        self.image.set_colorkey(BLACK)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

#decoration sprites
class Tree(pygame.sprite.Sprite):

    def __init__(self, filename):
        # Call the parent class (Sprite) constructor
        super(Tree, self).__init__()

        # image loaded from the disk.
        self.image = pygame.image.load(filename).convert()

        # Set background color
        self.image.set_colorkey(BLACK)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

#player sprite
class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the
    player controls """

    # Set speed vector
    change_x = 0
    change_y = 0

    def __init__(self, filename, x ,y):
        # Call the parent class (Sprite) constructor
        super(Player, self).__init__()

        # image loaded from the disk
        self.image = pygame.image.load(filename).convert()

        # Set background color
        self.image.set_colorkey(BLACK)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def changespeed(self, x, y):
        """ Change the speed of the player. Called with a keypress. """
        self.change_x += x
        self.change_y += y

    def move(self, walls):
        """ Find a new position for the player """

        # Move left/right
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

#bullet sprite
class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Bullet,self).__init__()

        self.image = pygame.Surface([4, 10])
        self.image.fill(PURPLE)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.y -= 3

#rooms
class Room(object):
    """ Base class for all rooms. """

    # Each room has a list of walls, and sprites.
    wall_list = None
    enemy_sprites = None
    trophy_sprites = None
    dragon_sprites = None
    health_sprites = None
    decoration_sprites = None

    def __init__(self):
        """ Constructor, create our lists. """
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.trophy_sprites = pygame.sprite.Group()
        self.dragon_sprites = pygame.sprite.Group()
        self.health_sprites = pygame.sprite.Group()
        self.decoration_sprites = pygame.sprite.Group()

class Room0(Room):
    """This creates all the walls in room 0"""
    def __init__(self):
        super(Room0, self).__init__()
        # Make the walls. (x_pos, y_pos, width, height)

        # This is a list of walls. Each is in the form [x, y, width, height]
        walls = [[0, 200, 200, 600, GREEN],
                 [400, 200, 600, 600, GREEN],[0,50,600,25,GREEN],
                ]

        # Loop through the list. Create the wall, add it to the list
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        #first aid kit
        wellness = Aid("health.gif")
        wellness.rect.x = 15
        wellness.rect.y = 150
        self.health_sprites.add(wellness)

        #trees
        grass = Tree("pine.png")
        grass.rect.x = 20
        grass.rect.y = 150
        self.decoration_sprites.add(grass)
        grass = Tree("pine.png")
        grass.rect.x = 450
        grass.rect.y = 150
        self.decoration_sprites.add(grass)
        grass = Tree("pine.png")
        grass.rect.x = 450
        grass.rect.y = 380
        self.decoration_sprites.add(grass)
        grass = Tree("pine.png")
        grass.rect.x = 20
        grass.rect.y = 380
        self.decoration_sprites.add(grass)



class Room1(Room):
    """This creates all the walls in room 1"""
    def __init__(self):
        super(Room1, self).__init__()

        walls = [[400,50,600,200,GREEN],[400,400,600,600,GREEN],
                 [0,50,400,25,GREEN],[0,625,600,650,GREEN],[0,50,25,650,GREEN]]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        # Create Enemies
        # This represents the enemies
        for i in range(10):
            enemy = Enemy("skull.png")

            # Set a random location for the enemy
            enemy.rect.x = random.randrange(50,350)
            enemy.rect.y = random.randrange(30,450)

            enemy.change_x = random.randrange(-3, 5)
            enemy.change_y = random.randrange(-3, 5)
            enemy.left_boundary = 35
            enemy.top_boundary = 125
            enemy.right_boundary = 370
            enemy.bottom_boundary = 600

            # Add the enemy to the list of objects
            self.enemy_sprites.add(enemy)

        #first aid kit
        wellness = Aid("health.gif")
        wellness.rect.x = 150
        wellness.rect.y = 450
        self.health_sprites.add(wellness)

        #trees
        grass = Tree("pine.png")
        grass.rect.x = 450
        grass.rect.y = 400
        self.decoration_sprites.add(grass)

class Room2(Room):
    """This creates all the walls in room 2"""
    def __init__(self):
        super(Room2, self).__init__()

        walls = [[0,0,200,200,GREEN],[400,0,600,650,GREEN],[0,400,600, 650,GREEN]]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        # Create Enemies
        # This represents the enemies
        for i in range(8):
            enemy = Enemy("skull.png")

            # Set a random location for the enemy
            enemy.rect.x = random.randrange(200,360)
            enemy.rect.y = random.randrange(150,400)

            enemy.change_x = random.randrange(-3, 5)
            enemy.change_y = random.randrange(-3, 5)
            enemy.left_boundary = 205
            enemy.top_boundary = 15
            enemy.right_boundary = 400
            enemy.bottom_boundary = 400

            # Add the enemy to the list of objects
            self.enemy_sprites.add(enemy)

        #first aid kit
        wellness = Aid("health.gif")
        wellness.rect.x = 250
        wellness.rect.y = 313
        self.health_sprites.add(wellness)

        #trees
        for x in range (0, 600, 80):
            grass = Tree("pine.png")
            grass.rect.x = 0 + x
            grass.rect.y = 400
            self.decoration_sprites.add(grass)

class Room3(Room):
    """This creates all the walls in room 3"""
    def __init__(self):
        super(Room3, self).__init__()

        walls = [[0,50,200,650,GREEN], [400,50,600,650,GREEN]]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        # Create Enemies
        # This represents the enemies
        for i in range(10):
            enemy = Enemy("skull.png")

            # Set a random location for the enemy
            enemy.rect.x = random.randrange(210, 390)
            enemy.rect.y = 250

            enemy.change_x = random.randrange(-3, 5)
            enemy.change_y = random.randrange(-3, 5)
            enemy.left_boundary = 190
            enemy.top_boundary = 190
            enemy.right_boundary = 390
            enemy.bottom_boundary = 500

            # Add the enemy to the list of objects
            self.enemy_sprites.add(enemy)

        #first aid kit
        wellness = Aid("health.gif")
        wellness.rect.x = 350
        wellness.rect.y = 300
        self.health_sprites.add(wellness)

        #trees
        for y in range (0, 600, 200):
            grass = Tree("pine.png")
            grass.rect.x = 25
            grass.rect.y = 400 - y
            self.decoration_sprites.add(grass)

        for y in range (0, 600, 200):
            grass = Tree("pine.png")
            grass.rect.x = 455
            grass.rect.y = 400 - y
            self.decoration_sprites.add(grass)

class Room4(Room):
    """This creates all the walls in room 4"""
    def __init__(self):
        super(Room4, self).__init__()

        walls = [[0,50,200,200,GREEN], [0,400,200,650,GREEN], [400,50,600,200,GREEN],
                [400,400,600,650,GREEN],[200,50,400,25,GREEN]]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        # Create Enemies
        # This represents the enemies
        enemy = Enemy("skull.png")
        # Set a random location for the enemy
        enemy.rect.x = 250
        enemy.rect.y = 105
        enemy.change_x = 7
        enemy.left_boundary = 200
        enemy.top_boundary = 125
        enemy.right_boundary = 400
        enemy.bottom_boundary = 600
        # Add the enemy to the list of objects
        self.enemy_sprites.add(enemy)

        #first aid kit
        wellness = Aid("health.gif")
        wellness.rect.x = 250
        wellness.rect.y = 90
        self.health_sprites.add(wellness)

        #trees
        grass = Tree("pine.png")
        grass.rect.x = 25
        grass.rect.y = 400
        self.decoration_sprites.add(grass)
        grass = Tree("pine.png")
        grass.rect.x = 500
        grass.rect.y = 400
        self.decoration_sprites.add(grass)

class Room5(Room):
    """This creates all the walls in room 5"""
    def __init__(self):
        super(Room5, self).__init__()

        walls = [[0,50,600,200,GREEN], [0,400,600,650,GREEN]]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        #first aid kit
        wellness = Aid("health.gif")
        wellness.rect.x = 360
        wellness.rect.y = 300
        self.health_sprites.add(wellness)

        #trees
        for x in range (0, 600, 80):
            grass = Tree("pine.png")
            grass.rect.x = 0 + x
            grass.rect.y = 400
            self.decoration_sprites.add(grass)

        #trees
        for x in range (0, 600, 80):
            grass = Tree("pine.png")
            grass.rect.x = 0 + x
            grass.rect.y = 0
            self.decoration_sprites.add(grass)

class Room6(Room):
    """This creates all the walls in room 6"""
    def __init__(self):
        super(Room6, self).__init__()

        walls = [[0,50,600,200,GREEN],[400,400,600,650,GREEN],[0,400,200,650,GREEN] ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        #first aid kit
        wellness = Aid("health.gif")
        wellness.rect.x = 230
        wellness.rect.y = 300
        self.health_sprites.add(wellness)

        #trees
        for x in range (0, 600, 80):
            grass = Tree("pine.png")
            grass.rect.x = 0 + x
            grass.rect.y = 0
            self.decoration_sprites.add(grass)

class Room7(Room):
    """This creates all the walls in room 7"""
    def __init__(self):
        super(Room7, self).__init__()

        walls = [[0,50,600,200,GREEN],[0,50,25,650,GREEN],[25,625,600,650,GREEN],[575,400,600,650,GREEN]]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        # Create Enemies
        # This represents the enemies
        for i in range(15):
            enemy = Enemy("skull.png")

            # Set a random location for the enemy
            enemy.rect.x = random.randrange(50,600)
            enemy.rect.y = random.randrange(400,600)

            enemy.change_x = random.randrange(-3, 5)
            enemy.change_y = random.randrange(-3, 5)

            enemy.left_boundary = 50
            enemy.top_boundary = 400
            enemy.right_boundary = 600
            enemy.bottom_boundary = 600

            # Add the block to the list of objects
            self.enemy_sprites.add(enemy)

        #first aid kit
        wellness = Aid("health.gif")
        wellness.rect.x = 150
        wellness.rect.y = 500
        self.health_sprites.add(wellness)

        #trees
        for x in range (0, 600, 80):
            grass = Tree("pine.png")
            grass.rect.x = 0 + x
            grass.rect.y = 0
            self.decoration_sprites.add(grass)

class Room8(Room):
    """This creates all the walls in room 8"""
    def __init__(self):
        super(Room8, self).__init__()

        walls = [[0,50,200,25,GREEN],[400,50,600,25,GREEN],[0,50,25,650,GREEN],[575,50,600,650,GREEN],
                    [25,625,575,650,GREEN]]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        # Create Enemies
        # This represents the enemies
        for i in range(25):
            enemy = Enemy("skull.png")

            # Set a random location for the enemy
            enemy.rect.x = random.randrange(50,550)
            enemy.rect.y = random.randrange(50,550)

            enemy.change_x = random.randrange(-3, 8)
            enemy.change_y = random.randrange(-3, 8)

            enemy.left_boundary = 50
            enemy.top_boundary = 50
            enemy.right_boundary = 600
            enemy.bottom_boundary = 600

            # Add the enemy to the list of objects
            self.enemy_sprites.add(enemy)

        #first aid kit
        wellness = Aid("health.gif")
        wellness.rect.x = 350
        wellness.rect.y = 300
        self.health_sprites.add(wellness)

        #trophy
        trophy = Trophy("win.png")
        trophy.rect.x = random.randrange(50,550)
        trophy.rect.y = 510
        trophy.change_x = 0
        trophy.change_y = 0

        # Add the block to the list of objects
        self.trophy_sprites.add(trophy)

class Room9(Room):
    #FINAL ROUND
    """This creates all the walls in room 9"""
    def __init__(self):
        super(Room9, self).__init__()

        walls = [[0,45,600,15,GREEN],[0,45,15,650,GREEN],[0,635,600,15,GREEN],[585,45,15,650,GREEN]]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        #dragon sprites
        for i in range(3):
            dragon = Dragon("kill.png")
            # Set a random location for the dragon
            dragon.rect.x = 60
            dragon.rect.y = 75
            dragon.change_x = random.randrange(-8,10)
            dragon.left_boundary = 50
            dragon.right_boundary = 600
            # Add the dragons to the list of objects
            self.dragon_sprites.add(dragon)

        #fire sprites, same use as enemy sprites
        for i in range(35):
            fire = Enemy("hot.png")
            # Set a random location for the fire
            fire.rect.x = random.randrange(50,550)
            fire.rect.y = random.randrange(50,550)
            fire.change_x = random.randrange(3,5)
            fire.change_y = random.randrange(3,5)
            fire.left_boundary = 50
            fire.top_boundary = 50
            fire.right_boundary = 600
            fire.bottom_boundary = 650
            # Add the fires to the list of objects
            self.enemy_sprites.add(fire)


def main():
    """ Main Program """

    # Call this function so the Pygame library can initialize itself
    pygame.init()

    # Create screen
    screen = pygame.display.set_mode([600, 650])

    # Set the title of the window
    pygame.display.set_caption('Magnificent Maze')

    done = False

    clock = pygame.time.Clock()

    # -- START of INSTRUCION SCREEN -- #

    #this is a font we use to draw text on the screen (size 36)
    font = pygame.font.Font(None, 36)

    #initialize variables
    display_instructions = True
    instruction_page = 1
    header_x = 225
    header_y = 525

    # --- Instruction Page Loop ---
    while not done and display_instructions:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                px, py = pygame.mouse.get_pos()
                #where the user clicks
                distance = abs(math.sqrt((px - header_x)**2 + (py - header_y)**2))
                #if user clicks play
                if distance < 100:
                    instruction_page += 1
                    if instruction_page == 2:
                            display_instructions = False

            #set the screen background
            screen.fill(BLACK)
            if instruction_page == 1:

                header = pygame.image.load("title.jpg")
                screen.blit(header,(0,0))

                #PLAY button
                font = pygame.font.SysFont('Consolas', 45, True, False)
                text = font.render("PLAY", True, WHITE)
                screen.blit(text, [225,525])

        #limit to 60 frames per second
        clock.tick(60)

        #update the screen with what we've drawn
        pygame.display.flip()

    # -- End of Instruction Screen -- #

    # --- Sprite lists

    # List of each bullet
    bullet_list = pygame.sprite.Group()

    #moving sprite
    movingsprites = pygame.sprite.Group()

    # Create the player paddle object
    player = Player("wizard.jpg", 200, 550)
    movingsprites.add(player)

    #initialize player score, health, lives
    score = 0
    lives = 3
    health = 100

    #empty list for each room
    rooms = []

    #append each room to the rooms list
    room = Room0()
    rooms.append(room)

    room = Room1()
    rooms.append(room)

    room = Room2()
    rooms.append(room)

    room = Room3()
    rooms.append(room)

    room = Room4()
    rooms.append(room)

    room = Room5()
    rooms.append(room)

    room = Room6()
    rooms.append(room)

    room = Room7()
    rooms.append(room)

    room = Room8()
    rooms.append(room)

    room = Room9()
    rooms.append(room)

    #start player in room 0
    current_room_no = 0

    #determines player's current room
    current_room = rooms[current_room_no]

    done = False

    clock = pygame.time.Clock()

    #play background music
    pygame.mixer.music.load('epic.mp3')
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)

    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.25)


    #booleans to determine conditions if player wins, loses, is near a first aid kit etc.
    health_visible = False
    game_over = False
    trap = False
    player_win = False

    # -- Main Program Loop -- #

    while not done:

        # --- Event Processing ---

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONUP:
                px, py = pygame.mouse.get_pos()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(5, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, -5)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, 5)
                if event.key == pygame.K_SPACE:
                # Fire a bullet if the user presses the space bar
                    bullet = Bullet()
                    #play sound effect if user shoots
                    #effect = pygame.mixer.Sound('shoot.mp3')
                    #effect.set_volume(0.9)
                    #effect.play()
                    # Set the bullet so it is where the player is
                    bullet.rect.x += player.rect.x
                    bullet.rect.y += player.rect.y
                    # Add the bullet to the lists
                    bullet_list.add(bullet)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(5, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, 5)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, -5)

        # --- Game Logic ---

        #based on the player's position, the current room is determined
        player.move(current_room.wall_list)

        #if player moves to the left of the screen to switch rooms
        if player.rect.x < -5:
            #room 0 -> room 1
            if current_room_no == 0:
                current_room_no = 1
                current_room = rooms[current_room_no]
                player.rect.x = 590
                player.rect.y = 313

            #room 2 -> room 0
            elif current_room_no == 2:
                current_room_no = 0
                current_room = rooms[current_room_no]
                player.rect.x = 590
                player.rect.y = 100
            #room 4 -> room 6
            elif current_room_no == 4:
                current_room_no = 6
                current_room = rooms[current_room_no]
                player.rect.x = 590
                player.rect.y = 313
            #room 5 -> room 4
            elif current_room_no == 5:
                current_room_no = 4
                current_room = rooms[current_room_no]
                player.rect.x = 590
                player.rect.y = 313
            #room 6 -> room 7
            elif current_room_no == 6:
                current_room_no = 7
                current_room = rooms[current_room_no]
                player.rect.x = 590
                player.rect.y = 313

        #if player moves to the right of the screen to switch rooms
        if player.rect.x > 601:
            #room 0 -> room 2
            if current_room_no == 0:
                current_room_no = 2
                current_room = rooms[current_room_no]
                player.rect.x = 0
                player.rect.y = 313
            #room 1 -> room 0
            elif current_room_no == 1:
                current_room_no = 0
                current_room = rooms[current_room_no]
                player.rect.x = 0
                player.rect.y = 100
            #room 4 -> room 5
            elif current_room_no == 4:
                current_room_no = 5
                current_room = rooms[current_room_no]
                player.rect.x = 0
                player.rect.y = 313
            #room 6 -> room 4
            elif current_room_no == 6:
                current_room_no = 4
                current_room = rooms[current_room_no]
                player.rect.x = 0
                player.rect.y = 313
            #room 7 -> room 6
            elif current_room_no == 7:
                current_room_no = 6
                current_room = rooms[current_room_no]
                player.rect.x = 0
                player.rect.y = 313
            elif current_room_no == 5:
                trap = True

        #if player moves to the top of the screen to switch rooms
        if player.rect.y < -5:
            #room 2 -> room 3
            if current_room_no == 2:
                current_room_no = 3
                current_room = rooms[current_room_no]
                player.rect.x = 313
                player.rect.y = 650
            #room 3 -> room 4
            elif current_room_no == 3:
                current_room_no = 4
                current_room = rooms[current_room_no]
                player.rect.x = 313
                player.rect.y = 650
            #room 8 -> room 6
            elif current_room_no == 8:
                current_room_no = 6
                current_room = rooms[current_room_no]
                player.rect.x = 313
                player.rect.y = 650

        #if player moves to the bottom of the screen to switch rooms
        if player.rect.y > 651:
            #room 6 -> room 8
            if current_room_no == 6:
                current_room_no = 8
                current_room = rooms[current_room_no]
                player.rect.x = 313
                player.rect.y = 0
            #room 4 -> room 3
            elif current_room_no == 4:
                current_room_no = 3
                current_room = rooms[current_room_no]
                player.rect.x = 313
                player.rect.y = 0
            #room 3 -> room 2
            elif current_room_no == 3:
                current_room_no = 2
                current_room = rooms[current_room_no]
                player.rect.x = 313
                player.rect.y = 0

        #update all the sprite groups

        bullet_list.update()

        current_room.enemy_sprites.update()

        current_room.trophy_sprites.update()

        current_room.dragon_sprites.update()

        #check if player retrieves the trophy to move onto the final level
        block_hit_list = pygame.sprite.spritecollide(player, current_room.trophy_sprites, True)
        for block in block_hit_list:
            current_room_no = 9
            current_room = rooms[current_room_no]
            player.rect.x = 25
            player.rect.y = 555

        # Calculate mechanics for each bullet
        for bullet in bullet_list:
            # See if it hit a block
            block_hit_list = pygame.sprite.spritecollide(bullet, current_room.enemy_sprites, True)
            # For each block hit, remove the bullet and add to the score
            for block in block_hit_list:
                bullet_list.remove(bullet)
                #add points for every enemy killed
                score += 10

        # for the final level:
        for bullet in bullet_list:
            #see if bullet hit the dragon
            block_hit_list = pygame.sprite.spritecollide(bullet, current_room.dragon_sprites, False)
            # For each block hit, remove the bullet and add to the score
            for block in block_hit_list:
                block.hp -= 10
                bullet_list.remove(bullet)

                if block.hp <= 0:
                    pygame.sprite.spritecollide(bullet, current_room.dragon_sprites, True)
                    score += 100
                    bullet_list.remove(bullet)

        # See if it player hit an enemy
        block_hit_list = pygame.sprite.spritecollide(player, current_room.enemy_sprites, True)
        # For each enemy hit, remove the enemy and subtract health
        for block in block_hit_list:
            health -= 10

        #if health goes to 0 subtract a life
        if health <= 0 and lives == 3:
            lives = 2
            health = 100

        if health <= 0 and lives == 2:
            lives = 1
            health = 100

        if health <= 0 and lives == 1:
            game_over = True

        # --- Drawing --- #
        #fills background screen
        screen.fill(BLACK)

        #draw all the sprites on the screen

        movingsprites.draw(screen)

        current_room.wall_list.draw(screen)

        current_room.enemy_sprites.draw(screen)

        current_room.trophy_sprites.draw(screen)

        current_room.dragon_sprites.draw(screen)

        current_room.decoration_sprites.draw(screen)

        bullet_list.draw(screen)

        #if statements to show clue for the player is they're near a first aid kit
        if current_room_no == 0 and player.rect.x > 100 and player.rect.x < 200 and player.rect.y > 100 and player.rect.y < 200:
            screen.blit(clue,(550,0))

        if current_room_no == 0 and px > 100 and px < 200 and py > 100 and py < 200:
            health_visible = True
            current_room.health_sprites.draw(screen)

        if current_room_no == 1 and player.rect.x > 100 and player.rect.x < 200 and player.rect.y > 400 and player.rect.y < 500:
            screen.blit(clue,(550,0))

        if current_room_no == 1 and px > 100 and px < 200 and py > 400 and py < 500:
            health_visible = True
            current_room.health_sprites.draw(screen)

        if current_room_no == 2 and player.rect.x > 75 and player.rect.x < 150 and player.rect.y > 280 and player.rect.y < 320:
            screen.blit(clue,(550,0))

        if current_room_no == 2 and px > 75 and px < 150 and py > 280 and py < 320:
            health_visible = True
            current_room.health_sprites.draw(screen)

        if current_room_no == 3 and player.rect.x > 250 and player.rect.x < 300 and player.rect.y > 275 and player.rect.y < 325:
            screen.blit(clue,(550,0))

        if current_room_no == 3 and px > 250 and px < 300 and py > 275 and py < 325:
            health_visible = True
            current_room.health_sprites.draw(screen)

        if current_room_no == 4 and player.rect.x > 200 and player.rect.x < 300 and player.rect.y > 50 and player.rect.y < 150:
            screen.blit(clue,(550,0))

        if current_room_no == 4 and px > 100 and px < 300 and py > 50 and py < 150:
            health_visible = True
            current_room.health_sprites.draw(screen)

        if current_room_no == 5 and player.rect.x > 250 and player.rect.x < 350 and player.rect.y > 250 and player.rect.y < 350:
            screen.blit(clue,(550,0))

        if current_room_no == 5 and px > 250 and px < 350 and py > 250 and py < 350:
            health_visible = True
            current_room.health_sprites.draw(screen)

        if current_room_no == 6 and player.rect.x > 250 and player.rect.x < 350 and player.rect.y > 350 and player.rect.y < 350:
            screen.blit(clue,(550,0))

        if current_room_no == 6 and px > 250 and px < 350 and py > 250 and py < 350:
            health_visible = True
            current_room.health_sprites.draw(screen)

        if current_room_no == 7 and player.rect.x > 200 and player.rect.x < 300 and player.rect.y > 450 and player.rect.y < 550:
            screen.blit(clue,(550,0))

        if current_room_no == 7 and px > 200 and px < 300 and py > 450 and py < 550:
            health_visible = True
            current_room.health_sprites.draw(screen)

        if current_room_no == 8 and player.rect.x > 25 and player.rect.x < 75 and player.rect.y > 250 and player.rect.y < 350:
            screen.blit(clue,(550,0))

        if current_room_no == 8 and px > 25 and px < 75 and py > 250 and py < 350:
            health_visible = True
            current_room.health_sprites.draw(screen)

        #if user clicked on area and first aid kit is visible
        if health_visible == True:
            # See if player retrieves first aid kit
            block_hit_list = pygame.sprite.spritecollide(player, current_room.health_sprites, True)
            # For each first aid kit, remove the kit and increase health
            for block in block_hit_list:
                health += 20

        # -- print out the score, health, lives
        font = pygame.font.SysFont('Consolas', 35, True, False)

        text = font.render("score:", True, WHITE)
        screen.blit(text, [10,10])

        text = font.render(str(score), True, WHITE)
        screen.blit(text, [125,10])

        text = font.render("health:", True, WHITE)
        screen.blit(text, [185,10])

        text = font.render(str(health), True, WHITE)
        screen.blit(text, [335,10])

        text = font.render("lives:", True, WHITE)
        screen.blit(text, [425,10])

        text = font.render(str(lives), True, WHITE)
        screen.blit(text, [535,10])

        # if player has eliminated all the dragons, player wins
        if current_room_no == 9 and len(current_room.dragon_sprites) == 0:
            player_win = True

        if player_win == True:
            screen.fill(BLACK)
            # If game over is true, draw game over
            text = font.render("SCORE:", True, WHITE)
            screen.blit(text, [220, 200])
            text = font.render(str(score), True, WHITE)
            screen.blit(text, [340, 200])
            font = pygame.font.SysFont('Consolas', 35, True, False)
            text = font.render("YOU WIN", True, WHITE)
            screen.blit(text, [240, 250])
            text = font.render("GAME OVER", True, WHITE)
            screen.blit(text, [220, 300])

        #game over screen
        if game_over == True:
            screen.fill(BLACK)
            # If game over is true, draw game over
            text = font.render("YOU DIED", True, WHITE)
            screen.blit(text, [230, 250])
            font = pygame.font.SysFont('Consolas', 35, True, False)
            text = font.render("GAME OVER", True, WHITE)
            screen.blit(text, [220, 300])

        #game over screen
        if trap == True:
            screen.fill(BLACK)
            # If game over is true, draw game over
            font = pygame.font.SysFont('Consolas', 35, True, False)
            text = font.render("YOU FELL INTO A BLACK HOLE", True, WHITE)
            screen.blit(text, [50, 100])
            text = font.render("GAME OVER", True, WHITE)
            screen.blit(text, [220, 300])


        #update screen with what we've drawn
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
