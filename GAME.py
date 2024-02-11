import pygame
import random
import os
FPS=60
BLACK=(0,0,0)
WHITE=(255,255,255)
GREEN=(0,225,0)
RED=(255,0,0)
YELLOW=(255,255,0)
WIDTH=500
HEIGHT=600
pygame.init()
pygame.mixer.init()
#self.image 物體
#self.rect  物體座標
screen=pygame.display.set_mode((WIDTH,HEIGHT))#創造畫面
pygame.display.set_caption("MY FIRST GAME")
clock=pygame.time.Clock() 
#載入圖片
background_img=pygame.image.load(os.path.join("img","background.png")).convert()
player_img=pygame.image.load(os.path.join("img","player.png")).convert()
bullet_img=pygame.image.load(os.path.join("img","bullet.png")).convert()
#rock_img=pygame.image.load(os.path.join("img","rock.png")).convert()
rock_imgs=[]
for i in range(7):
    rock_imgs.append(pygame.image.load (os.path.join("img",f"rock{i}.png")).convert())
shoot_sound=pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
font_name = pygame.font.match_font("arial")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
class Player(pygame.sprite.Sprite):#設定飛船的設定
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(player_img,(80,65))
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.radius=24
        self.rect.centerx=WIDTH/2#起始位置(X)
        self.rect.bottom=HEIGHT-10#起始位置(Y)
        self.speedx=7#速度
    def update(self):#每秒跟新的畫面
        
        key_pressed=pygame.key.get_pressed()#操控盤
        if key_pressed[pygame.K_a]:
            self.rect.x-=self.speedx 
        if key_pressed[pygame.K_d]:
            self.rect.x+=self.speedx
        
        if self.rect.right>WIDTH:
            self.rect.right=WIDTH
        if self.rect.right<0:
            self.rect.right=0
    def shoot(self):
        bullet= Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()
class Rock(pygame.sprite.Sprite):#設定石頭的設定
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori=random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image=self.image_ori.copy()
        self.rect=self.image.get_rect()
        self.radius=int(self.rect.width*0.85/2)
        self.rect.x=random.randrange(0, WIDTH - self.rect.width)#石頭隨機起始位置(X)
        self.rect.y=random.randrange(-180,-100)#起始位置(Y)
        self.speedy=random.randrange(4,13) #石頭掉下來的速度
        self.speedx=random.randrange(-3,3)
        self.total_degree=0
        self.rot_degree=random.randrange(-3,3)

    def rotate(self):
        self.total_degree+=self.rot_degree
        self.total_degree=self.total_degree%360
        self.image=pygame.transform.rotate(self.image_ori,self.total_degree)
        center=self.rect.center
        self.rect=self.image.get_rect()
        self.rect.center=center
    def update(self):#每秒跟新的畫面
        self.rotate()
        self.rect.y+=self.speedy 
        self.rect.x+=self.speedx   
        if self.rect.top>HEIGHT or self.rect.left>WIDTH or self.rect.right>WIDTH:
            self.rect.x=random.randrange(0, WIDTH - self.rect.width)#石頭隨機起始位置(X)
            self.rect.y=random.randrange(-100,-40)#起始位置(Y)
            self.speedy=random.randrange(2,10)#石頭掉下來的速度
            self.speedx=random.randrange(-3,3)    
class Bullet(pygame.sprite.Sprite):#設定石頭的設定
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=bullet_img
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.rect.centerx=x#子彈位置(X)
        self.rect.bottom=y#子彈位置(Y)
        self.speedy=-10
    def update(self):#每秒跟新的畫面
        self.rect.y+=self.speedy 
        if self.rect.bottom<0:
            self.kill()   

all_sprites=pygame.sprite.Group()
rocks=pygame.sprite.Group()
bullets=pygame.sprite.Group()
player=Player()
all_sprites.add(player)
for i in range(8):
    rock=Rock()
    all_sprites.add(rock)
    rocks.add(rock)


score=0
running=True
while running:#遊戲迴圈
    clock.tick(FPS)
    for event in pygame.event.get():#輸入
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                player.shoot()
    
    all_sprites.update()#畫面的更新
    hits=pygame.sprite.groupcollide(rocks,bullets,True,True)
    for hit in hits:
        score+=hit.radius
        r=Rock()
        all_sprites.add(r)
        rocks.add(r)

    hits=pygame.sprite.spritecollide(player,rocks,False,pygame.sprite.collide_circle)
    if hits:
        running=False
    screen.fill(BLACK)#畫面
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    draw_text(screen,str(score),18,WIDTH/2,10)
    pygame.display.update()
pygame.quit()