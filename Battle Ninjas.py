import sys
import pygame
import random as rnd
from pygame.locals import *

pygame.init()

class Player(pygame.sprite.Sprite): # main player sprite for the wave mode
    def __init__(self, health):
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.centery = 400
        self.rect.x = 25
        self.hp = health

        self.dx = 5
        self.dy = 5

        self.stop = False

    def update(self):
        keys = pygame.key.get_pressed()
        # this code is to make sure that the player and enemy sprites cannot overlap
        #
        if keys[pygame.K_d]:
            self.rect.x += self.dx
            for enemy in enemy_list:
                if pygame.sprite.collide_rect(self, enemy):
                    self.rect.x -= self.dx
        if keys[pygame.K_a]:
            self.rect.x -= self.dx
            for enemy in enemy_list:
                if pygame.sprite.collide_rect(self, enemy):
                    self.rect.x += self.dx
        if keys[pygame.K_w]:
            self.rect.y -= self.dy
            for enemy in enemy_list:
                if pygame.sprite.collide_rect(self, enemy):
                    self.rect.y += self.dy
                    # i needed the x -= 1 because the player should still be
                    # able to move up and down if the enemy has collided with them from the right
                    self.rect.x -= 1
                    enemy.rect.x += enemy.dx
        if keys[pygame.K_s]:
            self.rect.y += self.dy
            for enemy in enemy_list:
                if pygame.sprite.collide_rect(self, enemy):
                    self.rect.y -= self.dy
                    self.rect.x -= 1
                    enemy.rect.x += enemy.dx

        # setting boundaries on where the player can move
        if self.rect.x < 25:
            self.rect.x = 25
        if self.rect.x > 250:
            self.rect.x = 250
        if self.rect.top < 200:
            self.rect.top = 200
        if self.rect.y > height - self.rect.height:
            self.rect.y = height - self.rect.height

class Player2(pygame.sprite.Sprite): # player sprite in boss battle mode
    def __init__(self, health):
        super().__init__()
        self.image = pygame.image.load("player2.png")
        self.rect = self.image.get_rect()
        self.rect.y = height - self.rect.height - 150
        self.rect.x = 25
        self.hp = health

        self.dx = 5
        self.dy = 0

        self.isJumping = False
        self.isFalling = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.x += self.dx
        if keys[pygame.K_a]:
            self.rect.x -= self.dx
        self.rect.y -= self.dy

        if self.rect.x < 25:
            self.rect.x = 25
        if self.rect.right > width / 2:
            self.rect.right = width / 2

        # this code is what i wrote to let the sprites jump
        # and only jump when they are on the ground
        if self.isJumping == True:
            if self.rect.y == height - self.rect.height - 150:
                self.dy = 13
            else:
                self.dy -= 0.5
            if self.dy == 0:
                self.isFalling = True
                self.isJumping = False
        if self.isFalling == True:
            self.dy -= 0.5
            if self.rect.y >= height - self.rect.height - 150:
                self.dy = 0
                self.rect.y = height - self.rect.height - 150
                self.isFalling = False

class Boss1(pygame.sprite.Sprite): # boss1 sprite
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("boss1.png")
        self.rect = self.image.get_rect()
        self.rect.y = height - self.rect.height - 150
        self.rect.x = 600
        self.hp = 1000

        self.dx = 1
        self.dy = 0

        self.time = 0
        #the boss jumps and throws shurikens at random intervals
        self.jumpTime = rnd.randint(30,90)
        self.throwTime = rnd.randint(60,120)

        self.isJumping = False
        self.isFalling = False

    def update(self):
        self.time += 1
        self.rect.x -= self.dx
        self.rect.y -= self.dy

        # always moves left and right
        if self.rect.left < width / 2:
            self.dx *= -1
        if self.rect.right > width:
            self.dx *= -1
        # jumps at a random interval, sets next random interval to jump at
        if self.time == self.jumpTime:
            self.isJumping = True
            self.jumpTime += rnd.randint(60,180)
        # also throws shurikens at random intervals, sets next random interval as well
        if self.time == self.throwTime:
            shuriken = Shuriken(-7)
            shuriken.rect.right = self.rect.right
            shuriken.rect.centery = self.rect.centery
            sprite_list.add(shuriken)
            enemy_shuriken_list.add(shuriken)
            self.throwTime += rnd.randint(60,210)

        if self.isJumping == True:
            if self.rect.y == height - self.rect.height - 150:
                self.dy = 13
            else:
                self.dy -= 0.5
            if self.dy == 0:
                self.isFalling = True
                self.isJumping = False
        if self.isFalling == True:
            self.dy -= 0.5
            if self.rect.y >= height - self.rect.height - 150:
                self.dy = 0
                self.rect.y = height - self.rect.height - 150
                self.isFalling = False

