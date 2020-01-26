import os
import pygame
import math
import random

#FIX VARIABLE
SIZE = (700, 500)
DIR = os.path.split(os.path.abspath(__file__))[0]
PLAYER_IMAGE = os.path.join(DIR, "assets", "spaceShips_001.png")
BULLET1_IMAGE = os.path.join(DIR, "assets", "spaceMissiles_001.png")
BULLET2_IMAGE = os.path.join(DIR, "assets", "spaceMissiles_006.png")
METEOR_IMAGE = os.path.join(DIR, "assets", "spaceMeteors_001.png")
BUILDING_IMAGE = os.path.join(DIR, "assets", "spaceBuilding_023.png")
ROCKET_IMAGE = os.path.join(DIR, "assets", "spaceRockets_002.png")
SATELITE_IMAGE = os.path.join(DIR, "assets", "spaceStation_018.png")
SPACESTATION_IMAGE = os.path.join(DIR, "assets", "spaceStation_021.png")
DEATH_IMAGE = os.path.join(DIR, "assets", "explosion1.png")
POWER_BULLET_IMAGE = os.path.join(DIR, "assets", "spaceBuilding_007.png")
SHOOT_SOUND = os.path.join(DIR, "assets", "laser5.ogg")
BOOM_SOUND = os.path.join(DIR, "assets", "boom.wav")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
HIGH_SCORE = 0

#ALL CLASS
def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0

def rotate(x, y):
    if x > 0 and y > 0:
        return 225
    elif x > 0 and y < 0:
        return 315
    elif x < 0 and y > 0:
        return 135
    elif x < 0 and y < 0:
        return 45
    elif x > 0:
        return 270
    elif y > 0:
        return 180
    elif x < 0:
        return 90
    elif y < 0:
        return 0
    else:
        return 0

