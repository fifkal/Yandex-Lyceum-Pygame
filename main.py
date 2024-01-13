import pygame
import os

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
player_sprite = pygame.sprite.Group()


def load_image(name, color_key=None):  # загрузка изображений
    fullname = os.path.join('Enchantress', name)
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
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
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

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)


clock = pygame.time.Clock()
player = AnimatedSprite(load_image('Idle.png'), 5, 1, 100, 550)
running = True
is_jump = False
jump = 20
air = False
attack = False
death = -1
last_direction = 'RIGHT'
fone = pygame.image.load('fone.png',)

motion = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:  # проверка нажатия клавиш: клавиши A, D == влево и вправо соответственно,
            # при нажатии пробела - прыжок, а с зажатым шифтом - бег
            all_keys = pygame.key.get_pressed()
            if all_keys[pygame.K_SPACE] and not all_keys[pygame.K_d] and not all_keys[pygame.K_a]:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Jump.png'), 8, 1, x, y)
                is_jump = True
            if all_keys[pygame.K_d] and all_keys[pygame.K_a]:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Hurt.png'), 2, 1, x, y)

            if all_keys[pygame.K_d] and not all_keys[pygame.K_a] and not all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Walk.png'), 8, 1, x, y)
            elif all_keys[pygame.K_a] and not all_keys[pygame.K_d] and not all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Walk_left.png'), 8, 1, x, y)
            elif all_keys[pygame.K_a] and not all_keys[pygame.K_d] and all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Run_left.png'), 8, 1, x, y)
            elif all_keys[pygame.K_d] and not all_keys[pygame.K_a] and all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Run.png'), 8, 1, x, y)
        if event.type == pygame.KEYUP:
            # проверка отпускания клавиши на переход на другую подходящую анимацию
            all_keys = pygame.key.get_pressed()
            if not all_keys[pygame.K_d] and not all_keys[pygame.K_a] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Idle.png'), 5, 1, x, y)
            elif all_keys[pygame.K_d] and not all_keys[pygame.K_a] and not all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Walk.png'), 8, 1, x, y)
            elif all_keys[pygame.K_a] and not all_keys[pygame.K_d] and not all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Walk_left.png'), 8, 1, x, y)
            elif all_keys[pygame.K_a] and not all_keys[pygame.K_d] and all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Run_left.png'), 8, 1, x, y)
            elif all_keys[pygame.K_d] and not all_keys[pygame.K_a] and all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Run.png'), 8, 1, x, y)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # то же самое, что и с клавишами, но уже для нажатия мыши (атака, будет ещё подобие некой ульты, но сделаю
            # потом
            if event.button == 1 and last_direction == 'RIGHT':
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Attack_2.png'), 3, 1, x, y)
            elif event.button == 1 and last_direction == 'LEFT':
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Attack_2_left.png'), 3, 1, x, y)
        if event.type == pygame.MOUSEBUTTONUP:
            all_keys = pygame.key.get_pressed()
            if not all_keys[pygame.K_d] and not all_keys[pygame.K_a] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Idle.png'), 5, 1, x, y)
            elif all_keys[pygame.K_d] and not all_keys[pygame.K_a] and not all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Walk.png'), 8, 1, x, y)
            elif all_keys[pygame.K_a] and not all_keys[pygame.K_d] and not all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Walk_left.png'), 8, 1, x, y)
            elif all_keys[pygame.K_a] and not all_keys[pygame.K_d] and all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Run_left.png'), 8, 1, x, y)
            elif all_keys[pygame.K_d] and not all_keys[pygame.K_a] and all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Run.png'), 8, 1, x, y)
    screen.blit(fone, (0, 0))
    player_sprite.update()
    player_sprite.draw(screen)
    pygame.display.flip()
    all_keys = pygame.key.get_pressed()

    if all_keys[pygame.K_SPACE] and not is_jump:
        x, y = player.rect.x, player.rect.y
        player_sprite.remove(player)
        player = AnimatedSprite(load_image('Jump.png'), 8, 1, x, y)
        is_jump = True
    # создание гравитации
    if is_jump:
        player.rect.y -= jump
        jump -= 5
        if jump <= -20:
            is_jump = False
            jump = 20
            player.rect.y += 20
            air = True
    # переход на другую анимацию при приземлении персонажа
    if air and not all_keys[pygame.K_d] and not all_keys[pygame.K_a]:
        x, y = player.rect.x, player.rect.y
        player_sprite.remove(player)
        player = AnimatedSprite(load_image('Idle.png'), 5, 1, x, y)
        air = False

    elif air and all_keys[pygame.K_d] and not all_keys[pygame.K_a] and not all_keys[pygame.K_LSHIFT]:
        x, y = player.rect.x, player.rect.y
        player_sprite.remove(player)
        player = AnimatedSprite(load_image('Walk.png'), 8, 1, x, y)
        air = False

    elif air and not all_keys[pygame.K_d] and all_keys[pygame.K_a] and not all_keys[pygame.K_LSHIFT]:
        x, y = player.rect.x, player.rect.y
        player_sprite.remove(player)
        player = AnimatedSprite(load_image('Walk_left.png'), 8, 1, x, y)
        air = False

    elif air and all_keys[pygame.K_d] and not all_keys[pygame.K_a] and all_keys[pygame.K_LSHIFT]:
        x, y = player.rect.x, player.rect.y
        player_sprite.remove(player)
        player = AnimatedSprite(load_image('Run.png'), 8, 1, x, y)
        air = False

    elif air and not all_keys[pygame.K_d] and all_keys[pygame.K_a] and all_keys[pygame.K_LSHIFT]:
        x, y = player.rect.x, player.rect.y
        player_sprite.remove(player)
        player = AnimatedSprite(load_image('Run_left.png'), 8, 1, x, y)
        air = False

    elif air and all_keys[pygame.K_d] and all_keys[pygame.K_a]:
        x, y = player.rect.x, player.rect.y
        player_sprite.remove(player)
        player = AnimatedSprite(load_image('Hurt.png'), 2, 1, x, y)
        air = False

    # перемещение персонажа
    if all_keys[pygame.K_d] and not all_keys[pygame.K_a]:
        player.rect.x += 5
        last_direction = 'RIGHT'
    elif all_keys[pygame.K_a] and not all_keys[pygame.K_d]:
        player.rect.x -= 5
        last_direction = 'LEFT'
    if all_keys[pygame.K_d] and all_keys[pygame.K_LSHIFT] and not all_keys[pygame.K_a]:
        player.rect.x += 15
        last_direction = 'RIGHT'
    elif all_keys[pygame.K_a] and all_keys[pygame.K_LSHIFT] and not all_keys[pygame.K_d]:
        player.rect.x -= 15
        last_direction = 'LEFT'
    clock.tick(15)

pygame.quit()

