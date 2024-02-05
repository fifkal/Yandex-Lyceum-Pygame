import pygame
import sys
import os
from button import Button
import main
import runpy
cursor1 = pygame.image.load('Ai_Cursor_Open.png')

pygame.init()

width, height = 960, 600
lt = 0

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Menu')

fone = pygame.image.load('fone_images/new_menu_fone.jpg')
settings_fone = pygame.image.load('fone_images/setting_fone.png')
return_fone = pygame.image.load('fone_images/return_fone.jpg')
volume_fone = pygame.image.load('fone_images/volume_fone.png')
customize_fone = pygame.image.load('fone_images/customize_fone.jpg')
song = pygame.mixer.Sound('sound_effects/16-Bit Starter Pack/Various Themes/Origins.ogg')
click = pygame.mixer.Sound('sound_effects/mixkit-modern-technology-select-3124.wav')
level = pygame.image.load('fone_images/levels_fone.jpg')
level = pygame.transform.scale(level, (960, 600))
song.set_volume(0.5)
player_sprite = pygame.sprite.Group()
pygame.init()


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


player = AnimatedSprite(load_image('Enchantress/Idle.png'), 5, 1, 415, 210)
players = [{'idle': (load_image('Enchantress/Idle.png'), 5), 'step': (load_image('Enchantress/Walk.png'), 8),
            'step_left': (load_image('Enchantress/Walk_left.png'), 8), 'run': (load_image('Enchantress/Run.png'), 8),
            'run_left': (load_image('Enchantress/Run_left.png'), 8), 'jump': (load_image('Enchantress/Jump.png'), 8),
            'attack': (load_image('Enchantress/Attack_2.png'), 3),
            'attack_left': (load_image('Enchantress/Attack_2_left.png'), 3),
            'hurt': (load_image('Enchantress/Hurt.png'), 2)},
           {'idle': (load_image('Knight/Idle.png'), 6), 'step': (load_image('Knight/Walk.png'), 8),
            'step_left': (load_image('Knight/Walk_left.png'), 8), 'run': (load_image('Knight/Run.png'), 7),
            'run_left': (load_image('Knight/Run_left.png'), 7), 'jump': (load_image('Knight/Jump.png'), 6),
            'attack': (load_image('Knight/Attack_2.png'), 2),
            'attack_left': (load_image('Knight/Attack_2_left.png'), 2),
            'hurt': (load_image('Knight/Hurt.png'), 3)},
           {'idle': (load_image('Musketeer/Idle.png'), 5), 'step': (load_image('Musketeer/Walk.png'), 8),
            'step_left': (load_image('Musketeer/Walk_left.png'), 8), 'run': (load_image('Musketeer/Run.png'), 8),
            'run_left': (load_image('Musketeer/Run_left.png'), 8), 'jump': (load_image('Musketeer/Jump.png'), 7),
            'attack': (load_image('Musketeer/Attack_2.png'), 4),
            'attack_left': (load_image('Musketeer/Attack_2_left.png'), 4),
            'hurt': (load_image('Musketeer/Hurt.png'), 2)}
           ]
levelss = main.settings.y
now_level = []
last_cnt = 0
cnt = 0


