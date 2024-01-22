import pygame
import os
import sys


player_sprite = pygame.sprite.Group()
enemy_sprite = pygame.sprite.Group()
ani = 4
steps = 10
pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 10

sword_sound = pygame.mixer.Sound('sound_effects/sword_sound (mp3cut.net) (2).mp3')
ON_SIGHT = pygame.mixer.Sound('sound_effects/16-Bit Starter Pack/Overworld/Long Road Ahead.ogg')
jump_sound = pygame.mixer.Sound('sound_effects/free-sound-1674743518 (mp3cut.net).mp3')
fone = pygame.image.load('fone_images/fone.png', )


def load_image(name, color_key=None):  # загрузка изображений
    fullname = os.path.join('player_sprites', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class AnimatedSprite(pygame.sprite.Sprite):  # создание спрайтов
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(player_sprite)
        self.sheet = sheet
        self.frames = []
        self.cut_sheet(self.sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.x, self.y = x, y
        self.rect = self.rect.move(self.x, self.y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update_frame(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Player(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y, now_move):
        AnimatedSprite.__init__(self, sheet, columns, rows, x, y)
        self.rct = pygame.Rect(self.rect.x + 30, self.rect.y + 55, self.rect.w - 60, self.rect.h - 50)
        self.sheet = sheet
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.health = 10
        self.last_x = self.rect.x
        self.last_y = self.rect.y
        self.now_move = now_move
        self.last_move = now_move
        self.last_direction = 'right'
        self.change = False
        self.attack = False

    def control(self, x, y):
        self.movex = x
        self.movey = y
        self.last_x = self.rect.x
        self.rect.x += self.movex
        self.rct = pygame.Rect(self.rect.x + 30, self.rect.y + 55, self.rect.w - 60, self.rect.h - 50)

    def nova_move(self):
        if self.rect.y != self.last_y:
            self.now_move = 'jump'
            self.attack = False
        elif self.attack and self.last_direction == 'right':
            self.now_move = 'attack'
        elif self.attack and self.last_direction == 'left':
            self.now_move = 'attack_left'
        elif self.rect.x == self.last_x - 10:
            self.now_move = 'step_left'
        elif self.rect.x == self.last_x + 10:
            self.now_move = 'step'
        elif self.rect.x == self.last_x - 20:
            self.now_move = 'run_left'
        elif self.rect.x == self.last_x + 20:
            self.now_move = 'run'
        elif self.rect.x == self.last_x and self.rect.y == self.last_y:
            self.now_move = 'idle'

    def check(self):
        if self.last_move != self.now_move:
            self.change = True


class Enemy(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y, now_move):
        super().__init__(sheet, columns, rows, x, y)
        self.rct = pygame.Rect(self.rect.x + 30, self.rect.y + 55, self.rect.w - 60, self.rect.h - 50)
        self.sheet = sheet
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.health = 10
        self.last_x = self.rect.x
        self.last_y = self.rect.y
        self.now_move = now_move
        self.last_move = now_move
        self.last_direction = 'idle'
        self.change = False
        self.attack = False

    def updatee(self):
        if player.rect.x < self.rect.x and not player.rct.colliderect(self.rct):
            self.last_direction = 'left'
            self.now_move = 'walk_left'
            self.rect.x -= 5
        elif player.rect.x > self.rect.x and not player.rct.colliderect(self.rct):
            self.last_direction = 'right'
            self.now_move = 'walk'
            self.rect.x += 5
        else:
            self.now_move = 'idle'
        self.rct = pygame.Rect(self.rect.x + 30, self.rect.y + 55, self.rect.w - 60, self.rect.h - 50)

    def check(self):
        if self.last_move != self.now_move:
            self.change = True


platforms = pygame.sprite.Group()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x1, y1, width, height):
        super().__init__(platforms)
        self.image = load_image('box.png')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x1, y1, 50, 50)


running = True
is_jump = False
air = False
jump = 50
y_ground = 550
last_jump = 0
plat_check = False
ret = 0
now_step = 0
platform = Platform(400, 630, 50, 50)
player = Player(load_image('Enchantress/Idle.png'), 5, 1, 100, 550, 'idle')
enemy = Enemy(load_image('Skeleton/Idle.png'), 7, 1, 100, 550, 'idle')
moves = {'idle': (load_image('Enchantress/Idle.png'), 5), 'step': (load_image('Enchantress/Walk.png'), 8),
         'step_left': (load_image('Enchantress/Walk_left.png'), 8), 'run': (load_image('Enchantress/Run.png'), 8),
         'run_left': (load_image('Enchantress/Run_left.png'), 8), 'jump': (load_image('Enchantress/Jump.png'), 8),
         'attack': (load_image('Enchantress/Attack_2.png'), 3),
         'attack_left': (load_image('Enchantress/Attack_2_left.png'), 3)}
moves_enemy = {'idle': (load_image('Skeleton/Idle.png'), 7), 'walk': (load_image('Skeleton/Walk.png'), 8),
               'walk_left': (load_image('Skeleton/Walk_left.png'), 8)}
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                main = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_jump = True

    player.nova_move()
    if is_jump:
        player.rect.y -= jump
        jump -= 10
        if player.rect.y >= y_ground:
            is_jump = False
            air = True
            jump = 50
            player.last_y = player.rect.y
    all_keys = pygame.key.get_pressed()
    if all_keys[pygame.K_SPACE] and not is_jump:
        is_jump = True
    if pygame.mouse.get_pressed()[0]:
        player.attack = True
    else:
        player.attack = False
    if all_keys[pygame.K_a] and not all_keys[pygame.K_d] and not all_keys[pygame.K_LSHIFT]:
        now_step = -steps
        player.last_direction = 'left'
    elif all_keys[pygame.K_d] and not all_keys[pygame.K_a] and not all_keys[pygame.K_LSHIFT]:
        now_step = steps
        player.last_direction = 'right'
    elif all_keys[pygame.K_d] and not all_keys[pygame.K_a] and all_keys[pygame.K_LSHIFT]:
        now_step = steps * 2
        player.last_direction = 'right'
    elif all_keys[pygame.K_a] and not all_keys[pygame.K_d] and all_keys[pygame.K_LSHIFT]:
        now_step = -(steps * 2)
        player.last_direction = 'left'
    elif (all_keys[pygame.K_d] and all_keys[pygame.K_a]) or (not all_keys[pygame.K_d]) and (not all_keys[pygame.K_d]):
        now_step = 0
    screen.blit(fone, (0, 0))
    rct = pygame.Rect(player.rect.x + 30, player.rect.y + 25, player.rect.w - 60, player.rect.h - 15)
    player.update_frame()
    enemy.update_frame()
    player.control(now_step, 0)
    player.nova_move()
    player.check()
    enemy.check()
    player_sprite.draw(screen)
    platforms.draw(screen)
    if player.change:
        now = player.now_move
        x, y = player.rect.x, player.rect.y
        nd = player.last_direction
        player_sprite.remove(player)
        player = Player(moves[now][0], moves[now][1], 1, x, y, now)
        player.last_direction = nd
    if enemy.change:
        now = enemy.now_move
        x, y = enemy.rect.x, enemy.rect.y
        player_sprite.remove(enemy)
        enemy = Enemy(moves_enemy[now][0], moves_enemy[now][1], 1, x, y, now)
    enemy.updatee()
    pygame.display.flip()

    clock.tick(20)
