import pygame
import os
import random
import json

pygame.init()
pygame.font.init()

info = pygame.display.Info()

print(f"Window width: {info.current_w}, {info.current_h}")

# Ustawienie wysokości i szerokości okna
WINDOW_WIDTH, WINDOW_HEIGHT = info.current_w, info.current_h
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.NOFRAME)
# Ustawienia okna
pygame.display.set_caption("Circle Game")
pygame.display.set_icon(pygame.image.load(os.path.join('files', 'icon.png')))

# Kolory
MAIN_COLOR = (0, 0, 14)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
SMOKED_WHITE = (192, 192, 192)
LESS_SMOKED_WHITE = (210, 210, 210)

# Ustawienie czasu odświeżania gry wykorzystane w linii 32 (i 29)
FPS	= 60

# Inne ustawienia
SMALL_FONT = pygame.font.Font(os.path.join("files", "PixelEmulator-xq08.ttf"), 16)
MEDIUM_FONT = pygame.font.Font(os.path.join("files", "PixelEmulator-xq08.ttf"), 24)
MAIN_FONT = pygame.font.Font(os.path.join("files", "PixelEmulator-xq08.ttf"), 32)
BIG_FONT = pygame.font.Font(os.path.join("files", "PixelEmulator-xq08.ttf"), 48)

# Eventy
PLAYER_WAS_HIT = pygame.USEREVENT + 1

