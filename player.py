import pygame
import os
import sys
import pygame.gfxdraw
from button import Button
import runpy


player_sprite = pygame.sprite.Group()
enemy_sprite = pygame.sprite.Group()
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
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def pause_menu():
    global pause, screen, running
    start_button = Button(width / 2 - (252 / 2), 150, 252, 74, '',
                          'buttons/Resume/Resume1.png', 'buttons/Resume/Resume4.png')
    settings_button = Button(width / 2 - (252 / 2), 250, 252, 74, '',
                             'buttons/Settings/Settings1.png', 'buttons/Settings/Settings4.png')
    exit_button = Button(width / 2 - (252 / 2), 350, 252, 74, '',
                         'buttons/Main Menu/Main Menu1.png', 'buttons/Main Menu/Main Menu4.png')
    running1 = True
    while running1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running1 = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == start_button:
                running1 = False
                pause = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running1 = False
                pause = False
            if event.type == pygame.USEREVENT and event.button == exit_button:
                pygame.quit()
                runpy.run_path(path_name='menu.py')
                sys.exit()
            for btn in [start_button, settings_button, exit_button]:
                btn.handle_event(event)
                btn.check_hover(pygame.mouse.get_pos())
        s = pygame.Surface((800, 800))  # the size of your rect
        s.set_alpha(3)  # alpha level
        s.fill((220, 220, 220))  # this fills the entire surface
        screen.blit(s, (0, 0))
        font = pygame.font.Font('Pixelfraktur.ttf', 72)
        text_surface = font.render('Cloudborn', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width / 2, 100))
        screen.blit(text_surface, text_rect)
        for btn in [start_button, settings_button, exit_button]:
            btn.draw(screen)
        pygame.display.flip()


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
        self.health = 100
        self.last_x = self.rect.x
        self.last_y = self.rect.y
        self.now_move = now_move
        self.last_move = now_move
        self.last_direction = 'right'
        self.change = False
        self.attack = False
        self.cld = False

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
        elif self.rect.x == self.last_x and self.rect.y == self.last_y: # and not self.rct.colliderect(enemy.rct):
            self.now_move = 'idle'
        #elif (self.rct.colliderect(enemy.rct) and
              #self.rect.x == self.last_x and self.rect.y == self.last_y):
            #self.now_move = 'hurt'
            #self.health -= 0.25

    def check(self):
        if self.last_move != self.now_move:
            self.change = True

    def collid(self):
        global is_jump, jump
        flag = False
        for p in platforms:
            if self.rect.colliderect(p.rect) and is_jump and jump < 0:
                is_jump = False
                jump = -jump
                self.now_move = 'idle'
                self.cld = True


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + width / 2, -t + height / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-width), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-height), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)


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
        elif (player.rct.colliderect(self.rct) and player.rect.x >= self.rect.x and
                player.now_move not in ['attack', 'attack_left']):
            self.now_move = 'attack'
        elif (player.rct.colliderect(self.rct) and player.rect.x <= self.rect.x and
                player.now_move not in ['attack', 'attack_left']):
            self.now_move = 'attack_left'
        #elif self.rct.colliderect(enemy.rct) and player.now_move in ['attack', 'attack_left']:
            #self.now_move = 'hurt'
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
        self.rect = pygame.Rect(x1, y1, width, height)


running = True
is_jump = False
air = False
jump = 10
gravitation = 0.35
y_ground = 550
last_jump = 0
plat_check = False
ret = 0
now_step = 0
platform = Platform(400, 630, 100, 50)
player = Player(load_image('Enchantress/Idle.png'), 5, 1, 300, 550, 'idle')
# enemy = Enemy(load_image('Skeleton/Idle.png'), 7, 1, 100, 550, 'idle')
moves = {'idle': (load_image('Enchantress/Idle.png'), 5), 'step': (load_image('Enchantress/Walk.png'), 8),
         'step_left': (load_image('Enchantress/Walk_left.png'), 8), 'run': (load_image('Enchantress/Run.png'), 8),
         'run_left': (load_image('Enchantress/Run_left.png'), 8), 'jump': (load_image('Enchantress/Jump.png'), 8),
         'attack': (load_image('Enchantress/Attack_2.png'), 3),
         'attack_left': (load_image('Enchantress/Attack_2_left.png'), 3),
         'hurt': (load_image('Enchantress/Hurt.png'), 2)}
moves_enemy = {'idle': (load_image('Skeleton/Idle.png'), 7), 'walk': (load_image('Skeleton/Walk.png'), 8),
               'walk_left': (load_image('Skeleton/Walk_left.png'), 8),
               'attack': (load_image('Skeleton/Attack_2.png'), 4),
               'attack_left': (load_image('Skeleton/Attack_2_left.png'), 4),
               'hurt': (load_image('Skeleton/Hurt.png'), 3)}
pause = False
total_level_width = 400  # Высчитываем фактическую ширину уровня
total_level_height = 400  # высоту

camera = Camera(camera_configure, total_level_width, total_level_height)
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
            if event.key == pygame.K_ESCAPE and not pause:
                pause = True
            elif event.key == pygame.K_ESCAPE and pause:
                pause = False
        if event.type == pygame.MOUSEBUTTONUP and not pause:
            player.attack = False
    if not pause:
        if is_jump:
            player.rect.y -= jump
            if player.rect.y >= y_ground:
                is_jump = False
                air = False
                jump = 10
                player.last_y = player.rect.y
            else:
                jump -= gravitation
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
        elif ((all_keys[pygame.K_d] and all_keys[pygame.K_a]) or (not all_keys[pygame.K_d]) and
              (not all_keys[pygame.K_d])):
            now_step = 0
        screen.blit(fone, (0, 0))
        rct = pygame.Rect(player.rect.x + 30, player.rect.y + 25, player.rect.w - 60, player.rect.h - 15)
        player.update_frame()
        #enemy.update_frame()
        player.control(now_step, player.movey)
        player.nova_move()
        player.collid()
        player.check()
        #enemy.check()
        player_sprite.draw(screen)
        platforms.draw(screen)
        camera.update(player)
        pygame.draw.rect(screen, pygame.Color('red'), player.rct, 5)
        pygame.draw.rect(screen, pygame.Color('red'), platform.rect, 5)

        if player.change:
            now = player.now_move
            x, y = player.rect.x, player.rect.y
            nd = player.last_direction
            lh = player.health
            player_sprite.remove(player)
            player = Player(moves[now][0], moves[now][1], 1, x, y, now)
            player.last_direction = nd
            player.health = lh
        #if enemy.change:
            #now = enemy.now_move
            #x, y = enemy.rect.x, enemy.rect.y
            #player_sprite.remove(enemy)
            #enemy = Enemy(moves_enemy[now][0], moves_enemy[now][1], 1, x, y, now)
        #enemy.updatee()
        pygame.display.flip()
        clock.tick(20)
    else:
        pause_menu()
