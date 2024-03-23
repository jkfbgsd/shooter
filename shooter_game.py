import pygame
from random import randint

pygame.init()
window = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load('space.ogg')
sound_file = pygame.mixer.Sound('fire.ogg')

class Sprite(pygame.sprite.Sprite):
    def __init__(self, path, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Player(Sprite):
    def __init__(self, path, x, y, width, height):
        super().__init__(path, x, y, width, height)
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
    
    def update(self):
        global state
        hits = pygame.sprite.spritecollide(self, enemies, True)
        if hits:
            state = 'loose'
        hits = pygame.sprite.spritecollide(self, comets, True)
        if hits:
            state = 'loose'

class Enemy(Sprite):
    """Описание класса"""
    def __init__(self, path, x, y, width, height, speed):
        super().__init__(path, x, y, width, height)
        self.speed = speed
    
    def update(self):
        global points, missed
        self.rect.y += self.speed
        if self.rect.top > 500:
            missed += 1
            self.rect.bottom = 0
            self.rect.centerx = randint(0, 700)
        hits = pygame.sprite.spritecollide(self, bullets, True)
        if hits:
            points += 1
            self.rect.x, self.rect.y = randint(0, 500), randint(-400, -50)
            for bullet in hits:
                bullet.kill()

class Comet(Sprite):
    def __init__(self, path, x, y, width, height, speed):
        super().__init__(path, x, y, width, height)
        self.speed = speed
    
    def update(self):
        global points, missed
        self.rect.y += self.speed
        if self.rect.top > 500:
            missed += 1
            self.rect.bottom = 0
            self.rect.centerx = randint(0, 700)

class Bullet(Sprite):
    def __init__(self, path, x, y, width, height):
        super().__init__(path, x, y, width, height)
        self.speed = 7
        

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

font = pygame.font.SysFont('comicsans', 30, True)
points = 0
missed = 0
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
comets = pygame.sprite.Group()

# определение уровня и скорости врагов
level = 1
enemy_speed = 2
comet_speed = 1

# функция для создания врагов и комет базированных на текущем уровне
def create_enemies_and_comets(level):
    for i in range(level * 3):
        enemy = Enemy('ufo.png', 100 * i, randint(-400, -50), 50, 50, enemy_speed)
        enemies.add(enemy)
        comet = Comet('asteroid.png', 100 * i + 50, randint(-400, -50), 50, 50, comet_speed)
        comets.add(comet)

bg = Sprite('galaxy.jpg', 0, 0, 700, 500)
rocket = Player('rocket.png', 325, 400, 50, 70)
cooldown = 0 
state = 'menu'
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if state == 'menu':
                if event.key == pygame.K_RETURN:
                    state = 'game'
                    create_enemies_and_comets(level)
            elif state == 'game':
                if event.key == pygame.K_SPACE and cooldown == 0:
                    bullet = Bullet('bullet.png', rocket.rect.x + 20, rocket.rect.y, 5, 10)
                    bullets.add(bullet)
                    sound_file.play()
                    cooldown = 30

    if cooldown > 0:
        cooldown -= 1

    bg.draw(window)
    text_img = font.render(f'Очков: {points}', True, (255, 255, 255))
    window.blit(text_img, (10, 10))
    text_img2 = font.render(f'Пропущенных: {missed}', True, (255, 255, 255))
    window.blit(text_img2, (420, 10))
    enemies.draw(window)
    comets.draw(window)
    bullets.draw(window)
    rocket.draw(window)
    
    if points == level * 10:  # следующий уровень каждые 10 поинтов
        if level == 5:  # при достижении 5 уровня выводит надпись вин
            state = 'win'
        else:  # давай на другой уровень
            level += 1
            enemy_speed += 1  # Ускоряет врагов с каждым уровнем
            comet_speed += 0.5  # Ускоряет кометы с каждым уровнем
            state = 'menu'
    
    if missed == 15:
        state = 'loose'
    if state == 'win':
        text_img = font.render('Win', True, (0, 255, 0))
        window.blit(text_img, (325, 250))
    if state == 'loose':
        text_img = font.render('GAME OVER', True, (255, 0, 0))
        window.blit(text_img, (300, 250))
    if state == 'menu':
        text_img = font.render('Press ENTER to start the level', True, (255, 255, 255))
        window.blit(text_img, (220, 250))
    if state == 'game':
        rocket.update()
        enemies.update()
        comets.update()
        bullets.update()
        rocket.move()       
    pygame.display.update()
    clock.tick(60)         #фэпс

    