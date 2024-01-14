import pygame
import sys
from button import Button


pygame.init()

width, height = 960, 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Menu')
fone = pygame.image.load('fone_images/new_menu_fone.jpg')
song = pygame.mixer.Sound('sound_effects/16-Bit Starter Pack/Various Themes/Origins.ogg')
pygame.init()


def main_menu():
    start_button = Button(width / 2 - (252 / 2), 150, 252, 74, '',
                          'buttons/Start/Start1.png', 'buttons/Start/Start4.png')
    settings_button = Button(width / 2 - (252 / 2), 250, 252, 74, '',
                             'buttons/Settings/Settings1.png', 'buttons/Settings/Settings4.png')
    exit_button = Button(width / 2 - (252 / 2), 350, 252, 74, '',
                         'buttons/Quit/Quit1.png', 'buttons/Quit/Quit4.png')
    song.play(-1)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
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
        pygame.display.flip()


if __name__ == '__main__':
    main_menu()
