import pygame, sys, time, random
from pygame.locals import *



health = 0
#global health
#pygame.font.init()

def game(level):
    ######## Global declarations #####
    global health
    global count3
    count3 = 02
    walls = 4
    
    pygame.mixer.pre_init(44100, -16, 2, 2048) #sound buffer
    pygame.init() #init pygame
    pygame.mixer.init() #pygame sound
    killE = False
    mainClock = pygame.time.Clock() #used to set FPS
    global speedX
    speedX = 2 + level
    scrn = pygame.display.set_mode((2000, 1550)) #set screen size
    #scrn = pygame.display.set_mode((800, 600)), FULLSCREEN | HWSURFACE | DOUBLEBUF, 3
    NUMSHIPS = 1 #number of ships
    global bulletType
    bulletType = 1
    global bullets
    bullets = []
    global bulletsList
    bulletsList = pygame.sprite.Group(bullets)
    basicFont = pygame.font.SysFont(None, 40) #Create font for txt display
    bigFont = pygame.font.SysFont(None, 150) 
    largeFont = pygame.font.SysFont(None, 500)
    global ebullets
    ebullets = []
    global EBulletsList
    EBulletsList = pygame.sprite.Group(ebullets)
    global enemy
    enemy =[]
    global enemyList
    enemyList = pygame.sprite.Group(enemy)
    global explodes
    explodes = []
    global explodeList
    explodeList = pygame.sprite.Group(explodes)

    #######Load graphics and sound########
    shipPic0 = pygame.image.load('player.png').convert_alpha()
    shipPic = pygame.transform.scale(shipPic0, (100, 100))
    enemyPic0 = pygame.image.load('enemy.png').convert_alpha()
    enemyPic00 = pygame.transform.scale(enemyPic0, (80, 80))
    enemyPic = pygame.transform.flip(enemyPic00, False, True)
    bulletPic = pygame.image.load('missile.png').convert_alpha()
    direc = pygame.image.load('testdir.png').convert_alpha()
    ebulletPic = pygame.transform.flip(bulletPic, False, True)
    explodePic = pygame.image.load('explode.png').convert_alpha()
    explodeSmallPic = pygame.image.load('explode.png').convert_alpha() #explodesmall
    explodeExtraSmallPic = pygame.image.load('explodeextrasmall.png').convert_alpha()
    bg = pygame.image.load('bg.png').convert()
    las = pygame.mixer.Sound('hit.ogg')
    swish = pygame.mixer.Sound('swish.ogg')
    lose = pygame.mixer.Sound('lose.ogg')
    explode = pygame.mixer.Sound('exp.ogg')
    
    music = pygame.mixer.Sound('bgMusic.ogg')


    
    def checkCollision(sprite1, sprite2, ty = 0): # COLLISION
        rect = [sprite1.rect.left, sprite1.rect.right, sprite1.rect.top, sprite1.rect.bottom]
        if ty == 0:
            if sprite2.rect.right > rect[0] and sprite2.rect.left < rect[1] and sprite2.rect.bottom > rect[2] and sprite2.rect.top < rect[3]: ## ALL MUST BE TRUE FOR COL ##
                col = True # IS
            else:
                col = False #Not
        return col #send the data that it collides or doesn't regardless


                
    class EnemySprite(pygame.sprite.Sprite):
        def __init__(self, row, column):
            pygame.sprite.Sprite.__init__(self)
            self.image = enemyPic
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect.top = row
            self.rect.left = column
            self.health = 10
        def update(self):
            global speedX
            
            self.rect.left += speedX
                
            if self.rect.left < 99:
                speedX = abs(speedX)
                
            if self.rect.right > 1899:
                speedX = -abs(speedX)
                
            if killE == True:
                self.kill()
            shoot = random.randint(0,100 - (10*level)) #140  #20
            if shoot == 11:
                ebullets.append(EnemyBullet(self.rect.center))
                EBulletsList = pygame.sprite.Group(ebullets) 


    class EnemyBullet(pygame.sprite.Sprite):
        def __init__(self, start):
            pygame.sprite.Sprite.__init__(self)
            self.image = ebulletPic
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.center = start
            self.rect.top += 30
            self.dx = level * .5 # 2 + (level * .25)
            
        def update(self):
            global EBulletsList
            global ebullets
            self.dx *= 1.1
            if self.rect.top + self.dx < 1600:
                self.rect.top += self.dx
            else:
                self.kill()
                EBulletsList.remove(self)
                del ebullets[ebullets.index(self)]

            
    class ShipSprite(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = shipPic
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.top = 1400
            self.rect.left = 1000
            keyA = False
            keyD = False
            self.dx = 10
            self.a = 0
            
        def update(self):
            global keyA
            global keyD
            if keyA == True:
                self.a = True
                if self.dx < 20:
                    self.dx += 6
                self.rect.left -= self.dx
                self.rect.right += self.dx
            elif keyD == True:
                self.a = False
                if self.dx < 17:
                    self.dx += 6
                self.rect.left += self.dx
                self.rect.right -= self.dx
            else:
                if self.dx > 0:
                    self.dx -= 1
                if self.a == True:
                    self.rect.left -= self.dx
                elif self.a == False:
                    self.rect.left += self.dx
                
                

    class BulletSprite(pygame.sprite.Sprite):
        def __init__(self, startx, starty):
            pygame.sprite.Sprite.__init__(self)
            self.image = bulletPic
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            startx += 62
            starty -= 42
            self.rect.top = starty
            self.rect.left = startx
            self.dx = 2
            
        def update(self):
            global bulletsList
            self.dx *= 1.1
            if self.rect.top - self.dx > 0:
                self.rect.top -= self.dx
            else:
                self.kill()
                bulletsList.remove(self)

    
    class ExplodeSprite(pygame.sprite.Sprite):
        def __init__(self, start):
            pygame.sprite.Sprite.__init__(self)
            self.image = explodeSmallPic
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.center = start
            self.lifeSpan = 15
            
        def update(self):
            global explodeList
            self.lifeSpan -= 1
            if self.lifeSpan == 10:
                self.image = explodePic
                self.rect.top -= 20
                self.rect.left -= 15
            elif self.lifeSpan == 5:
                self.image = explodeSmallPic
                self.rect.top += 20
                self.rect.left += 15
            elif self.lifeSpan == 0:
                self.kill()
                explodeList.remove(self)

    class smallExplodeSprite(pygame.sprite.Sprite):
        def __init__(self, start):
            pygame.sprite.Sprite.__init__(self)
            self.image = explodeExtraSmallPic
            self.image.set_colorkey((0,0,0))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.center = start
            self.lifeSpan = 5
            
        def update(self):
            global explodeList
            self.lifeSpan -= 1
            if self.lifeSpan == 0:
                self.kill()
                explodeList.remove(self)

    
                
            
    def intro():
        title0 = pygame.image.load('TITLE_Kratos.gif')
        title = pygame.transform.scale(title0, (500, 500))
        scrn.blit(title, (775,500))
        pygame.display.update()
        time.sleep(3)
        scrn.blit(bg, (0,0))
        time.sleep(1)
        #test = pygame.font.Font('Invasion2000', 50)
        scrn.blit(direc, (300, 500))
        #openText = bigFont.render( 'Kill all enemies, avoid missiles.', False, (47,50,203))
        #Test = test.render( 'Kill all enemies, avoid missiles.', False, (47,50,203))
        #scrn.blit(openText, (200,500))
        pygame.display.update()
        time.sleep(5)
        pygame.display.update()
        time.sleep(.5)

    def levelDis():
        textWin = largeFont.render( 'LEVEL ' + str(level), False, (255,255,255))
        scrn.blit(textWin, (200,200))
        pygame.display.update()
        time.sleep(3)
        
    
    def main():
        global health
        global keyA
        global keyD
        count3 = 0
        keyA = False
        keyD = False
        mute = False
        pygame.display.set_caption('SPACE KRATOS. BY LUKE BARTINI')
        pygame.mixer.music.set_volume(.35)
        scrn.blit(bg, (0,0))
        textWin = 0
        bulletType = 1
        ships = []
        music.play()
        bullets = []
        explodes = []
        for _ in xrange(NUMSHIPS):
            ships.append(ShipSprite())
        for x in range(1,7):
            for y in range(1,3):
                enemy.append(EnemySprite(y*300,x*250))
        allSprites = pygame.sprite.Group(ships)
        EBulletsList = pygame.sprite.Group(ebullets)
        enemyList = pygame.sprite.Group(enemy)
        bulletsList = pygame.sprite.Group(bullets)
        explodeList = pygame.sprite.Group(explodes)
        keepGoing = True
        #Main game loop
        
        while keepGoing:
            explodes = []
            EBulletsList = pygame.sprite.Group(ebullets)
            keys = pygame.key.get_pressed()  #checking pressed keys
            if keys[pygame.K_LEFT]:
                keyA = True
                allSprites.update()
                keyA = False
            if keys[pygame.K_RIGHT]:
                keyD = True
                allSprites.update()
                keyD = False
            if keys[pygame.K_DOWN]:
                keyS = True
            mainClock.tick(30)

            for bullet in bulletsList:
                for enemy2 in enemyList:
                    if checkCollision(bullet,enemy2):
                        explode.play()
                        bullet.kill()
                        bullets.remove(bullet)
                        enemy2.kill()
                        enemyList.remove(enemy2)
                        explodes.append(ExplodeSprite(enemy2.rect.center))
                        explodeList = pygame.sprite.Group(explodes)
                        explodes = []
                        
            for bullet in EBulletsList:
                for you in allSprites:
                    if checkCollision(bullet,you):
                        health += 1
                        explode.play()
                        explodes.append(smallExplodeSprite(bullet.rect.center))
                        explodeList = pygame.sprite.Group(explodes)
                        if health > 10:
                            explode.play()
                            bullet.kill()
                            EBulletsList.remove(bullet)
                            you.kill()
                            allSprites.remove(you)
                            explodes.append(ExplodeSprite(you.rect.center))
                            explodeList = pygame.sprite.Group(explodes)
                            explodes = []
     
                        
            oldTime = time.time()
            for event in pygame.event.get():
                if event.type == QUIT:
                    keepGoing = False
                if event.type == KEYDOWN:
                    if event.key == 27: #27 is the escape key, you can also do K_ESC
                        keepGoing = False
                    if event.key == K_m: #this is the mute key ## CHEAT CODE ## ERASES WALLS SO YOU CAN HIDE ##
                        walls -= 4 #gets rid of walls
                        if mute == False:
                            pygame.mixer.music.set_volume(0)
                            mute = True
                        elif mute == True:
                            pygame.mixer.music.set_volume(.55)
                            mute = False
                    if event.key == K_c:
                        pass
                    if event.key == K_1:
                        bulletType = 1
                    if event.key == K_2:
                        if level > 1:
                            bulletType = 2
                    if event.key == K_3:
                        if level > 2:
                            bulletType = 3
                    if event.key == K_4:
                        if level > 3:
                            bulletType = 4
                    if event.key == K_UP:
                        if bulletType == 1:
                            if len(bulletsList) == 0:
                                swish.play()
                                bullets.append(BulletSprite(ships[0].rect.left,ships[0].rect.top))
                                bulletsList = pygame.sprite.Group(bullets)
    
                            
           
            
            scrn.blit(bg, (0, 0))
            
            
                
            EBulletsList.clear(scrn, bg)
            EBulletsList.update()
            EBulletsList.draw(scrn)
            
            allSprites.clear(scrn, bg)
            allSprites.update()
            allSprites.draw(scrn)

            enemyList.clear(scrn, bg)
            enemyList.update()
            enemyList.draw(scrn)

            explodeList.clear(scrn,bg)
            explodeList.update()
            explodeList.draw(scrn)
     
            bulletsList.clear(scrn,bg)
            bulletsList.update()
            bulletsList.draw(scrn)

            text = basicFont.render( 'HEALTH: ' + '* ' * (10 - health), False, (247,5,203))
            scrn.blit(text, (100,100))
            levelDis = basicFont.render( 'LEVEL: ' + str(level), False, (24,200,23))
            scrn.blit(levelDis, (700,100))
            
            
            
            
            if len(enemyList) == 0:
                levelLis = 1
                levelLis += 1
                levelDis0 = pygame.image.load('level2.png').convert_alpha()
                levelDis = pygame.transform.scale(levelDis0, (400, 100))
                #levelDis0 = pygame.image.scale2x(levelDis0)

                #textWin = largeFont.render( 'NEXT', False, (247,5,203))
                #game(level + 1)
                textWin2 = largeFont.render(str(levelLis), False, (255,255,255))
                scrn.blit(levelDis, (600,500))
                scrn.blit(textWin2, (650,700))
                pygame.display.update()
                time.sleep(3)
                scrn.blit(bg, (0,0))
                game(level + 1)

            if level >= 1:
                textType = basicFont.render( 'WEAPON TYPE: Missile', False, (255,0,0))
                scrn.blit(textType, (1500,100))

            pygame.display.update()

            if len(allSprites) == 0:
                lose.play()
                textWin = largeFont.render( 'YOU LOSE.', False, (255,255,255))
                scrn.blit(textWin, (125,200))
                pygame.display.update()
                time.sleep(3)
                scrn.blit(bg, (0,0))
                pygame.display.quit()
                return
            
            
    if level == 1:
        intro()
    else:
        levelDis()

    if __name__ == '__main__':
        main()
game(1)
