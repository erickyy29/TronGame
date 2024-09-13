import pygame
import sys
import threading
import time
import random

pygame.init()

WIDTH = 1280
HEIGHT = 720
SAFE_ZONE = 100  #Safe distance from the borders
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Background image
tron_bg = pygame.image.load("tron game.png")
tron_bg = pygame.transform.scale(tron_bg, (1280, 720))
tron_bg_rect = tron_bg.get_rect(center=(WIDTH // 2, HEIGHT // 2))

#Bike images
tron_red = pygame.image.load("redBiky.png")
tron_red = pygame.transform.scale(tron_red, (66, 36))
tron_yellow = pygame.image.load("orangeBiky.png")
tron_yellow = pygame.transform.scale(tron_yellow, (66, 36))

#Initial positions and directions
tron_red_rect = tron_red.get_rect(topleft=(50, 50))
tron_yellow_rect = tron_yellow.get_rect(bottomright=(WIDTH - 50, HEIGHT - 50))

#Clock for FPS
CLOCK = pygame.time.Clock()

#Game state
game_state = 'loading'

#Loading variables
TIME = 10000000
loading_finished = False
loading_progress = 0

#Loading bar and background
LOADING_BG = pygame.image.load("test 2.png")
LOADING_BG = pygame.transform.scale(LOADING_BG, (WIDTH, HEIGHT))
LOADING_BG_RECT = LOADING_BG.get_rect()

loading_bar = pygame.image.load("Loading Bar.png")
loading_bar_rect = loading_bar.get_rect(midleft=(280, 360))
loading_bar_width = 8

previous_yellow_direction = [-1, 0]

def doWork():
    global loading_finished, loading_progress
    for i in range(TIME):
        random_value = 523687 / 789456 * 89456  #Simulating work
        loading_progress = i
    loading_finished = True

#Start thread for loading simulation
threading.Thread(target=doWork).start()

#Button class for main menu
class Button:
    def __init__(self, text, pos, font, bg_color, hover_color):
        self.x, self.y = pos
        self.font = pygame.font.Font(font, 50)
        self.text = text
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.rect = pygame.Rect(self.x, self.y, 300, 80)
        self.shadow_rect = pygame.Rect(self.x + 5, self.y + 5, 300, 80)
        self.text_surf = self.font.render(self.text, True, pygame.Color("White"))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.bg_color
        pygame.draw.rect(screen, pygame.Color("black"), self.shadow_rect, border_radius=10)
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        screen.blit(self.text_surf, self.text_rect)

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

#Main menu function
def main_menu():
    global game_state, red_score, yellow_score
    one_player_button = Button("1 Player", (490, 300), None, pygame.Color("darkgoldenrod1"), pygame.Color("lightyellow"))
    two_player_button = Button("2 Players", (490, 450), None, pygame.Color("blue"), pygame.Color("lightblue"))
    controls_button = Button("Info", (490, 600), None, pygame.Color("black"), pygame.Color("lightgreen"))

    while game_state == 'start_screen':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if one_player_button.click(event):
                game_state = 'one_player_mode'
                red_score = 0
                yellow_score = 0
            if two_player_button.click(event):
                game_state = 'two_player_mode'
                red_score = 0
                yellow_score = 0
            if controls_button.click(event):
                game_state = 'controls_screen'

        screen.blit(tron_bg, tron_bg_rect)
        
        one_player_button.draw(screen)
        two_player_button.draw(screen)
        controls_button.draw(screen)
        pygame.display.update()
        CLOCK.tick(60)

#Controls screen function
def controls_screen():
    global game_state
    back_button = Button("Back", (490, 600), None, pygame.Color("red"), pygame.Color("lightcoral"))
    controls_text = [
        "Red Bike Controls: W (Up), A (Left), S (Down), D (Right)",
        "Yellow Bike Controls: Arrow Keys (Up, Left, Down, Right)",
        "Avoid hitting trails or boundaries (screen 1280x720)",
        "you cant go to the direction opposite of you.",
        "Ex. If you're moving left, you can't switch directly to right.",
        "To turn right, you first need to go up or down before making the turn.",
        "First to 3 points wins",
        "If timer reaches 60 secs = tie",
     
    ]

    while game_state == 'controls_screen':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.click(event):
                game_state = 'start_screen'

        screen.fill("#0d0e2e")
        for i, text in enumerate(controls_text):
            control_surf = score_font.render(text, True, pygame.Color("white"))
            control_rect = control_surf.get_rect(center=(WIDTH // 2, 200 + i * 50))
            screen.blit(control_surf, control_rect)
        
        back_button.draw(screen)
        pygame.display.update()
        CLOCK.tick(60)

#Initial direction and speed
red_direction = [1, 0]
yellow_direction = [-1, 0]
speed = 5

#Scores and font
red_score = 0
yellow_score = 0
score_font = pygame.font.Font(None, 36)

#Trails
red_trail = []
yellow_trail = []
trail_fade_time = 6000 #milliseconds

#Render scores
def render_scores():
    red_score_surf = score_font.render(f"Red: {red_score}", True, pygame.Color("red"))
    yellow_score_surf = score_font.render(f"Yellow: {yellow_score}", True, pygame.Color("yellow"))
    screen.blit(red_score_surf, (WIDTH - 150, 10))
    screen.blit(yellow_score_surf, (WIDTH - 150, 40))

#Render timer
def render_timer(time_left):
    timer_surf = score_font.render(f"Time: {time_left}", True, pygame.Color("white"))
    screen.blit(timer_surf, (WIDTH // 2 - 50, 10))

#Position reset
def reset_positions():
    global red_direction, yellow_direction, red_trail, yellow_trail, round_start_time
    tron_red_rect.topleft = (50, 50)
    tron_yellow_rect.bottomright = (WIDTH - 50, HEIGHT - 50)
    red_direction = [1, 0]
    yellow_direction = [-1, 0]
    red_trail = []
    yellow_trail = []
    pygame.time.delay(2000)
    round_start_time = pygame.time.get_ticks()#Reset the timer

#Check collision with trails
def check_collision_with_trails():
    global red_score, yellow_score
    #Red bike with yellow trail
    for point, timestamp in yellow_trail:
        if tron_red_rect.colliderect(pygame.Rect(point, (2, 2))):
            yellow_score += 1
            reset_positions()
            return

    #Yellow bike with red trail
    for point, timestamp in red_trail:
        if tron_yellow_rect.colliderect(pygame.Rect(point, (2, 2))):
            red_score += 1
            reset_positions()
            return

#Display winner message
def display_winner(color):
    winner_font = pygame.font.Font(None, 72)
    if color == "Red":
        text_color = pygame.Color("red")
    elif color == "Yellow":
        text_color = pygame.Color("yellow")

    shadow_surf = winner_font.render(f"{color} Wins!", True, pygame.Color("black"))
    shadow_rect = shadow_surf.get_rect(center=(WIDTH // 2 + 2, HEIGHT // 2 + 2))
    screen.blit(shadow_surf, shadow_rect)

    winner_surf = winner_font.render(f"{color} Wins!", True, text_color)
    winner_rect = winner_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(winner_surf, winner_rect)

    pygame.display.update()
    time.sleep(3)

#reset the game
def reset_game():
    global red_score, yellow_score
    red_score = 0
    yellow_score = 0
    reset_positions()
    game_state = 'start_screen'

grid_bg = pygame.image.load("grid.png")
grid_bg = pygame.transform.scale(grid_bg, (1280, 720))
grid_bg_rect = grid_bg.get_rect(center=(WIDTH // 2, HEIGHT // 2))

#AI function for yellow bike to stay within safe zone
def ai_move():
    global yellow_direction, previous_yellow_direction
    if (tron_yellow_rect.left < SAFE_ZONE and yellow_direction == [-1.5, 0]) or \
       (tron_yellow_rect.right > WIDTH - SAFE_ZONE and yellow_direction == [1.5, 0]) or \
       (tron_yellow_rect.top < SAFE_ZONE and yellow_direction == [0, -1.5]) or \
       (tron_yellow_rect.bottom > HEIGHT - SAFE_ZONE and yellow_direction == [0, 1.5]):
  
        yellow_direction = random.choice([[0, -1.5], [0, 1.5], [-1.5, 0], [1.5, 0]])
        if previous_yellow_direction[0] == yellow_direction[0] and previous_yellow_direction[1] == yellow_direction[1]:
            yellow_direction[0] = yellow_direction[0] * (-1)
            yellow_direction[1] = yellow_direction[1] *(-1)
        
    elif random.random() < 0.04: #randomly change direction percentage
        yellow_direction = random.choice([[0, -1.5], [0, 1.5], [-1.5, 0], [1.5, 0]])
        if previous_yellow_direction[0] == yellow_direction[0] and previous_yellow_direction[1] == yellow_direction[1]:
            yellow_direction[0] = yellow_direction[0] * (-1)
            yellow_direction[1] = yellow_direction[1] * (-1)
        previous_yellow_direction = yellow_direction
    return yellow_direction

#Timer
round_start_time = 0
round_duration = 60000  #30 secs for timer

#Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state == 'loading':
        screen.fill("#0d0e2e")

        loading_bar_width = loading_progress / TIME * 720
        loading_bar = pygame.transform.scale(loading_bar, (int(loading_bar_width), 150))
        loading_bar_rect = loading_bar.get_rect(midleft=(280, 360))

        screen.blit(LOADING_BG, LOADING_BG_RECT)
        screen.blit(loading_bar, loading_bar_rect)

        if loading_finished:
            game_state = 'start_screen'
    
    elif game_state == 'start_screen':
        main_menu()

    elif game_state == 'controls_screen':
        controls_screen()

    elif game_state == 'one_player_mode':
        screen.blit(grid_bg, grid_bg_rect)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and red_direction != [0, 1]:
            red_direction = [0, -1]
        elif keys[pygame.K_s] and red_direction != [0, -1]:
            red_direction = [0, 1]
        elif keys[pygame.K_a] and red_direction != [1, 0]:
            red_direction = [-1, 0]
        elif keys[pygame.K_d] and red_direction != [-1, 0]:
            red_direction = [1, 0]

        tron_red_rect = tron_red_rect.move(red_direction[0] * speed, red_direction[1] * speed)
        red_trail.append((tron_red_rect.center, pygame.time.get_ticks()))

        yellow_direction = ai_move()
        tron_yellow_rect = tron_yellow_rect.move(yellow_direction[0] * speed, yellow_direction[1] * speed)
        yellow_trail.append((tron_yellow_rect.center, pygame.time.get_ticks()))

        if tron_red_rect.left < 0 or tron_red_rect.right > WIDTH or tron_red_rect.top < 0 or tron_red_rect.bottom > HEIGHT:
            yellow_score += 1
            reset_positions()

        if tron_yellow_rect.left < 0 or tron_yellow_rect.right > WIDTH or tron_yellow_rect.top < 0 or tron_yellow_rect.bottom > HEIGHT:
            red_score += 1
            reset_positions()

        if red_score >= 3:
            print("RED WON")
            red_score == 0
            display_winner("Red")
            reset_positions()
            game_state = 'start_screen'

        if yellow_score >= 3:
            print("YELLOW WON")
            yellow_score == 0
            display_winner("Yellow")
            reset_positions()
            game_state = 'start_screen'

        check_collision_with_trails()

        current_time = pygame.time.get_ticks()
        red_trail = [(point, timestamp) for point, timestamp in red_trail if current_time - timestamp < trail_fade_time]
        yellow_trail = [(point, timestamp) for point, timestamp in yellow_trail if current_time - timestamp < trail_fade_time]

        screen.blit(grid_bg, grid_bg_rect)
        for point, timestamp in red_trail:
            if ((current_time - timestamp) / trail_fade_time * 255) > 150:
                alpha = max(0, 255 - (current_time - timestamp) / trail_fade_time * 255)
            else:
                alpha = max(0, 150)
            trail_surf = pygame.Surface((2, 2))
            trail_surf.set_alpha(alpha)
            trail_surf.fill(pygame.Color("red"))
            screen.blit(trail_surf, point)
        for point, timestamp in yellow_trail:
            alpha = max(0, 255 - (current_time - timestamp) / trail_fade_time * 255)
            trail_surf = pygame.Surface((2, 2))
            trail_surf.set_alpha(alpha)
            trail_surf.fill(pygame.Color("yellow"))
            screen.blit(trail_surf, point)
        screen.blit(tron_red, tron_red_rect)
        screen.blit(tron_yellow, tron_yellow_rect)
        render_scores()

        #Check if 30 seconds have passed
        time_left = max(0, round_duration - (current_time - round_start_time))
        render_timer(time_left // 1000)

        if current_time - round_start_time >= round_duration:
            red_score += 1
            yellow_score += 1
            reset_positions()

    elif game_state == 'two_player_mode':
        screen.blit(grid_bg, grid_bg_rect)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and red_direction != [0, 1]:
            red_direction = [0, -1]
        elif keys[pygame.K_s] and red_direction != [0, -1]:
            red_direction = [0, 1]
        elif keys[pygame.K_a] and red_direction != [1, 0]:
            red_direction = [-1, 0]
        elif keys[pygame.K_d] and red_direction != [-1, 0]:
            red_direction = [1, 0]

        if keys[pygame.K_UP] and yellow_direction != [0, 1]:
            yellow_direction = [0, -1]
        elif keys[pygame.K_DOWN] and yellow_direction != [0, -1]:
            yellow_direction = [0, 1]
        elif keys[pygame.K_LEFT] and yellow_direction != [1, 0]:
            yellow_direction = [-1, 0]
        elif keys[pygame.K_RIGHT] and yellow_direction != [-1, 0]:
            yellow_direction = [1, 0]

        tron_red_rect = tron_red_rect.move(red_direction[0] * speed, red_direction[1] * speed)
        tron_yellow_rect = tron_yellow_rect.move(yellow_direction[0] * speed, yellow_direction[1] * speed)

        red_trail.append((tron_red_rect.center, pygame.time.get_ticks()))
        yellow_trail.append((tron_yellow_rect.center, pygame.time.get_ticks()))

        if tron_red_rect.left < 0 or tron_red_rect.right > WIDTH or tron_red_rect.top < 0 or tron_red_rect.bottom > HEIGHT:
            yellow_score += 1
            reset_positions()

        if tron_yellow_rect.left < 0 or tron_yellow_rect.right > WIDTH or tron_yellow_rect.top < 0 or tron_yellow_rect.bottom > HEIGHT:
            red_score += 1
            reset_positions()

        if red_score >= 3:
            print("RED WON")
            red_score == 0
            display_winner("Red")
            reset_positions()
            game_state = 'start_screen'

        if yellow_score >= 3:
            print("YELLOW WON")
            yellow_score == 0
            display_winner("Yellow")
            reset_positions()
            game_state = 'start_screen'


        check_collision_with_trails()

        current_time = pygame.time.get_ticks()
        red_trail = [(point, timestamp) for point, timestamp in red_trail if current_time - timestamp < trail_fade_time]
        yellow_trail = [(point, timestamp) for point, timestamp in yellow_trail if current_time - timestamp < trail_fade_time]
        #these update the red and yellow trails only the points/trail is younger are kept in trail
        screen.blit(grid_bg, grid_bg_rect)
        for point, timestamp in red_trail:
            alpha = max(0, 255 - (current_time - timestamp) / trail_fade_time * 255)
            trail_surf = pygame.Surface((2, 2))
            trail_surf.set_alpha(alpha)
            trail_surf.fill(pygame.Color("red"))
            screen.blit(trail_surf, point)
        for point, timestamp in yellow_trail:
            alpha = max(0, 255 - (current_time - timestamp) / trail_fade_time * 255)
            trail_surf = pygame.Surface((2, 2))
            trail_surf.set_alpha(alpha)
            trail_surf.fill(pygame.Color("yellow"))
            screen.blit(trail_surf, point)
        #renders the trails
        screen.blit(tron_red, tron_red_rect)
        screen.blit(tron_yellow, tron_yellow_rect)
        render_scores()

        #Check if 30 seconds have passed
        time_left = max(0, round_duration - (current_time - round_start_time))
        render_timer(time_left // 1000)

        if current_time - round_start_time >= round_duration:
            red_score += 1
            yellow_score += 1
            reset_positions()

    pygame.display.update()
    CLOCK.tick(60)
