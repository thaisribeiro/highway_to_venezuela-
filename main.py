import random
import pygame

from persons import Road, Lula, Trucks, Cloud, Gaudy

pygame.init()
SCREEN = WIDTH, HEIGHT = (600, 200)
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)

clock = pygame.time.Clock()
FPS = 60

WHITE = (225, 225, 225)
BLACK = (0, 0, 0)
GRAY = (32, 33, 36)

start_img = pygame.image.load('images/logo.png')

game_over_img = pygame.image.load('images/game_over.png')
game_over_img = pygame.transform.scale(game_over_img, (200, 36))

replay_img = pygame.image.load('images/replay.png')
replay_img = pygame.transform.scale(replay_img, (40, 36))
replay_rect = replay_img.get_rect()
replay_rect.x = WIDTH // 2 - 20
replay_rect.y = 100

numbers_img = pygame.image.load('images/numbers.png')
numbers_img = pygame.transform.scale(numbers_img, (120, 12))

sound_jump = pygame.mixer.Sound('sounds/irra.wav')
sound_died = pygame.mixer.Sound('sounds/morreu.wav')
sound_checkpoint = pygame.mixer.Sound('sounds/passou.wav')

road = Road()
lula = Lula(50, 160)

trucks_group = pygame.sprite.Group()
gaudy_group = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()


def reset():
    global counter, SPEED, score, high_score

    if score and score >= high_score:
        high_score = score

    counter = 0
    SPEED = 5
    score = 0
    
    sound_jump.stop()
    sound_checkpoint.stop()
    sound_died.stop()

    trucks_group.empty()
    gaudy_group.empty()
    cloud_group.empty()

    lula.reset()


keys = []
GODMODE = False
DAYMODE = False
LYAGAMI = False

counter = 0
enemy_time = 100
cloud_time = 500
stars_time = 175

SPEED = 5
jump = False
crouching = False

score = 0
high_score = 0

start_page = True
mouse_pos = (-1, -1)

running = True
while running:
    jump = False
    win.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False

            if event.key == pygame.K_SPACE:
                if start_page:
                    sound_jump.stop()
                    sound_checkpoint.stop()
                    sound_died.stop()
                    start_page = False
                elif lula.alive:
                    jump = True
                    sound_jump.play()
                    
                else:
                    reset()

            if event.key == pygame.K_UP:
                jump = True
                sound_jump.play()

            if event.key == pygame.K_DOWN:
                crouching = True

            key = pygame.key.name(event.key)
            keys.append(key)
            keys = keys[-7:]
            if ''.join(keys).upper() == 'GODMODE':
                GODMODE = not GODMODE

            if ''.join(keys).upper() == 'DAYMODE':
                DAYMODE = not DAYMODE

            if ''.join(keys).upper() == 'LYAGAMI':
                LYAGAMI = not LYAGAMI

            if ''.join(keys).upper() == 'SPEEDUP':
                SPEED += 2

            if ''.join(keys).upper() == 'IAMRICH':
                score += 10000

            if ''.join(keys).upper() == 'HISCORE':
                high_score = 99999

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                jump = False

            if event.key == pygame.K_DOWN:
                crouching = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = (-1, -1)

    if start_page:
        win.blit(start_img, (0, 0))
    else:
        if lula.alive:
            counter += 1
            if counter % int(enemy_time) == 0:
                if random.randint(1, 10) == 5:
                    y = random.choice([85, 130])
                    gaudy = Gaudy(WIDTH, y)
                    gaudy_group.add(gaudy)
                else:
                    rand = random.randint(1, 3)
                    cactus = Trucks(rand)
                    trucks_group.add(cactus)

            if counter % cloud_time == 0:
                y = random.randint(40, 100)
                cloud = Cloud(WIDTH, y)
                cloud_group.add(cloud)

            if counter % 100 == 0:
                SPEED += 0.1
                enemy_time -= 0.5

            if counter % 5 == 0:
                score += 1

            if score and score % 100 == 0:
                sound_jump.stop()
                sound_checkpoint.play()

            if not GODMODE:
                for trucks in trucks_group:
                    if LYAGAMI:
                        dx = trucks.rect.x - lula.rect.x
                        if 0 <= dx <= (70 + (score//100)):
                            jump = True

                    if pygame.sprite.collide_mask(lula, trucks):
                        SPEED = 0
                        lula.alive = False
                        sound_jump.stop()
                        sound_checkpoint.stop()
                        sound_died.play()

                for cactus in gaudy_group:
                    if LYAGAMI:
                        dx = gaudy.rect.x - lula.rect.x
                        if 0 <= dx <= 70:
                            if lula.rect.top <= gaudy.rect.top:
                                jump = True
                            else:
                                crouching = True
                        else:
                            crouching = False

                    if pygame.sprite.collide_mask(lula, gaudy):
                        SPEED = 0
                        lula.alive = False
                        sound_died.play()

        road.update(SPEED)
        road.draw(win)
        cloud_group.update(SPEED-3, lula)
        cloud_group.draw(win)
        # stars_group.update(SPEED-3, lula)
        # stars_group.draw(win)
        trucks_group.update(SPEED, lula)
        trucks_group.draw(win)
        gaudy_group.update(SPEED-1, lula)
        gaudy_group.draw(win)
        lula.update(jump, crouching)
        lula.draw(win)

        string_score = str(score).zfill(5)
        for i, num in enumerate(string_score):
            win.blit(numbers_img, (520+11*i, 10), (10*int(num), 0, 10, 12))

        if high_score:
            win.blit(numbers_img, (425, 10), (100, 0, 20, 12))
            string_score = f'{high_score}'.zfill(5)
            for i, num in enumerate(string_score):
                win.blit(numbers_img, (455+11*i, 10), (10*int(num), 0, 10, 12))

        if not lula.alive:
            win.blit(game_over_img, (WIDTH//2-100, 55))
            win.blit(replay_img, replay_rect)

            if replay_rect.collidepoint(mouse_pos):
                reset()

    pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 4)
    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