class Boss2(pygame.sprite.Sprite): #same code as boss1 with some minor tweaks to numbers
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("boss2.png")
        self.rect = self.image.get_rect()
        self.rect.y = height - self.rect.height - 150
        self.rect.x = 600
        self.hp = 1500

        self.dx = 1
        self.dy = 0

        self.time = 0
        self.jumpTime = rnd.randint(30,90)
        self.throwTime = rnd.randint(60,120)

        self.isJumping = False
        self.isFalling = False

    def update(self):
        self.time += 1
        self.rect.x -= self.dx
        self.rect.y -= self.dy

        if self.rect.left < width / 2:
            self.dx *= -1
            # self.rect.left = width / 2 + 100
        if self.rect.right > width:
            self.dx *= -1
            # self.rect.right = width

        if self.time == self.jumpTime:
            self.isJumping = True
            self.jumpTime += rnd.randint(60,180)

        if self.time == self.throwTime:
            shuriken = Shuriken(-7)
            shuriken.rect.right = self.rect.right
            shuriken.rect.centery = self.rect.centery
            sprite_list.add(shuriken)
            enemy_shuriken_list.add(shuriken)
            self.throwTime += rnd.randint(60,150)

        if self.isJumping == True:
            if self.rect.y == height - self.rect.height - 150:
                self.dy = 13
            else:
                self.dy -= 0.5
            if self.dy == 0:
                self.isFalling = True
                self.isJumping = False
        if self.isFalling == True:
            self.dy -= 0.5
            if self.rect.y >= height - self.rect.height - 150:
                self.dy = 0
                self.rect.y = height - self.rect.height - 150
                self.isFalling = False

class Boss3(pygame.sprite.Sprite): #same, minor tweaks to numbers
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("boss3.png")
        self.rect = self.image.get_rect()
        self.rect.y = height - self.rect.height - 150
        self.rect.x = 600
        self.hp = 2000

        self.dx = 1
        self.dy = 0

        self.time = 0
        self.jumpTime = rnd.randint(30,90)
        self.throwTime = rnd.randint(60,120)

        self.isJumping = False
        self.isFalling = False

    def update(self):
        self.time += 1
        self.rect.x -= self.dx
        self.rect.y -= self.dy

        if self.rect.left < width / 2:
            self.dx *= -1
            # self.rect.left = width / 2 + 100
        if self.rect.right > width:
            self.dx *= -1
            # self.rect.right = width

        if self.time == self.jumpTime:
            self.isJumping = True
            self.jumpTime += rnd.randint(60,180)

        if self.time == self.throwTime:
            shuriken = Shuriken(-7)
            shuriken.rect.right = self.rect.right
            shuriken.rect.centery = self.rect.centery
            sprite_list.add(shuriken)
            enemy_shuriken_list.add(shuriken)
            self.throwTime += rnd.randint(60,120)

        if self.isJumping == True:
            if self.rect.y == height - self.rect.height - 150:
                self.dy = 13
            else:
                self.dy -= 0.5
            if self.dy == 0:
                self.isFalling = True
                self.isJumping = False
        if self.isFalling == True:
            self.dy -= 0.5
            if self.rect.y >= height - self.rect.height - 150:
                self.dy = 0
                self.rect.y = height - self.rect.height - 150
                self.isFalling = False

class Boss4(pygame.sprite.Sprite): #same, with tweaks to numbers
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("boss4.png")
        self.rect = self.image.get_rect()
        self.rect.y = height - self.rect.height - 150
        self.rect.x = 600
        self.hp = 2500

        self.dx = 1
        self.dy = 0

        self.time = 0
        self.jumpTime = rnd.randint(30,90)
        self.throwTime = rnd.randint(60,120)

        self.isJumping = False
        self.isFalling = False

    def update(self):
        self.time += 1
        self.rect.x -= self.dx
        self.rect.y -= self.dy

        if self.rect.left < width / 2:
            self.dx *= -1
            # self.rect.left = width / 2 + 100
        if self.rect.right > width:
            self.dx *= -1
            # self.rect.right = width

        if self.time == self.jumpTime:
            self.isJumping = True
            self.jumpTime += rnd.randint(60,180)

        if self.time == self.throwTime:
            shuriken = Shuriken(-7)
            shuriken.rect.right = self.rect.right
            shuriken.rect.centery = self.rect.centery
            sprite_list.add(shuriken)
            enemy_shuriken_list.add(shuriken)
            self.throwTime += rnd.randint(30,90)

        if self.isJumping == True:
            if self.rect.y == height - self.rect.height - 150:
                self.dy = 13
            else:
                self.dy -= 0.5
            if self.dy == 0:
                self.isFalling = True
                self.isJumping = False
        if self.isFalling == True:
            self.dy -= 0.5
            if self.rect.y >= height - self.rect.height - 150:
                self.dy = 0
                self.rect.y = height - self.rect.height - 150
                self.isFalling = False

class Ground(pygame.sprite.Sprite): #ground sprite in boss battles
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ground.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = height - 150

