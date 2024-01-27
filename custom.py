from menu import load_image, cnt
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
res = players[cnt % 3]
print(res)