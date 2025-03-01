import pygame
pygame.init()
import pygame.mixer
pygame.mixer.init()

shot_sound = pygame.mixer.Sound('shot.mp3')

fail_sound = pygame.mixer.Sound('fail.mp3')
win_sound = pygame.mixer.Sound('win.wav')
pygame.mixer.music.load('soundtrack.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
win_sound.set_volume(0.3)
shot_sound.set_volume(0.6)
FPS = 120

clock = pygame.time.Clock()
screen = pygame.display.set_mode((640, 480))
screen_rect = screen.get_rect()
main_color = (255, 255, 255)
missile_color = (255, 0, 0)
ship_color = (0, 0, 0)

fail_color = (0, 0, 0)
win_color = (0, 255, 0)
back_color = main_color
ship = pygame.Rect(300, 200, 50, 100)
ship.right = screen_rect.right
ship.centery = screen_rect.centery
missile = pygame.Rect(50, 50, 10, 10)
missile.left = screen_rect.left
missile.centery = screen_rect.centery

missile_speed_x = 0
missile_speed_y = 0
ship_speed_y = 1  # Начальная скорость корабля

ship_alive = True
missile_alive = True
missile_launched = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not missile_launched:
                missile_launched = True
                missile_speed_x = 3  # Скорость ракеты по оси X
                missile_speed_y = 0  # Ракета летит прямо
                shot_sound.play()
    # Бесконечное движение корабля (если корабль жив)
    if ship_alive:
        ship.move_ip(0, ship_speed_y)
        if ship.bottom >= screen_rect.bottom or ship.top <= 0:
            ship_speed_y *= -1  # Меняем направление движения корабля

    # Управление ракетой
    if missile_alive:
        missile.move_ip(missile_speed_x, missile_speed_y)
        if not missile.colliderect(screen_rect):  # Ракета вышла за пределы экрана?
            missile_alive = False
            back_color = fail_color
            pygame.mixer.music.stop()
            fail_sound.play()
        if ship_alive and missile.colliderect(ship):
            missile_alive = False
            ship_alive = False
            back_color = win_color
            pygame.mixer.music.stop()
            win_sound.play()

    # Отрисовка объектов
    screen.fill(back_color)
    if ship_alive:
        pygame.draw.rect(screen, ship_color, ship)
    if missile_alive:
        pygame.draw.rect(screen, missile_color, missile)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()