def main_menu():
    global lt
    start_button = Button(width / 2 - (252 / 2), 150, 252, 74, '',
                          'buttons/Start/Start1.png', 'buttons/Start/Start4.png')
    settings_button = Button(width / 2 - (252 / 2), 250, 252, 74, '',
                             'buttons/Settings/Settings1.png', 'buttons/Settings/Settings4.png')
    customize_button = Button(width / 2 - (252 / 2), 350, 252, 74, '',
                              'buttons/Customize/Customize1.png',
                              'buttons/Customize/Customize4.png')
    exit_button = Button(width / 2 - (252 / 2), 450, 252, 74, '',
                         'buttons/Quit/Quit1.png', 'buttons/Quit/Quit4.png')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == settings_button:
                click.play()
                setting_menu()
            if event.type == pygame.USEREVENT and event.button == start_button:
                click.play()
                levels()
            if event.type == pygame.USEREVENT and event.button == exit_button:
                click.play()
                quit_menu()
            if event.type == pygame.USEREVENT and event.button == customize_button:
                click.play()
                customize()
            for btn in [start_button, settings_button, customize_button, exit_button]:
                btn.handle_event(event)
                btn.check_hover(pygame.mouse.get_pos())
        screen.blit(fone, (0, 0))
        font = pygame.font.Font('Pixelfraktur.ttf', 72)
        text_surface = font.render('Cloudborn', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width / 2, 100))
        screen.blit(text_surface, text_rect)
        for btn in [start_button, settings_button, customize_button, exit_button]:
            btn.draw(screen)
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_focused():
            screen.blit(cursor1, (pos[0], pos[1]))
        pygame.display.flip()


def setting_menu():
    volume_button = Button(width / 2 - (252 / 2), 150, 252, 74, '',
                           'buttons/Volume/Volume1.png', 'buttons/Volume/Volume4.png')

    escape_button = Button(width / 2 - (252 / 2), 250, 252, 74, '',
                           'buttons/Back/Back1.png', 'buttons/Back/Back4.png')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == escape_button:
                click.play()
                main_menu()
            if event.type == pygame.USEREVENT and event.button == volume_button:
                click.play()
                volume_menu()
            for btn in [volume_button, escape_button]:
                btn.handle_event(event)
                btn.check_hover(pygame.mouse.get_pos())
        screen.blit(settings_fone, (0, 0))
        font = pygame.font.Font('Pixelfraktur.ttf', 72)
        text_surface = font.render('Cloudborn', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width / 2, 100))
        screen.blit(text_surface, text_rect)
        for btn in [volume_button, escape_button]:
            btn.draw(screen)
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_focused():
            screen.blit(cursor1, (pos[0], pos[1]))
        pygame.display.flip()


def quit_menu():
    return_button = Button(width / 2 - (252 / 2), 150, 252, 74, '',
                           'buttons/Back/Back1.png', 'buttons/Back/Back4.png')

    escape_button = Button(width / 2 - (252 / 2), 250, 252, 74, '',
                           'buttons/Quit/Quit1.png', 'buttons/Quit/Quit4.png')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == escape_button:
                click.play()
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == return_button:
                click.play()
                main_menu()
            for btn in [return_button, escape_button]:
                btn.handle_event(event)
                btn.check_hover(pygame.mouse.get_pos())
        screen.blit(return_fone, (0, 0))
        font = pygame.font.Font('Pixelfraktur.ttf', 50)
        text_surface = font.render('Are you sure you want to quit?', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width / 2, 100))
        screen.blit(text_surface, text_rect)
        for btn in [return_button, escape_button]:
            btn.draw(screen)
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_focused():
            screen.blit(cursor1, (pos[0], pos[1]))
        pygame.display.flip()


def volume_menu():
    swipper_button = Button(width / 2 - (252 / 2), 150, 252, 74, '',
                            'buttons/Volume/Swiper/Swiper1.png')
    return_button = Button(width / 2 - (252 / 2), 250, 252, 74, '',
                           'buttons/Back/Back1.png', 'buttons/Back/Back4.png')
    slider = Button(width / 2 - (252 / 2), 150, 252, 74, '',
                    'buttons/Volume/Swiper/Swiper2.png')

    running = True
    sound = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == return_button:
                click.play()
                main_menu()
            if event.type == pygame.USEREVENT and event.button == swipper_button:
                sound = True
            if event.type == pygame.MOUSEBUTTONUP:
                sound = False
            for btn in [swipper_button, return_button, slider]:
                btn.handle_event(event)
                btn.check_hover(pygame.mouse.get_pos())
        screen.blit(volume_fone, (0, 0))
        font = pygame.font.Font('Pixelfraktur.ttf', 72)
        text_surface = font.render('Cloudborn', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width / 2, 100))
        screen.blit(text_surface, text_rect)
        if sound:
            slider.move_slider(pygame.mouse.get_pos())
        for btn in [swipper_button, return_button, slider]:
            btn.draw(screen)
        song.set_volume((slider.rect.centerx - (width / 2 - (252 / 2))) / swipper_button.width)
        pygame.display.flip()