class Wall(pygame.sprite.Sprite): #wall sprite
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("wall100.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.hp = 7500

    def update(self): # the wall has different sprites for how damaged it is, will dissapear if broken
        if self.hp > 5625:
            self.image = pygame.image.load("wall100.png")
        elif self.hp > 3750:
            self.image = pygame.image.load("wall75.png")
        elif self.hp > 1875:
            self.image = pygame.image.load("wall50.png")
        elif self.hp > 750:
            self.image = pygame.image.load("wall25.png")
        elif self.hp > 0:
            self.image = pygame.image.load("wall10.png")
        else:
            sprite_list.remove(wall)


class Enemy(pygame.sprite.Sprite): #class for wave enemies
    def __init__(self):
        super().__init__()
        self.time = rnd.randint(61,180)

    def update(self):
        self.time += 1
        # works with colision detection with player, will stop moving if they collide
        if self.stop == False:
            self.rect.x -= self.dx
            self.rect.y -= self.dy
        else:
            self.stop = False

        if self.rect.y > height - self.rect.height:
            self.dy *= -1
        if self.rect.y < 50:
            self.dy *= -1
        if self.rect.x < 250:
            self.rect.x = 250
            self.dx = 0

        # throws a shuriken every 3 seconds after random first throw
        if self.time % 180 == 0:
            shuriken = Shuriken(-7)
            shuriken.rect.right = self.rect.right
            shuriken.rect.centery = self.rect.centery
            sprite_list.add(shuriken)
            enemy_shuriken_list.add(shuriken)



class Enemy1(Enemy): #basic blue enemy
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy1.png")
        self.rect = self.image.get_rect()
        self.hp = 200
        self.dx = 3
        self.dy = 0
        self.rect.x = width

        # 4 possible lanes to spawn in, generates a random remaining lane
        self.lane = rnd.randint(0,3)
        while lanes[self.lane] == True:
            self.lane = rnd.randint(0,3)

        # spawns the enemy in the corresponding lane
        if lanes[self.lane] == False:
            if self.lane == 0:
                self.rect.centery = 250
                lanes[self.lane] = True
            elif self.lane == 1:
                self.rect.centery = 350
                lanes[self.lane] = True
            elif self.lane == 2:
                self.rect.centery = 450
                lanes[self.lane] = True
            elif self.lane == 3:
                self.rect.centery = 550
                lanes[self.lane] = True


class Enemy2(Enemy): #same as enemy1 but with number tweaks (this is the big and slow orange ninja)
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy2.png")
        self.rect = self.image.get_rect()
        self.hp = 400
        self.dx = 2
        self.dy = 0
        self.rect.x = width
        self.lane = rnd.randint(0, 3)
        while lanes[self.lane] == True:
            self.lane = rnd.randint(0, 3)

        if lanes[self.lane] == False:
            if self.lane == 0:
                self.rect.centery = 250
                lanes[self.lane] = True
            elif self.lane == 1:
                self.rect.centery = 350
                lanes[self.lane] = True
            elif self.lane == 2:
                self.rect.centery = 450
                lanes[self.lane] = True
            elif self.lane == 3:
                self.rect.centery = 550
                lanes[self.lane] = True

class Enemy3(Enemy): #same, but with number tweaks (this is the small and fast green ninja)
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy3.png")
        self.rect = self.image.get_rect()
        self.hp = 100
        self.dx = 5
        self.dy = 0
        self.rect.x = width
        self.lane = rnd.randint(0, 3)
        while lanes[self.lane] == True:
            self.lane = rnd.randint(0, 3)

        if lanes[self.lane] == False:
            if self.lane == 0:
                self.rect.centery = 250
                lanes[self.lane] = True
            elif self.lane == 1:
                self.rect.centery = 350
                lanes[self.lane] = True
            elif self.lane == 2:
                self.rect.centery = 450
                lanes[self.lane] = True
            elif self.lane == 3:
                self.rect.centery = 550
                lanes[self.lane] = True

class Enemy4(Enemy): #same, this is the elite purple ninja - more health and faster
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy4.png")
        self.rect = self.image.get_rect()
        self.hp = 400
        self.dx = 4
        self.dy = 0
        self.rect.x = width
        self.lane = rnd.randint(0, 3)
        while lanes[self.lane] == True:
            self.lane = rnd.randint(0, 3)

        if lanes[self.lane] == False:
            if self.lane == 0:
                self.rect.centery = 250
                lanes[self.lane] = True
            elif self.lane == 1:
                self.rect.centery = 350
                lanes[self.lane] = True
            elif self.lane == 2:
                self.rect.centery = 450
                lanes[self.lane] = True
            elif self.lane == 3:
                self.rect.centery = 550
                lanes[self.lane] = True

class Shuriken(pygame.sprite.Sprite): #sprite class for all shurikens
    def __init__(self, dx):
        super().__init__()
        self.dx = dx
        self.image = pygame.image.load("shuriken.png")
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.dx

class GameOver(pygame.sprite.Sprite): #game over screen
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("gameover.jpg")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class YouWin(pygame.sprite.Sprite): #you win screen
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("youwin.jpg")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class PlayerIcon(pygame.sprite.Sprite): #player icon beside health bar
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player icon.png")
        self.rect = self.image.get_rect()
        self.rect.x = 45
        self.rect.centery = 50

class BossIcon(pygame.sprite.Sprite): #boss icon beside boss health bar
    def __init__(self):
        super().__init__()

        # icon will be dependent on which boss battle is happening
        if bossBattle1 == True:
            self.image = pygame.image.load("boss1 icon.png")
        if bossBattle2 == True:
            self.image = pygame.image.load("boss2 icon.png")
        if bossBattle3 == True:
            self.image = pygame.image.load("boss3 icon.png")
        if bossBattle4 == True:
            self.image = pygame.image.load("boss4 icon.png")

        self.rect = self.image.get_rect()
        self.rect.right = width - 20
        self.rect.centery = 50

class PlayerHealthBar(pygame.sprite.Sprite): #player health bar
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("healthbar100.png")
        self.rect = self.image.get_rect()
        self.rect.x = 140
        self.rect.centery = 50

    #the health bar sprite updates to show the player's remaining health
    def update(self):
        if health > 1200:
            self.image = pygame.image.load("healthbar100.png")
        elif health > 900:
            self.image = pygame.image.load("healthbar80.png")
        elif health > 600:
            self.image = pygame.image.load("healthbar60.png")
        elif health > 300:
            self.image = pygame.image.load("healthbar40.png")
        elif health > 0:
            self.image = pygame.image.load("healthbar20.png")
        elif health <= 0:
            self.image = pygame.image.load("healthbar0.png")

class BossHealthBar(pygame.sprite.Sprite): #boss health bar sprite
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bosshealthbar100.png")
        self.rect = self.image.get_rect()
        self.rect.right = 785
        self.rect.centery = 50

    # only appears during boss battles
    # each boss has a different amount of health, so i hard-coded each one
    def update(self):
        if bossBattle1 == True:
            if boss1.hp > 800:
                self.image = pygame.image.load("bosshealthbar100.png")
            elif boss1.hp > 600:
                self.image = pygame.image.load("bosshealthbar80.png")
            elif boss1.hp > 400:
                self.image = pygame.image.load("bosshealthbar60.png")
            elif boss1.hp > 200:
                self.image = pygame.image.load("bosshealthbar40.png")
            elif boss1.hp > 0:
                self.image = pygame.image.load("bosshealthbar20.png")
            elif boss1.hp <= 0:
                self.image = pygame.image.load("bosshealthbar0.png")

        if bossBattle2 == True:
            if boss2.hp > 1200:
                self.image = pygame.image.load("bosshealthbar100.png")
            elif boss2.hp > 900:
                self.image = pygame.image.load("bosshealthbar80.png")
            elif boss2.hp > 600:
                self.image = pygame.image.load("bosshealthbar60.png")
            elif boss2.hp > 300:
                self.image = pygame.image.load("bosshealthbar40.png")
            elif boss2.hp > 0:
                self.image = pygame.image.load("bosshealthbar20.png")
            elif boss2.hp <= 0:
                self.image = pygame.image.load("bosshealthbar0.png")

        if bossBattle3 == True:
            if boss3.hp > 1600:
                self.image = pygame.image.load("bosshealthbar100.png")
            elif boss3.hp > 1200:
                self.image = pygame.image.load("bosshealthbar80.png")
            elif boss3.hp > 800:
                self.image = pygame.image.load("bosshealthbar60.png")
            elif boss3.hp > 400:
                self.image = pygame.image.load("bosshealthbar40.png")
            elif boss3.hp > 0:
                self.image = pygame.image.load("bosshealthbar20.png")
            elif boss3.hp <= 0:
                self.image = pygame.image.load("bosshealthbar0.png")

        if bossBattle4 == True:
            if boss4.hp > 2000:
                self.image = pygame.image.load("bosshealthbar100.png")
            elif boss4.hp > 1500:
                self.image = pygame.image.load("bosshealthbar80.png")
            elif boss4.hp > 1000:
                self.image = pygame.image.load("bosshealthbar60.png")
            elif boss4.hp > 500:
                self.image = pygame.image.load("bosshealthbar40.png")
            elif boss4.hp > 0:
                self.image = pygame.image.load("bosshealthbar20.png")
            elif boss4.hp <= 0:
                self.image = pygame.image.load("bosshealthbar0.png")

class Wave(pygame.sprite.Sprite): # wave sprite at top of screen to display current wave
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("wave.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2 - 20
        self.rect.centery = 50

class WaveNum(pygame.sprite.Sprite): # wave number, updates based on current wave
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("1.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2 + 120
        self.rect.centery = 50

    def update(self):
        if wave1 == True:
            self.image = pygame.image.load("1.png")
        if wave2 == True:
            self.image = pygame.image.load("2.png")
        if wave3 == True:
            self.image = pygame.image.load("3.png")
        if wave4 == True:
            self.image = pygame.image.load("4.png")

class BossIncoming(pygame.sprite.Sprite): #boss incoming... message
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("boss incoming.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.centery = height / 2 - 50

class Wave1Complete(pygame.sprite.Sprite): #wave complete message
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("wave 1 complete.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.centery = height / 2 - 50

class Wave2Complete(pygame.sprite.Sprite): #same
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("wave 2 complete.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.centery = height / 2 - 50

class Wave3Complete(pygame.sprite.Sprite): #same
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("wave 3 complete.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.centery = height / 2 - 50

class Wave4Complete(pygame.sprite.Sprite): #same
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("wave 4 complete.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.centery = height / 2 - 50

class WallDestroyed(pygame.sprite.Sprite): #wall destroyed message
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("wall destroyed.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.centery = height / 2 - 50

class Instructions(pygame.sprite.Sprite): #instructions message at start screen
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("instructions.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.centery = height / 2

width = 900
height = 600

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Battle Ninjas")

#two background images that i use
bg = pygame.image.load("Forest.png")
instructions_bg = pygame.image.load("instructions background.png")

FPS = 60
fpsClock = pygame.time.Clock()

#custom user events to spawn enemies
spawn_enemy1 = pygame.USEREVENT
pygame.event.Event(spawn_enemy1)

spawn_enemy2 = pygame.USEREVENT + 1
pygame.event.Event(spawn_enemy2)

spawn_enemy3 = pygame.USEREVENT + 2
pygame.event.Event(spawn_enemy3)

spawn_enemy4 = pygame.USEREVENT + 3
pygame.event.Event(spawn_enemy4)

#initializing all my sprite groups
sprite_list = pygame.sprite.Group()
shuriken_list = pygame.sprite.Group()
enemy_shuriken_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()
temp_list = pygame.sprite.Group()
temp_enemy_list = pygame.sprite.Group()

#player's starting health
health = 1500

#instructions at start of game
instructions = Instructions()
sprite_list.add(instructions)

sprite_list.update()
screen.blit(instructions_bg, (0,0))
sprite_list.draw(screen)
pygame.display.flip()
begin_game = False

while begin_game == False:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        # once the player clicks on the screen, the game begins
        if event.type == MOUSEBUTTONDOWN:
            begin_game = True

sprite_list.remove(instructions)

# adding sprites to the screen
player = Player(health)
sprite_list.add(player)
player_list.add(player)

wall = Wall()
sprite_list.add(wall)

playerIcon = PlayerIcon()
sprite_list.add(playerIcon)

playerHealthBar = PlayerHealthBar()
sprite_list.add(playerHealthBar)

wave = Wave()
sprite_list.add(wave)

waveNum = WaveNum()
sprite_list.add(waveNum)

# setting up all of my variables
lanes = [False,False,False,False]

time = 0
temp_time = 10000000
temp_time2 = 10000000
spawned = 0
wave1 = True
bossBattle1 = False
bossBattle1Completed = False
bossBattle2 = False
bossBattle2Completed = False
bossBattle3 = False
bossBattle3Completed = False
bossBattle4 = False
bossBattle4Completed = False
wave2 = False
wave3 = False
wave4 = False
lastWave = ""
setup = False
setup2 = False
setup3 = False
setup4 = False
gameCompleted = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT: #when the user closes the window
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_g:
                # for the player to throw a shuriken at enemies
                if player in sprite_list:
                    if len(shuriken_list) < 3 and bossBattle1 == False and bossBattle2 == False and bossBattle3 == False and bossBattle4 == False:
                        shuriken = Shuriken(7)
                        shuriken.rect.left = player.rect.right - 20
                        shuriken.rect.centery = player.rect.centery
                        sprite_list.add(shuriken)
                        shuriken_list.add(shuriken)
                if bossBattle1 == True or bossBattle2 == True or bossBattle3 == True or bossBattle4 == True:
                    if player2 in sprite_list:
                        if len(shuriken_list) < 3:
                            shuriken = Shuriken(7)
                            shuriken.rect.left = player2 .rect.right - 20
                            shuriken.rect.centery = player2.rect.centery
                            sprite_list.add(shuriken)
                            shuriken_list.add(shuriken)
            #if in a boss battle, space bar to jump, if player is standing on the ground
            if event.key == K_SPACE:
                if bossBattle1 == True or bossBattle2 == True or bossBattle3 == True or bossBattle4 == True or bossBattle4Completed == True:
                    if player2.rect.y == height - player2.rect.height - 150:
                        player2.isJumping = True
        # custom events to spawn enemies
        if event.type == spawn_enemy1:
            basicEnemy = Enemy1()
            sprite_list.add(basicEnemy)
            enemy_list.add(basicEnemy)

        if event.type == spawn_enemy2:
            largeEnemy = Enemy2()
            sprite_list.add(largeEnemy)
            enemy_list.add(largeEnemy)

        if event.type == spawn_enemy3:
            fastEnemy = Enemy3()
            sprite_list.add(fastEnemy)
            enemy_list.add(fastEnemy)

        if event.type == spawn_enemy4:
            eliteEnemy = Enemy4()
            sprite_list.add(eliteEnemy)
            enemy_list.add(eliteEnemy)

    # to check for enemy collisions
    for enemy in enemy_list:
        enemy.stop = False
        if pygame.sprite.collide_rect(player,enemy):
            enemy.stop = True

    # this is all code to check for collisions of player shurikens with enemies
    for shuriken in shuriken_list:
        # removes the shuriken if it goes off the screen
        if shuriken.rect.x > width:
            sprite_list.remove(shuriken)
            shuriken_list.remove(shuriken)
        for enemy in enemy_list:
            enemy_hit_list = pygame.sprite.spritecollide(shuriken,enemy_list,False)
            shuriken_hit_list = pygame.sprite.spritecollide(enemy, shuriken_list, False)


            # damages enemy if it hits
            for enemy_hit in enemy_hit_list:
                for shuriken in shuriken_hit_list:
                    sprite_list.remove(shuriken)
                    shuriken_list.remove(shuriken)
                    enemy_hit.hp -= 100

                    # if the enemy's hp goes to 0, it's removed
                    if enemy_hit.hp <= 0:
                        enemy_list.remove(enemy_hit)
                        sprite_list.remove(enemy_hit)
                        # frees up the lane for another enemy to spawn in that lane
                        if wave1 == True or wave2 == True or wave3 == True or wave4 == True:
                            lanes[enemy_hit.lane] = False

                        # to check if it was the last enemy of the wave, if it was, initiate the boss battle
                        if wave1 == True and spawned >= 5 and len(enemy_list) == 0:
                            if wall.hp > 0 and health > 0:
                                wave1 = False
                                spawned = 0
                                time = 0
                                bossIncoming = BossIncoming()
                                sprite_list.add(bossIncoming)

                        if wave2 == True and spawned >= 10 and len(enemy_list) == 0:
                            if wall.hp > 0 and health > 0:
                                wave2 = False
                                spawned = 0
                                time = 0
                                lastWave = "wave2"
                                bossIncoming = BossIncoming()
                                sprite_list.add(bossIncoming)

                        if wave3 == True and spawned >= 15 and len(enemy_list) == 0:
                            if wall.hp > 0 and health > 0:
                                wave3 = False
                                spawned = 0
                                time = 0
                                lastWave = "wave3"
                                bossIncoming = BossIncoming()
                                sprite_list.add(bossIncoming)

                        if wave4 == True and spawned >= 20 and len(enemy_list) == 0:
                            if wall.hp > 0 and health > 0:
                                wave4 = False
                                spawned = 0
                                time = 0
                                lastWave = "wave4"
                                bossIncoming = BossIncoming()
                                sprite_list.add(bossIncoming)


    # code to check for enemy shuriken collisions with player
    for shuriken in enemy_shuriken_list:
        enemy_shuriken_hit_list = pygame.sprite.spritecollide(player, enemy_shuriken_list, False)

        # damages wall if it's hit
        if shuriken.rect.x < 25:
            sprite_list.remove(shuriken)
            enemy_shuriken_list.remove(shuriken)
            wall.hp -= 100

        # hurts player if player is hit, removes player if hp reaches 0
        for player in player_list:
            for shuriken in enemy_shuriken_hit_list:
                sprite_list.remove(shuriken)
                enemy_shuriken_list.remove(shuriken)
                health -= 100

                if health <= 0:
                    sprite_list.remove(player)
                    player_list.remove(player)

    # to keep track of time for events
    time += 1

    # wave 1 code
    # code is roughly the same for all waves, i will only comment notable differences for wave 2-4

    # spawns enemies
    if wave1 == True and time % 90 == 0 and spawned < 5 and len(enemy_list) < 4:
        pygame.event.post(pygame.event.Event(spawn_enemy1))
        spawned += 1

    # if wave1 is complete, wait 3 seconds before starting boss battle
    if wave1 == False and time == 180 and lastWave == "":
        lastWave = "wave1"

    # initiates the boss battle
    if wave1 == False and lastWave == "wave1" and bossBattle1 == False and bossBattle1Completed == False:
        bossBattle1 = True
        setup = True

    # setting up all of the sprites for the boss battle
    if bossBattle1 == True and setup == True:
        sprite_list.remove(player)
        player_list.remove(player)

        for shuriken in shuriken_list:
            sprite_list.remove(shuriken)
            shuriken_list.remove(shuriken)
        for shuriken in enemy_shuriken_list:
            sprite_list.remove(shuriken)
            enemy_shuriken_list.remove(shuriken)

        player2 = Player2(health)
        sprite_list.add(player2)
        player_list.add(player2)

        boss1 = Boss1()
        sprite_list.add(boss1)
        enemy_list.add(boss1)

        ground = Ground()
        sprite_list.add(ground)

        bossHealthBar = BossHealthBar()
        bossIcon = BossIcon()
        sprite_list.add(bossHealthBar)
        sprite_list.add(bossIcon)

        sprite_list.remove(bossIncoming)

        setup = False

    # checks to see if boss has been defeated
    if bossBattle1 == True and bossBattle1Completed == False:
        if wall.hp > 0 and health > 0:
            if boss1.hp <= 0:
                time = 0
                bossBattle1Completed = True
                wave1Completed = Wave1Complete()
                sprite_list.add(wave1Completed)

    # waits 5 seconds before starting wave 2 and re-adding all necessary sprites
    if bossBattle1Completed == True and lastWave == "wave1":
        if time == 300:
            wave2 = True
            sprite_list.remove(player2)
            player_list.remove(player2)
            player = Player(health)
            sprite_list.add(player)
            player_list.add(player)
            sprite_list.remove(ground)
            for shuriken in enemy_shuriken_list:
                sprite_list.remove(shuriken)
                enemy_shuriken_list.remove(shuriken)
            bossBattle1 = False

            sprite_list.remove(bossHealthBar)
            sprite_list.remove(bossIcon)
            sprite_list.remove(wave1Completed)

    # wave 2

    if wave2 == True and time % 90 == 0 and spawned < 10 and len(enemy_list) < 4:
        num = rnd.randint(1,2)
        if num == 1:
            pygame.event.post(pygame.event.Event(spawn_enemy1))
            spawned += 1
            # in wave 2, if a blue enemy is spawned, there is a 1/3 chance a second will spawn at the same time
            temp_num = rnd.randint(0,2)
            if temp_num == 0:
                if len(enemy_list) < 3:
                    pygame.event.post(pygame.event.Event(spawn_enemy1))
                    spawned += 1

        if num == 2:
            pygame.event.post(pygame.event.Event(spawn_enemy2))
            spawned += 1

    if wave2 == False and lastWave == "wave2" and bossBattle2 == False and bossBattle2Completed == False and bossBattle1Completed == True and time == 180:
        bossBattle2 = True
        setup2 = True


    if bossBattle2 == True and setup2 == True:
        sprite_list.remove(player)
        player_list.remove(player)

        for shuriken in shuriken_list:
            sprite_list.remove(shuriken)
            shuriken_list.remove(shuriken)
        for shuriken in enemy_shuriken_list:
            sprite_list.remove(shuriken)
            enemy_shuriken_list.remove(shuriken)

        player2 = Player2(health)
        sprite_list.add(player2)
        player_list.add(player2)

        boss2 = Boss2()
        sprite_list.add(boss2)
        enemy_list.add(boss2)

        ground = Ground()
        sprite_list.add(ground)

        bossHealthBar = BossHealthBar()
        bossIcon = BossIcon()
        sprite_list.add(bossHealthBar)
        sprite_list.add(bossIcon)

        sprite_list.remove(bossIncoming)

        setup2 = False

    if bossBattle2 == True and bossBattle2Completed == False:
        if wall.hp > 0 and health > 0:
            if boss2.hp <= 0:
                time = 0
                bossBattle2Completed = True
                wave2Completed = Wave2Complete()
                sprite_list.add(wave2Completed)


    if bossBattle2Completed == True and lastWave == "wave2":
        if time == 300:
            wave3 = True
            sprite_list.remove(player2)
            player_list.remove(player2)
            player = Player(health)
            sprite_list.add(player)
            player_list.add(player)
            sprite_list.remove(ground)
            for shuriken in enemy_shuriken_list:
                sprite_list.remove(shuriken)
                enemy_shuriken_list.remove(shuriken)
            bossBattle2 = False
            sprite_list.remove(bossHealthBar)
            sprite_list.remove(bossIcon)
            sprite_list.remove(wave2Completed)

    # wave 3

    if wave3 == True and time % 90 == 0 and spawned < 15  and len(enemy_list) < 4:
        num = rnd.randint(1,3)
        if num == 1:
            pygame.event.post(pygame.event.Event(spawn_enemy1))
            spawned += 1
            # 1/2 chance of spawning 2 blue enemies at once
            temp_num = rnd.randint(0, 1)
            if len(enemy_list) < 3 and temp_num == 0:
                pygame.event.post(pygame.event.Event(spawn_enemy1))
                spawned += 1
        elif num == 2:
            pygame.event.post(pygame.event.Event(spawn_enemy2))
            spawned += 1
            # 1/3 chance of spawning an orange and green enemy at the same time
            temp_num = rnd.randint(0, 2)
            if len(enemy_list) < 3 and temp_num == 0:
                pygame.event.post(pygame.event.Event(spawn_enemy3))
                spawned += 1
        else:
            pygame.event.post(pygame.event.Event(spawn_enemy3))
            spawned += 1

    if wave3 == False and lastWave == "wave3" and bossBattle3 == False and bossBattle3Completed == False and bossBattle2Completed == True and time == 180:
        bossBattle3 = True
        setup3 = True


    if bossBattle3 == True and setup3 == True:
        sprite_list.remove(player)
        player_list.remove(player)

        for shuriken in shuriken_list:
            sprite_list.remove(shuriken)
            shuriken_list.remove(shuriken)
        for shuriken in enemy_shuriken_list:
            sprite_list.remove(shuriken)
            enemy_shuriken_list.remove(shuriken)

        player2 = Player2(health)
        sprite_list.add(player2)
        player_list.add(player2)

        boss3 = Boss3()
        sprite_list.add(boss3)
        enemy_list.add(boss3)

        ground = Ground()
        sprite_list.add(ground)

        bossHealthBar = BossHealthBar()
        bossIcon = BossIcon()
        sprite_list.add(bossHealthBar)
        sprite_list.add(bossIcon)

        sprite_list.remove(bossIncoming)

        setup3 = False

    if bossBattle3 == True and bossBattle3Completed == False:
        if wall.hp > 0 and health > 0:
            if boss3.hp <= 0:
                time = 0
                bossBattle3Completed = True
                wave3Completed = Wave3Complete()
                sprite_list.add(wave3Completed)


    if bossBattle3Completed == True and lastWave == "wave3":
        if time == 300:
            wave4 = True
            sprite_list.remove(player2)
            player_list.remove(player2)
            player = Player(health)
            sprite_list.add(player)
            player_list.add(player)
            sprite_list.remove(ground)
            for shuriken in enemy_shuriken_list:
                sprite_list.remove(shuriken)
                enemy_shuriken_list.remove(shuriken)
            bossBattle3 = False
            sprite_list.remove(bossHealthBar)
            sprite_list.remove(bossIcon)
            sprite_list.remove(wave3Completed)

    # wave 4

    if wave4 == True and time % 90 == 0 and spawned < 20 and len(enemy_list) < 4:
        num = rnd.randint(1, 4)
        if num == 1:
            pygame.event.post(pygame.event.Event(spawn_enemy1))
            spawned += 1
            # 1/2 chance to spawn 2 blue enemies at once, 1/2 chance to spawn 3 blue enemies at once
            temp_num = rnd.randint(0, 1)
            if len(enemy_list) < 3 and temp_num == 0:
                pygame.event.post(pygame.event.Event(spawn_enemy1))
                spawned += 1
            if len(enemy_list) < 3 and temp_num == 1:
                pygame.event.post(pygame.event.Event(spawn_enemy1))
                spawned += 1
                if len(enemy_list) < 2:
                    pygame.event.post(pygame.event.Event(spawn_enemy1))
                    spawned += 1
        elif num == 2:
            pygame.event.post(pygame.event.Event(spawn_enemy2))
            spawned += 1
            # always spawns a green enemy if an orange enemy spawns
            if len(enemy_list) < 3:
                pygame.event.post(pygame.event.Event(spawn_enemy3))
                spawned += 1
        elif num == 3:
            pygame.event.post(pygame.event.Event(spawn_enemy3))
            spawned += 1
            temp_num = rnd.randint(0,1)
            # 1/2 chance of spawning 2 green enemies at once
            if len(enemy_list) < 3 and temp_num == 0:
                pygame.event.post(pygame.event.Event(spawn_enemy3))
                spawned += 1
        else:
            pygame.event.post(pygame.event.Event(spawn_enemy4))
            spawned += 1
            temp_num = rnd.randint(0, 1)
            # 1/2 chance of spawning a blue enemy when a purple enemy spawns
            if len(enemy_list) < 3 and temp_num == 0:
                pygame.event.post(pygame.event.Event(spawn_enemy1))
                spawned += 1

    if wave4 == False and lastWave == "wave4" and bossBattle4 == False and bossBattle4Completed == False and bossBattle3Completed == True and time == 180:
        bossBattle4 = True
        setup4 = True


    if bossBattle4 == True and setup4 == True:
        sprite_list.remove(player)
        player_list.remove(player)

        for shuriken in shuriken_list:
            sprite_list.remove(shuriken)
            shuriken_list.remove(shuriken)
        for shuriken in enemy_shuriken_list:
            sprite_list.remove(shuriken)
            enemy_shuriken_list.remove(shuriken)

        player2 = Player2(health)
        sprite_list.add(player2)
        player_list.add(player2)

        boss4 = Boss4()
        sprite_list.add(boss4)
        enemy_list.add(boss4)

        ground = Ground()
        sprite_list.add(ground)

        bossHealthBar = BossHealthBar()
        bossIcon = BossIcon()
        sprite_list.add(bossHealthBar)
        sprite_list.add(bossIcon)

        sprite_list.remove(bossIncoming)

        setup4 = False

    if bossBattle4 == True and bossBattle4Completed == False:
        if boss4.hp <= 0:
            if wall.hp > 0 and health > 0:
                time = 0
                bossBattle4Completed = True
                wave4Completed = Wave4Complete()
                sprite_list.add(wave4Completed)


    if bossBattle4Completed == True and lastWave == "wave4":
        if time == 300:
            sprite_list.remove(wave4Completed)
            for shuriken in enemy_shuriken_list:
                sprite_list.remove(shuriken)
                enemy_shuriken_list.remove(shuriken)
            bossBattle4 = False
            gameCompleted = True

    # if the player's health runs out, set a timer for 3 seconds before the game over screen appears
    if wave1 == True or wave2 == True or wave3 == True or wave4 == True:
        if health == 0:
            temp_time = time
            health = -100
    if bossBattle1 == True or bossBattle2 == True or bossBattle3 == True or bossBattle4 == True:
        if health == 0:
            temp_time = time
            health = -100

    # if the wall is destroyed, set a timer for 3 seconds before the game over screen appears
    if wall.hp == 0:
        temp_time = time
        wallDestroyed = WallDestroyed()
        sprite_list.add(wallDestroyed)
        wall.hp = -100

    # if the player wins the game, set a timer for 3 seconds before the you win screen
    if bossBattle4Completed == True and gameCompleted == True:
        temp_time2 = time
        gameCompleted = False

    # game over screen, then exits the program
    if temp_time + 180 == time:
        game_over = GameOver()
        sprite_list.add(game_over)
        sprite_list.update()
        sprite_list.draw(screen)
        pygame.display.flip()
        pygame.time.delay(5000)
        pygame.quit()
        sys.exit()

    # you win screen, then exits the program
    if temp_time2 + 180 == time:
        you_win = YouWin()
        sprite_list.add(you_win)
        sprite_list.update()
        sprite_list.draw(screen)
        pygame.display.flip()
        pygame.time.delay(5000)
        pygame.quit()
        sys.exit()

    #updating sprites and the screen every loop
    sprite_list.update()
    screen.blit(bg, (0,0))
    sprite_list.draw(screen)
    pygame.display.flip()
    fpsClock.tick(FPS)