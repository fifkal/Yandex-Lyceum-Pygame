import pygame
import sys
import runpy
from button import Button
pygame.mouse.set_visible(False)
cursor1 = pygame.image.load('Ai_Cursor_Open.png')


pygame.init()

width, height = 960, 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Menu')
fone = pygame.image.load('fone_images/new_menu_fone.jpg')
settings_fone = pygame.image.load('fone_images/setting_fone.png')
song = pygame.mixer.Sound('sound_effects/16-Bit Starter Pack/Various Themes/Origins.ogg')
pygame.init()


def main_menu():
    global song
    start_button = Button(width / 2 - (252 / 2), 150, 252, 74, '',
                          'buttons/Start/Start1.png', 'buttons/Start/Start4.png')
    settings_button = Button(width / 2 - (252 / 2), 250, 252, 74, '',
                             'buttons/Settings/Settings1.png', 'buttons/Settings/Settings4.png')
    exit_button = Button(width / 2 - (252 / 2), 350, 252, 74, '',
                         'buttons/Quit/Quit1.png', 'buttons/Quit/Quit4.png')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == settings_button:
                setting_menu()
            if event.type == pygame.USEREVENT and event.button == start_button:
                pygame.quit()
                runpy.run_path(path_name='main.py')
                sys.exit()
            for btn in [start_button, settings_button, exit_button]:
                btn.handle_event(event)
                btn.check_hover(pygame.mouse.get_pos())
        screen.blit(fone, (0, 0))
        font = pygame.font.Font('Pixelfraktur.ttf', 72)
        text_surface = font.render('Cloudborn', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width / 2, 100))
        screen.blit(text_surface, text_rect)
        for btn in [start_button, settings_button, exit_button]:
            btn.draw(screen)
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_focused():
            screen.blit(cursor1, (pos[0], pos[1]))
        pygame.display.flip()


def setting_menu():
    volume_button = Button(width / 2 - (252 / 2), 150, 252, 74, '',
                          'buttons/Volume/Volume1.png', 'buttons/Volume/Volume4.png')

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
                main_menu()
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


if __name__ == '__main__':
    song.play(-1)
    main_menu()