class Block(pygame.sprite.Sprite):
    images = []
    def __init__(self):
        super().__init__()
        scale = random.randrange(1,  2)
        thing = random.randrange(5)
        if thing == 0:
            self.real_image = pygame.transform.scale(self.images[0], (20//scale, 20//scale))
        elif thing == 1:
            self.real_image = pygame.transform.scale(self.images[1], (32//scale, 9//scale))
        elif thing == 2:
            self.real_image = pygame.transform.scale(self.images[2], (15//scale, 30//scale))
        elif thing == 3:
            self.real_image = pygame.transform.scale(self.images[3], (34//scale, 10//scale))
        elif thing == 4:
            self.real_image = pygame.transform.scale(self.images[4], (17//scale, 28//scale))
            
        self.image = self.real_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.rect.x = random.randrange(SIZE[0] - self.width)
        self.rect.y = random.randrange(SIZE[1] - 100)
        self.x_change = random.randrange(-5,  5)
        self.y_change = random.randrange(-5,  5)
        self.angle = random.randrange(360)
        self.hit_poin = 2
        
    def reset_pos(self):
        self.rect.x = random.randrange(SIZE[0] - self.width)
        self.rect.y = random.randrange(-200, -10)
        
    def update(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        if (self.rect.x + self.width >= SIZE[0]) or (self.rect.x <= 0):
            self.x_change *= -1
        elif (self.rect.y + self.height >= SIZE[1]) or (self.rect.y <= 0):
            self.y_change *= -1        
        self.angle += 2
        if self.angle >= 360:
            self.angle=0
        self.image = pygame.transform.rotate(self.real_image, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)
            
class Player(pygame.sprite.Sprite):
    images = []
    def __init__(self):
        super().__init__()
        
        self.image = self.images[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 330
        self.rect.y = 450
        self.x_change = 0
        self.y_change = 0
        self.x_face = 0
        self.y_face = -1
    
    def update(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change         
        
        if self.x_change != 0 or self.y_change != 0:
            self.image = pygame.transform.rotate(self.images[0], rotate(self.x_change, self.y_change))
            self.x_face = sign(self.x_change)
            self.y_face = sign(self.y_change)
        
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x + self.rect.width >= SIZE[0]:
            self.rect.x = SIZE[0] - self.rect.width
            
        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y + self.rect.height >= SIZE[1]:
            self.rect.y = SIZE[1] - self.rect.height
            
class Bullet(pygame.sprite.Sprite):
    images = []
    def __init__(self, x, y, x_face, y_face, type):
        super().__init__()
        pygame.mixer.Sound(SHOOT_SOUND).play()
        if type == 1:
            self.image = pygame.transform.rotate(pygame.transform.scale(self.images[0], (4, 7)), rotate(x_face, y_face))
        elif type == 2:
            self.image = pygame.transform.rotate(pygame.transform.scale(self.images[1], (10, 15)), rotate(x_face, y_face))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bullet_speed = 20
        self.x_change = x_face * self.bullet_speed
        self.y_change = y_face * self.bullet_speed
    
    def update(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change      

class Death(pygame.sprite.Sprite):
    images = []
    def __init__(self, x, y):
        super().__init__()
        pygame.mixer.Sound(BOOM_SOUND).play()
        self.image = pygame.transform.scale(self.images[0], (50, 50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Power_Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(POWER_BULLET_IMAGE).convert(), (30, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SIZE[0] - 30)
        self.rect.y = random.randrange(SIZE[1] - 30)
        
class Game(object):
    def __init__(self, jml):
        self.score = 0
        self.font =  pygame.font.SysFont('Calibri', 20, True, False)
        self.speed_move = 10
        self.block_list = pygame.sprite.Group()
        self.all_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.power_bullet_list = pygame.sprite.Group()
        self.game_over = False
        self.win = False
        self.bullet_type = 1
        self.set_assets()
        self.jml = jml
        
        for i in range(jml):
            block = Block()
            self.block_list.add(block)
            self.all_list.add(block)
        self.player = Player()
        self.all_list.add(self.player)
        self.power_bullet = Power_Bullet()
        self.all_list.add(self.power_bullet)
        self.power_bullet_list.add(self.power_bullet)
        
    def set_assets(self):
        Player.images.append(pygame.transform.scale(pygame.image.load(PLAYER_IMAGE).convert(), (40, 40)))
        Bullet.images.append(pygame.image.load(BULLET1_IMAGE).convert())
        Bullet.images.append(pygame.image.load(BULLET2_IMAGE).convert())
        Block.images.append(pygame.image.load(METEOR_IMAGE).convert())
        Block.images.append(pygame.image.load(BUILDING_IMAGE).convert())
        Block.images.append(pygame.image.load(ROCKET_IMAGE).convert())
        Block.images.append(pygame.image.load(SATELITE_IMAGE).convert())
        Block.images.append(pygame.image.load(SPACESTATION_IMAGE).convert())
        Death.images.append(pygame.image.load(DEATH_IMAGE).convert())
    
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if self.win:
                        self.__init__(self.jml + 10)
                    else:
                        self.__init__(self.jml)
                else:
                    if event.key == pygame.K_ESCAPE:
                        return True
                    elif event.key == pygame.K_LEFT:
                        self.player.x_change += (-1)*self.speed_move
                    elif event.key == pygame.K_RIGHT:
                        self.player.x_change += (1)*self.speed_move
                    elif event.key == pygame.K_UP:
                        self.player.y_change += (-1)*self.speed_move
                    elif event.key == pygame.K_DOWN:
                        self.player.y_change += (1)*self.speed_move
                    elif event.key == pygame.K_SPACE:
                        bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, self.player.x_face, self.player.y_face, self.bullet_type)
                        self.bullet_list.add(bullet)
                        self.all_list.add(bullet)
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT):
                    self.player.x_change = 0
                elif (event.key == pygame.K_UP) or (event.key == pygame.K_DOWN):
                    self.player.y_change = 0
            elif event.type == pygame.JOYBUTTONDOWN:
                if my_joystick.get_button(0):
                    pass
                elif my_joystick.get_button(1):
                    pass
                elif my_joystick.get_button(2):
                    pass
                elif my_joystick.get_button(3):
                    pass
                    
        #if joystick_count != 0 and controller == "JOYSTICK":
            #x_axis = my_joystick.get_axis(0)
            #y_axis = my_joystick.get_axis(1)
            #player.x_change = int(x_axis * speed_move)
            #player.y_change = int(y_axis * speed_move)
            
        #if controller == "MOUSE":
            #mouse_pos = pygame.mouse.get_pos()
            #player.rect.x = mouse_pos[0]
            #player.rect.y = mouse_pos[1]
        return False
    
    def run_logic(self):
        global HIGH_SCORE
        if not self.game_over:
            for bullet in self.bullet_list:
                block_hit = pygame.sprite.spritecollide(bullet, self.block_list, False)
                for block in block_hit:
                    block.hit_poin -= self.bullet_type
                    self.bullet_list.remove(bullet)
                    self.all_list.remove(bullet)
                    if block.hit_poin <= 0:
                        pygame.mixer.Sound(BOOM_SOUND).play()
                        self.all_list.remove(block)
                        self.block_list.remove(block)
                        self.score += 1
                if bullet.rect.x < -10 or bullet.rect.y < -10 or bullet.rect.x > SIZE[0] + 10 or bullet.rect.y > SIZE[1] + 10:
                    self.bullet_list.remove(bullet)
                    self.all_list.remove(bullet)
                if len(self.block_list) == 0:
                    self.game_over = True
                    self.win = True
                    if HIGH_SCORE < self.score:
                        HIGH_SCORE = self.score                    
            if len(pygame.sprite.spritecollide(self.player, self.power_bullet_list, True)) > 0:
                self.bullet_type = 2
            block_hit = pygame.sprite.spritecollide(self.player, self.block_list, True)
            for block in block_hit:
                end = Death(self.player.rect.x, self.player.rect.y)
                self.all_list.add(end)
                self.all_list.remove(self.player)
                self.game_over = True
                self.win = False
                if HIGH_SCORE < self.score:
                    HIGH_SCORE = self.score
            self.all_list.update()
        
    def display_frame(self, screen):
        screen.fill(WHITE)
        self.all_list.draw(screen)
        high_score_text = self.font.render("High  Score: " + str(HIGH_SCORE), True, BLUE)
        score_text = self.font.render("Score: " + str(self.score), True, BLUE)
        screen.blit(high_score_text, [0, 25])
        screen.blit(score_text, [0, 0])
        if self.game_over:
            if self.win:
                text = self.font.render("Congratulation you win, push any key to restart", True, BLUE)
            else:
                text = self.font.render("Game Over, push any key to restart", True, BLUE)
            screen.blit(text, [(SIZE[0] // 2) - (text.get_width() // 2), (SIZE[1] // 2) - (text.get_height() // 2)])
        pygame.display.flip()
 

#ALL FUNCTION       
def main():
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()    
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Space Shooter")
    done = False
    clock = pygame.time.Clock()
    pygame.joystick.init()
    
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        print("Error, cant\'t find joystick")
    else:
        my_joystick = pygame.joystick.Joystick(0)
        my_joystick.init()
        print(my_joystick.get_name().rstrip() + " attach")
    controller = "KEYBOARD"
    if controller == "MOUSE":
        pygame.mouse.set_visible(False)
    
    game = Game(20)
    
    #MAIN LOOP
    while not done:
        
        #EVENT HANDLER
        done = game.process_events()
    
        #GAME LOGIC
        game.run_logic()
    
        #DRAWING OBJECT
        game.display_frame(screen)
        
        #MOVING OBJECT
        
        
        #FLIP & TICK
        clock.tick(20)
    
    pygame.quit()
    quit()


#RUN MAIN FUNCTION
if __name__ == "__main__":
    main()