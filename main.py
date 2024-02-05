import pygame
import os

screen = pygame.display.set_mode((960, 600))


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


class Settings:
    def __init__(self):
        self.y = [[x for x in open('levels/level1')],
                  [x for x in open('levels/level2')],
                  [x for x in open('levels/level3')]]
        self.level = self.y[0]
        self.player = [{'idle': (load_image('Enchantress/Idle.png'), 5), 'step': (load_image('Enchantress/Walk.png'), 8),
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
        self.choise = self.player[0]


settings = Settings()
