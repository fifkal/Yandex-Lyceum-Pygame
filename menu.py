import pygame
import sys
pygame.init()
from button import Button
width, height = 960, 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Menu')
fone = pygame.image.load('fone_images/menu_fone.png')


def main_menu():
    start_button = Button(width / 2 - (252 / 2), 150, 252, 74, '',
                          'buttons/Start/Start1.png', 'buttons/Start/Start4.png')
    settings_button = Button(width / 2 - (252 / 2), 250, 252, 74, '',
                             'buttons/Start/Start1.png', 'buttons/Start/Start4.png')
    exit_button = Button(width / 2 - (252 / 2), 350, 252, 74, '',
                         'buttons/Start/Start1.png', 'buttons/Start/Start4.png')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            for btn in [start_button, settings_button, exit_button]:
                btn.handle_event(event)
        screen.blit(fone, (0, 0))