def customize():
    global cnt, player, player_sprite, last_cnt
    swipper_button = Button(200, 250, 100, 100, '',
                            'buttons/LeftKey/LeftKey1.png', 'buttons/LeftKey/LeftKey4.png')
    swipper1_button = Button(660, 250, 100, 100, '',
                             'buttons/RightKey/RightKey1.png', 'buttons/RightKey/RightKey4.png')
    return_button = Button(width / 2 - (252 / 2), 450, 252, 74, '',
                           'buttons/Back/Back1.png', 'buttons/Back/Back4.png')
    running = True
    sound = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == return_button:
                click.play()
                main_menu()
            if event.type == pygame.USEREVENT and event.button == swipper1_button:
                click.play()
                cnt += 1
            if event.type == pygame.USEREVENT and event.button == swipper_button:
                click.play()
                cnt -= 1
            for btn in [swipper_button, return_button, swipper1_button]:
                btn.handle_event(event)
                btn.check_hover(pygame.mouse.get_pos())
        screen.blit(customize_fone, (0, 0))
        font = pygame.font.Font('Pixelfraktur.ttf', 72)
        text_surface = font.render('Cloudborn', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width / 2, 100))
        screen.blit(text_surface, text_rect)
        for btn in [swipper_button, return_button, swipper1_button]:
            btn.draw(screen)
        if last_cnt != cnt:
            if cnt % 3 == 0:
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Idle.png'), 5, 1, 415, 210)
            if cnt % 3 == 1:
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Knight/Idle.png'), 6, 1, 415, 210)
            if cnt % 3 == 2:
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Musketeer/Idle.png'), 5, 1, 415, 210)
            last_cnt = cnt
        player_sprite.draw(screen)
        player.update_frame()
        pygame.display.flip()
        clock.tick(10)


def levels():
    global levelss, now_level
    level_1 = Button(width / 2 - (252 / 2) - 40, 150, 74, 74, '',
                            'buttons/Numbers/1.png')
    level_2 = Button(width / 2 - 40, 150, 74, 74, '',
                     'buttons/Numbers/2.png')
    level_3 = Button(width / 2 + (252 / 2) - 40, 150, 74, 74, '',
                     'buttons/Numbers/3.png')

    return_button = Button(width / 2 - (252 / 2), 250, 252, 74, '',
                           'buttons/Back/Back1.png', 'buttons/Back/Back4.png')

    running = True
    sound = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == return_button:
                click.play()
                main_menu()
            if event.type == pygame.USEREVENT and event.button == level_1:
                click.play()
                main.settings.choise = main.settings.player[cnt % 3]
                main.settings.level = main.settings.y[0]
                pygame.quit()
                runpy.run_module(mod_name="player")
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == level_2:
                main.settings.level = main.settings.y[1]
                main.settings.choise = main.settings.player[cnt % 3]
                click.play()
                pygame.quit()
                runpy.run_module(mod_name="player")
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == level_3:
                main.settings.level = main.settings.y[2]
                main.settings.choise = main.settings.player[cnt % 3]
                click.play()
                pygame.quit()
                runpy.run_module(mod_name="player")
                sys.exit()
            for btn in [level_1, level_2, level_3, return_button]:
                btn.handle_event(event)
                btn.check_hover(pygame.mouse.get_pos())
        screen.blit(level, (0, 0))
        font = pygame.font.Font('Pixelfraktur.ttf', 72)
        text_surface = font.render('Cloudborn', True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(width / 2, 100))
        screen.blit(text_surface, text_rect)
        for btn in [level_1, level_2, level_3, return_button]:
            btn.draw(screen)
        pygame.display.flip()


song.play(-1)
song.set_volume(0.1)
main_menu()
