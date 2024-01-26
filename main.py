import pygame
import os
import pygame.camera

pygame.init()
pygame.camera.init()

sword_sound = pygame.mixer.Sound('sound_effects/sword_sound (mp3cut.net) (2).mp3')
ON_SIGHT = pygame.mixer.Sound('sound_effects/16-Bit Starter Pack/Overworld/Long Road Ahead.ogg')
jump_sound = pygame.mixer.Sound('sound_effects/free-sound-1674743518 (mp3cut.net).mp3')

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
player_sprite = pygame.sprite.Group()
pygame.mouse.set_visible(False)
cursor1 = pygame.image.load('Ai_Cursor_Open.png')


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


clock = pygame.time.Clock()
player = AnimatedSprite(load_image('Enchantress/Idle.png'), 5, 1, 100, 550)
enemy = AnimatedSprite(load_image('Skeleton/Idle.png'), 7, 1, 300, 550)
running = True
is_jump = False
jump = 20
air = False
attack = False
sound_sword = False
sound_jump = False
death = -1
last_direction = 'RIGHT'
fone = pygame.image.load('fone_images/fone.png', )
camera = pygame.Rect(0, 0, 10, 140)

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
                player = AnimatedSprite(load_image('Enchantress/Jump.png'), 8, 1, x, y)
                is_jump = True
            if all_keys[pygame.K_d] and all_keys[pygame.K_a]:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Hurt.png'), 2, 1, x, y)
            if pygame.mouse.get_pressed()[0] and all_keys[pygame.K_a]:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Attack_2_left.png'), 3, 1, x, y)
            elif pygame.mouse.get_pressed()[0] and all_keys[pygame.K_d]:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Attack_2.png'), 3, 1, x, y)
            elif all_keys[pygame.K_d] and not all_keys[pygame.K_a] and not all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Walk.png'), 8, 1, x, y)
            elif all_keys[pygame.K_a] and not all_keys[pygame.K_d] and not all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Walk_left.png'), 8, 1, x, y)
            elif all_keys[pygame.K_a] and not all_keys[pygame.K_d] and all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Run_left.png'), 8, 1, x, y)
            elif all_keys[pygame.K_d] and not all_keys[pygame.K_a] and all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Run.png'), 8, 1, x, y)
        if event.type == pygame.KEYUP:
            # проверка отпускания клавиши на переход на другую подходящую анимацию
            all_keys = pygame.key.get_pressed()
            if not all_keys[pygame.K_d] and not all_keys[pygame.K_a] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Idle.png'), 5, 1, x, y)
                sound_sword = False
            if pygame.mouse.get_pressed()[0] and all_keys[pygame.K_a]:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Attack_2_left.png'), 3, 1, x, y)
            elif pygame.mouse.get_pressed()[0] and all_keys[pygame.K_d]:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Attack_2.png'), 3, 1, x, y)
            elif all_keys[pygame.K_d] and not all_keys[pygame.K_a] and not all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Walk.png'), 8, 1, x, y)
            elif all_keys[pygame.K_a] and not all_keys[pygame.K_d] and not all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Walk_left.png'), 8, 1, x, y)
            elif all_keys[pygame.K_a] and not all_keys[pygame.K_d] and all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Run_left.png'), 8, 1, x, y)
            elif all_keys[pygame.K_d] and not all_keys[pygame.K_a] and all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Run.png'), 8, 1, x, y)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # то же самое, что и с клавишами, но уже для нажатия мыши (атака, будет ещё подобие некой ульты, но сделаю
            # потом
            if event.button == 1 and last_direction == 'RIGHT':
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Attack_2.png'), 3, 1, x, y)
                sound_sword = True
            elif event.button == 1 and last_direction == 'LEFT':
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Attack_2_left.png'), 3, 1, x, y)
                sound_sword = True
        if event.type == pygame.MOUSEBUTTONUP:
            sound_sword = False
            all_keys = pygame.key.get_pressed()
            if all_keys[pygame.K_d] and all_keys[pygame.K_a]:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Hurt.png'), 2, 1, x, y)
            if not all_keys[pygame.K_d] and not all_keys[pygame.K_a] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Idle.png'), 5, 1, x, y)
            elif all_keys[pygame.K_d] and not all_keys[pygame.K_a] and not all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Walk.png'), 8, 1, x, y)
            elif all_keys[pygame.K_a] and not all_keys[pygame.K_d] and not all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Walk_left.png'), 8, 1, x, y)
            elif all_keys[pygame.K_a] and not all_keys[pygame.K_d] and all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Run_left.png'), 8, 1, x, y)
            elif all_keys[pygame.K_d] and not all_keys[pygame.K_a] and all_keys[pygame.K_LSHIFT] and not is_jump:
                x, y = player.rect.x, player.rect.y
                player_sprite.remove(player)
                player = AnimatedSprite(load_image('Enchantress/Run.png'), 8, 1, x, y)

    camera.x = player.rect.centerx - 150 / 2
    camera.y = player.rect.centery - 1227 / 2
    screen.blit(fone, (0, 0))
    player_sprite.update()
    player_sprite.draw(screen)
    pygame.display.update()
    pygame.display.flip()
    all_keys = pygame.key.get_pressed()
    if sound_sword:
        sword_sound.play()
    if all_keys[pygame.K_SPACE] and not is_jump:
        x, y = player.rect.x, player.rect.y
        player_sprite.remove(player)
        camera.x = player.rect.centerx - 150 / 2
        camera.y = player.rect.centery - 1227 / 2
        player = AnimatedSprite(load_image('Enchantress/Jump.png'), 8, 1, x, y)
        is_jump = True
    # создание гравитации
    if is_jump:
        if not sound_jump:
            jump_sound.play()
            sound_jump = True
            sound_sword = False
        player.rect.y -= jump
        jump -= 5
        if jump <= -20:
            is_jump = False
            jump = 20
            player.rect.y += 20
            air = True
            sound_jump = False
    # переход на другую анимацию при приземлении персонажа
    if air and not all_keys[pygame.K_d] and not all_keys[pygame.K_a]:
        x, y = player.rect.x, player.rect.y
        player_sprite.remove(player)
        player = AnimatedSprite(load_image('Enchantress/Idle.png'), 5, 1, x, y)
        air = False

    elif air and all_keys[pygame.K_d] and not all_keys[pygame.K_a] and not all_keys[pygame.K_LSHIFT]:
        x, y = player.rect.x, player.rect.y
        player_sprite.remove(player)
        player = AnimatedSprite(load_image('Enchantress/Walk.png'), 8, 1, x, y)
        air = False

    elif air and not all_keys[pygame.K_d] and all_keys[pygame.K_a] and not all_keys[pygame.K_LSHIFT]:
        x, y = player.rect.x, player.rect.y
        player_sprite.remove(player)
        player = AnimatedSprite(load_image('Enchantress/Walk_left.png'), 8, 1, x, y)
        air = False

    elif air and all_keys[pygame.K_d] and not all_keys[pygame.K_a] and all_keys[pygame.K_LSHIFT]:
        x, y = player.rect.x, player.rect.y
        player_sprite.remove(player)
        player = AnimatedSprite(load_image('Enchantress/Run.png'), 8, 1, x, y)
        air = False

    elif air and not all_keys[pygame.K_d] and all_keys[pygame.K_a] and all_keys[pygame.K_LSHIFT]:
        x, y = player.rect.x, player.rect.y
        player_sprite.remove(player)
        player = AnimatedSprite(load_image('Enchantress/Run_left.png'), 8, 1, x, y)
        air = False

    elif air and all_keys[pygame.K_d] and all_keys[pygame.K_a]:
        x, y = player.rect.x, player.rect.y
        player_sprite.remove(player)
        player = AnimatedSprite(load_image('Enchantress/Hurt.png'), 2, 1, x, y)
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

    if player.rect.x < -10:
        player.rect.x = -10
    elif player.rect.x > 666:
        player.rect.x = 666

    clock.tick(30)

pygame.quit()