# Tekstury
PLAYER_IMG = pygame.image.load(os.path.join("files", "player_circle.png"))
PLAYER_IMG = pygame.transform.scale(PLAYER_IMG, (WINDOW_WIDTH//19.2, WINDOW_HEIGHT//10.8))
RED_HEART_IMG = pygame.image.load(os.path.join("files", "red_heart.png"))
RED_HEART_IMG = pygame.transform.scale(RED_HEART_IMG, (WINDOW_WIDTH//120, WINDOW_HEIGHT//67.5))
GRAY_HEART_IMG = pygame.image.load(os.path.join("files", "red_heart.png"))
GRAY_HEART_IMG = pygame.transform.scale(GRAY_HEART_IMG, (16, 16))

def read_stat(stat):
    with open(os.path.join("files", "stats.json"), "r") as file:
        data = json.load(file)
        return data[stat]

def save_stat(stat, value):
    with open(os.path.join("files", "stats.json"), "r") as file:
        data = json.load(file)

    data[stat] = value

    with open(os.path.join("files", "stats.json"), "w") as file:
        json.dump(data, file, indent=4)

def lose(seconds_passed, diff, osh, WIN):
    if diff == 1 and osh == False:
        if seconds_passed > read_stat("best_easy_time"):
            save_stat("best_easy_time", seconds_passed)
    elif diff == 1 and osh == True:
        if seconds_passed > read_stat("best_easy_time_oneshot"):
            save_stat("best_easy_time_oneshot", seconds_passed)

    elif diff == 2 and osh == False:
        if seconds_passed > read_stat("best_medium_time"):
            save_stat("best_medium_time", seconds_passed)
    elif diff == 2 and osh == True:
        if seconds_passed > read_stat("best_medium_time_oneshot"):
            save_stat("best_medium_time_oneshot", seconds_passed)
            
    elif diff == 3 and osh == False:
        if seconds_passed > read_stat("best_hard_time"):
            save_stat("best_hard_time", seconds_passed)
    elif diff == 3 and osh == True:
        if seconds_passed > read_stat("best_hard_time_oneshot"):
            save_stat("best_hard_time_oneshot", seconds_passed)
            
    elif diff == 4 and osh == False:
        if seconds_passed > read_stat("best_vhard_time"):
            save_stat("best_vhard_time", seconds_passed)
    elif diff == 4 and osh == True:
        if seconds_passed > read_stat("best_vhard_time_oneshot"):
            save_stat("best_vhard_time_oneshot", seconds_passed)
            
    elif diff == 5 and osh == False:
        if seconds_passed > read_stat("best_extreme_time"):
            save_stat("best_extreme_time", seconds_passed)
    elif diff == 5 and osh == True:
        if seconds_passed > read_stat("best_extreme_time_oneshot"):
            save_stat("best_extreme_time_oneshot", seconds_passed)
            
    elif diff == 6 and osh == False:
        if seconds_passed > read_stat("best_insane_time"):
            save_stat("best_insane_time", seconds_passed)
    elif diff == 6 and osh == True:
        if seconds_passed > read_stat("best_insane_time_oneshot"):
            save_stat("best_insane_time_oneshot", seconds_passed)
            
    else:
        print("There was an error with detecting difficulty")

    print("You lost")

    save_stat("current_difficulty", 7)
    save_stat("one_shot_enabled", None)

    clock = pygame.time.Clock()

    lost_menu_running = True
    while lost_menu_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Zamknięcie okna po kliknięciu X
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    lost_menu_running = False
                    pygame.display.quit()
                    pygame.quit()
                    exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.time.set_timer(0, 0)
                    main()

        WIN.fill(MAIN_COLOR)

        you_lost_text = MAIN_FONT.render("You lost", True, SMOKED_WHITE)
        WIN.blit(you_lost_text, (WINDOW_WIDTH - WINDOW_WIDTH//40 - you_lost_text.get_width(), WINDOW_HEIGHT//40))
        you_lost_info_text = SMALL_FONT.render("Click ENTER to restart game or ESC to close the game", True, SMOKED_WHITE)
        WIN.blit(you_lost_info_text, (WINDOW_WIDTH//40, WINDOW_HEIGHT - WINDOW_HEIGHT//40))

        last_game_time_text = BIG_FONT.render(f"You lasted {seconds_passed} seconds", True, WHITE)
        WIN.blit(last_game_time_text, (WINDOW_WIDTH//2 - last_game_time_text.get_width()//2, WINDOW_HEIGHT//2 - last_game_time_text.get_height()//2))

        stats_text = MAIN_FONT.render("Best game times", True, WHITE)
        WIN.blit(stats_text, (WINDOW_WIDTH//40, WINDOW_HEIGHT//40))

        # Statystyki
        normal_mode_stats_text = MEDIUM_FONT.render("Normal mode", True, LESS_SMOKED_WHITE)
        WIN.blit(normal_mode_stats_text, (WINDOW_WIDTH//40, WINDOW_HEIGHT//40 + stats_text.get_height()))

        bet_text = SMALL_FONT.render(f'Easy: {read_stat("best_easy_time")}', True, SMOKED_WHITE)
        WIN.blit(bet_text, (WINDOW_WIDTH//40, WINDOW_HEIGHT//40 + normal_mode_stats_text.get_height() + stats_text.get_height()))
        bmt_text = SMALL_FONT.render(f'Medium: {read_stat("best_medium_time")}', True, SMOKED_WHITE)
        WIN.blit(bmt_text, (WINDOW_WIDTH//40, WINDOW_HEIGHT//40 + normal_mode_stats_text.get_height() + stats_text.get_height() + bet_text.get_height()))
        bht_text = SMALL_FONT.render(f'Hard: {read_stat("best_hard_time")}', True, SMOKED_WHITE)
        WIN.blit(bht_text, (WINDOW_WIDTH//40, WINDOW_HEIGHT//40 + normal_mode_stats_text.get_height() + stats_text.get_height() + bet_text.get_height()*2))
        bvht_text = SMALL_FONT.render(f'V. Hard: {read_stat("best_vhard_time")}', True, SMOKED_WHITE)
        WIN.blit(bvht_text, (WINDOW_WIDTH//40, WINDOW_HEIGHT//40 + normal_mode_stats_text.get_height() + stats_text.get_height() + bet_text.get_height()*3))
        bext_text = SMALL_FONT.render(f'Extreme: {read_stat("best_extreme_time")}', True, SMOKED_WHITE)
        WIN.blit(bext_text, (WINDOW_WIDTH//40, WINDOW_HEIGHT//40 + normal_mode_stats_text.get_height() + stats_text.get_height() + bet_text.get_height()*4))
        bint_text = SMALL_FONT.render(f'Insane: {read_stat("best_insane_time")}', True, SMOKED_WHITE)
        WIN.blit(bint_text, (WINDOW_WIDTH//40, WINDOW_HEIGHT//40 + normal_mode_stats_text.get_height() + stats_text.get_height() + bet_text.get_height()*5))

        # Statystyki oneshot
        oneshot_mode_stats_text = MEDIUM_FONT.render("Oneshot mode", True, LESS_SMOKED_WHITE)
        WIN.blit(oneshot_mode_stats_text, (WINDOW_WIDTH//40, WINDOW_HEIGHT//40 + normal_mode_stats_text.get_height() + stats_text.get_height() + bet_text.get_height()*6))

        bet_oneshot_text = SMALL_FONT.render(f'Easy: {read_stat("best_easy_time_oneshot")}', True, SMOKED_WHITE)
        WIN.blit(bet_oneshot_text, (WINDOW_WIDTH//40, WINDOW_HEIGHT//40 + oneshot_mode_stats_text.get_height() + normal_mode_stats_text.get_height() + stats_text.get_height() + bet_text.get_height()*6))
        bmt_oneshot_text = SMALL_FONT.render(f'Medium: {read_stat("best_medium_time_oneshot")}', True, SMOKED_WHITE)
        WIN.blit(bmt_oneshot_text, (WINDOW_WIDTH//40, WINDOW_HEIGHT//40 + oneshot_mode_stats_text.get_height() + normal_mode_stats_text.get_height() + stats_text.get_height() + bet_text.get_height()*7))
        bht_oneshot_text = SMALL_FONT.render(f'Hard: {read_stat("best_hard_time_oneshot")}', True, SMOKED_WHITE)
        WIN.blit(bht_oneshot_text, (WINDOW_WIDTH//40, WINDOW_HEIGHT//40 + oneshot_mode_stats_text.get_height() + normal_mode_stats_text.get_height() + stats_text.get_height() + bet_text.get_height()*8))

        bvht_oneshot_text = SMALL_FONT.render(f'V. Hard: {read_stat("best_vhard_time_oneshot")}', True, SMOKED_WHITE)
        WIN.blit(bvht_oneshot_text, (WINDOW_WIDTH//40, WINDOW_HEIGHT//40 + oneshot_mode_stats_text.get_height() + normal_mode_stats_text.get_height() + stats_text.get_height() + bet_text.get_height()*9))
        bext_oneshot_text = SMALL_FONT.render(f'Extreme: {read_stat("best_extreme_time_oneshot")}', True, SMOKED_WHITE)
        WIN.blit(bext_oneshot_text, (WINDOW_WIDTH//40, WINDOW_HEIGHT//40 + oneshot_mode_stats_text.get_height() + normal_mode_stats_text.get_height() + stats_text.get_height() + bet_text.get_height()*10))
        bint_oneshot_text = SMALL_FONT.render(f'Insane: {read_stat("best_insane_time_oneshot")}', True, SMOKED_WHITE)
        WIN.blit(bint_oneshot_text, (WINDOW_WIDTH//40, WINDOW_HEIGHT//40 + oneshot_mode_stats_text.get_height() + normal_mode_stats_text.get_height() + stats_text.get_height() + bet_text.get_height()*11))

        pygame.display.update()

def draw_window(player, bullets_right, bullet_right, bullets_left, bullet_left, PLAYER_HEALTH, seconds_passed, WIN):
    WIN.fill(MAIN_COLOR)
    WIN.blit(PLAYER_IMG, (player.x, player.y))

    hp_text = MAIN_FONT.render("HP " + str(PLAYER_HEALTH), True, WHITE)
    WIN.blit(hp_text, (WINDOW_WIDTH//40, WINDOW_HEIGHT//16))

    timer_text = MAIN_FONT.render("Time: " + str(seconds_passed), True, WHITE)
    WIN.blit(timer_text, (WINDOW_WIDTH//40, WINDOW_HEIGHT//40))

    # WIN.blit(RED_HEART_IMG, (WINDOW_WIDTH//40, WINDOW_HEIGHT//40))

    for bullet_right in bullets_right:
        pygame.draw.rect(WIN, RED, bullet_right)

    for bullet_left in bullets_left:
        pygame.draw.rect(WIN, RED, bullet_left)

    pygame.display.update() # Odświeżenie ekranu

def player_movement(keys_pressed, player, PLAYER_SPEED):
    if keys_pressed[pygame.K_w] and player.y - PLAYER_SPEED > 0: # Poruszanie w górę
        player.y -= PLAYER_SPEED
    elif keys_pressed[pygame.K_UP] and player.y - PLAYER_SPEED > 0:
        player.y -= PLAYER_SPEED
        
    if keys_pressed[pygame.K_s] and player.y + PLAYER_SPEED + player.height < WINDOW_HEIGHT: # Poruszanie w dół
        player.y += PLAYER_SPEED
    elif keys_pressed[pygame.K_DOWN] and player.y + PLAYER_SPEED + player.height < WINDOW_HEIGHT:
        player.y += PLAYER_SPEED
        
    if keys_pressed[pygame.K_a] and player.x - PLAYER_SPEED > 0: # Poruszanie w lewo
        player.x -= PLAYER_SPEED
    elif keys_pressed[pygame.K_LEFT] and player.x - PLAYER_SPEED > 0:
        player.x -= PLAYER_SPEED
        
    if keys_pressed[pygame.K_d] and player.x + PLAYER_SPEED + player.width < WINDOW_WIDTH: # Poruszanie w prawo
        player.x += PLAYER_SPEED
    elif keys_pressed[pygame.K_RIGHT] and player.x + PLAYER_SPEED + player.width < WINDOW_WIDTH:
        player.x += PLAYER_SPEED

def handle_bullets(bullets_right, bullet_right, bullets_left, bullet_left, player, BULLET_SPEED):
    for bullet_right in bullets_right:
        bullet_right.x -= BULLET_SPEED

        if player.colliderect(bullet_right):
            pygame.event.post(pygame.event.Event(PLAYER_WAS_HIT))
            bullets_right.remove(bullet_right)

        elif bullet_right.x < 0:
            bullets_right.remove(bullet_right)

    for bullet_left in bullets_left:
        bullet_left.x += BULLET_SPEED

        if player.colliderect(bullet_left):
            pygame.event.post(pygame.event.Event(PLAYER_WAS_HIT))
            bullets_left.remove(bullet_left)

        elif bullet_left.x > WINDOW_WIDTH:
            bullets_left.remove(bullet_left)

def main():
    difficulty = read_stat("current_difficulty")
    one_shot = read_stat("one_shot_enabled")

    if difficulty == 7 or one_shot == None:
        os.startfile("start.pyw")

    ticks_passed = 0
    
    if difficulty == 0:
        PLAYER_SPEED = 10
        PLAYER_HEALTH = 1000
        BULLET_SPEED = 14
        MAX_BULLETS = 39
        print("Debugger mode")
    elif difficulty == 1:
        PLAYER_SPEED = 10
        PLAYER_HEALTH = 10
        BULLET_SPEED = 6
        MAX_BULLETS = 15
    elif difficulty == 2:
        PLAYER_SPEED = 10
        PLAYER_HEALTH = 10
        BULLET_SPEED = 8
        MAX_BULLETS = 15
    elif difficulty == 3:
        PLAYER_SPEED = 10
        PLAYER_HEALTH = 5
        BULLET_SPEED = 12
        MAX_BULLETS = 19
    elif difficulty == 4:
        PLAYER_SPEED = 10
        PLAYER_HEALTH = 5
        BULLET_SPEED = 16
        MAX_BULLETS = 19
    elif difficulty == 5:
        PLAYER_SPEED = 10
        PLAYER_HEALTH = 5
        BULLET_SPEED = 16
        MAX_BULLETS = 23
    elif difficulty == 6:
        PLAYER_SPEED = 16
        PLAYER_HEALTH = 2
        BULLET_SPEED = 20
        MAX_BULLETS = 23
    else:
        print("ER294")
        pygame.display.quit()
        pygame.quit()
        exit()
    if one_shot == True:
        PLAYER_HEALTH = 1

    player = pygame.Rect(WINDOW_WIDTH // 2 - 64, WINDOW_HEIGHT // 2 - 64, PLAYER_IMG.get_width(), PLAYER_IMG.get_height()) # Reprezentuje gracza

    # Tworzy listę kuli
    bullets_right = []
    bullets_left = []

    clock = pygame.time.Clock()
    running = True
    while running: # Główna pętla
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Zamknięcie okna po kliknięciu X
                save_stat("current_difficulty", 7)
                save_stat("one_shot_enabled", None)
                running = False
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_stat("current_difficulty", 7)
                    save_stat("one_shot_enabled", None)
                    pygame.display.quit()
                    pygame.quit()
                    exit()
            if event.type == PLAYER_WAS_HIT:
                PLAYER_HEALTH -= 1
                print("-1 HP")

        ticks_passed += 1
        seconds_passed = ticks_passed / 60
        seconds_passed = round(seconds_passed, 2)

        bullet_left = None
        bullet_right = None

        if len(bullets_right) <= MAX_BULLETS // 2:
            bullet_right = pygame.Rect(random.randint(WINDOW_WIDTH, WINDOW_WIDTH + WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT), 16, 16) # Reprezentuje kule
            bullets_right.append(bullet_right)

        if len(bullets_left) <= MAX_BULLETS // 2:
            bullet_left = pygame.Rect(0 - random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT), 16, 16) # Reprezentuje kule
            bullets_left.append(bullet_left)

        keys_pressed = pygame.key.get_pressed() # Ustawia aktualnie naciskany przycisk jako zmienną
        player_movement(keys_pressed, player, PLAYER_SPEED) # Wywołanie funkcji ruchu gracza

        handle_bullets(bullets_right, bullet_right, bullets_left, bullet_left, player, BULLET_SPEED) # Linia 45

        draw_window(player, bullets_right, bullet_right, bullets_left, bullet_left, PLAYER_HEALTH, seconds_passed, WIN) # Linia 28

        if PLAYER_HEALTH <= 0:
            running = False
            pygame.time.delay(2000)
            lose(seconds_passed, difficulty, one_shot, WIN)

main()