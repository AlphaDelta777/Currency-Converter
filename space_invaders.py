import pygame
import random
import json
import os

# Initialize PyGame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders: The Remake")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
NEBULA_BLUE = (10, 20, 70) 
ARCADE_BLUE = (0, 160, 255)       
ARCADE_LIGHT_GRAY = (170, 180, 190) 
ARCADE_DARK_GRAY = (90, 100, 110) 
ARCADE_PURPLE = (200, 50, 240)  
ARCADE_ORANGE = (255, 110, 0) 

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = self.size * 0.8  

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.size)

starfield = [Star() for _ in range(100)]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create a clean surface size matching our pixel layout (13x11 scale)
        self.image = pygame.Surface((52, 44), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 60
        self.speed = 6
        
        # Power-up state variables
        self.double_shot = False
        self.laser_boost = False
        self.boost_timer = 0    

        # Designing the 8-bit Starfighter Grid Layout
        # '.' = Empty Space, 'G' = Light Gray, 'D' = Dark Gray, 'B' = Thruster Blue, 'O' = Flame Orange
        pixel_map = [
            "......G......",
            ".....GGG.....",
            ".....GDG.....",
            ".....GDG.....",
            "....GGGGG....",
            "..GGGGDGGGG..",
            ".GGGGGGGGGGG.",
            "GGGGGGGGGGGGG",
            "G.BB.GGG.BB.G",
            "D.OO.D.D.OO.D",
            ".....O.O....."
        ]
        
        # Draw the layout onto the surface (each pixel character is scaled up to 4x4 blocks)
        pixel_size = 4
        color_lookup = {
            'G': ARCADE_LIGHT_GRAY,
            'D': ARCADE_DARK_GRAY,
            'B': ARCADE_BLUE,
            'O': ARCADE_ORANGE
        }
        
        for row_idx, row in enumerate(pixel_map):
            for col_idx, char in enumerate(row):
                if char in color_lookup:
                    pygame.draw.rect(
                        self.image, 
                        color_lookup[char], 
                        (col_idx * pixel_size, row_idx * pixel_size, pixel_size, pixel_size)
                    )

    def update(self):
        # Handle active power-up decay
        if self.double_shot or self.laser_boost:
            self.boost_timer -= 1
            if self.boost_timer <= 0:
                self.double_shot = False
                self.laser_boost = False
                
        # Moving these outside of the timer block ensures left/right ALWAYS work!
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Screen boundaries tracking
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Surface matching the retro wide-saucer aspect ratio (13x8 scale)
        self.image = pygame.Surface((52, 32), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Designing the 8-bit Flying Saucer Grid Layout
        # '.' = Empty Space, 'B' = Blue Dome, 'G' = Gray Rim, 'W' = White Lights, 'P' = Purple Shields
        pixel_map = [
            ".....BBB.....",
            "....BBBBB....",
            "...GGGGGGGG..",
            "..GGWGGWGGWG.",
            "GGGGGGGGGGGGG",
            "G.PPPPPPPPP.G",
            "....P...P....",
            "...P.....P..."
        ]
        
        pixel_size = 4
        color_lookup = {
            'B': ARCADE_BLUE,
            'G': ARCADE_LIGHT_GRAY,
            'W': WHITE,
            'P': ARCADE_PURPLE
        }
        
        for row_idx, row in enumerate(pixel_map):
            for col_idx, char in enumerate(row):
                if char in color_lookup:
                    pygame.draw.rect(
                        self.image, 
                        color_lookup[char], 
                        (col_idx * pixel_size, row_idx * pixel_size, pixel_size, pixel_size)
                    )

    def update(self):
        pass

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, color):
        super().__init__()
        # Draw a sleek 4-pixel wide, 16-pixel high arcade laser beam
        self.image = pygame.Surface((4, 16), pygame.SRCALPHA)
        self.image.fill(color)
        
        # Add a bright white internal core to simulate arcade glowing intensity
        pygame.draw.line(self.image, WHITE, (2, 2), (2, 14), 2)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
            
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Large surface for a massive arcade boss ship (21x10 scale)
        self.image = pygame.Surface((126, 60), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.y = 60
        self.speed = 3
        self.direction = 1
        self.health = 5

        # Designing a massive Alien Command Flagship Grid Layout
        pixel_map = [
            ".......BBBBBBBB.......",
            "......BBBBBBBBBB......",
            "....GGGGGGGGGGGGGG....",
            "...GGGGGGGGGGGGGGGG...",
            "..GGGRGGGGGGGGGGGRGGG..",
            ".GGGGGGGGGGGGGGGGGGGGG.",
            "GGGGWGGGGWGGGGWGGGGWGGG",
            "GGGGGGGGGGGGGGGGGGGGGGG",
            "..G.RR.G.RR.G.RR.G.RR.G..",
            "....R....R....R....R...."
        ]
        
        pixel_size = 6  
        color_lookup = {
            'B': ARCADE_BLUE,
            'G': ARCADE_DARK_GRAY,
            'W': WHITE,
            'R': RED
        }
        
        for row_idx, row in enumerate(pixel_map):
            for col_idx, char in enumerate(row):
                if char in color_lookup:
                    pygame.draw.rect(
                        self.image, 
                        color_lookup[char], 
                        (col_idx * pixel_size, row_idx * pixel_size, pixel_size, pixel_size)
                    )

    def update(self):
        # Hover back and forth across the top of the screen
        self.rect.x += self.speed * self.direction
        if self.rect.right >= SCREEN_WIDTH - 20 or self.rect.left <= 20:
            self.direction *= -1

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Randomly choose an item type: "DOUBLE" (Green), "BAD_LIFE" (Red), or "BOOST" (Cyan)
        self.type = random.choice(["DOUBLE", "BAD_LIFE", "BOOST"])
        
        # Color coding for visual clarity
        if self.type == "DOUBLE":
            self.color = (0, 255, 0)       # Green
        elif self.type == "BAD_LIFE":
            self.color = (255, 0, 0)       # Red
        else:
            self.color = (0, 255, 255)     # Cyan / Laser Boost
            
        # Draw a simple 12x12 pixel square icon for the item drop
        self.image = pygame.Surface((12, 12))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3

    def update(self):
        # Fall down the screen toward the player
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()     
               
# --- Game State Functions ---

def create_fleet(level):
    global fleet_speed, fleet_direction
    aliens.empty()
    boss_group.empty()  
    
    if level == 3:
        boss = Boss()
        all_sprites.add(boss)
        boss_group.add(boss)
    else:
        fleet_speed = 1.5 + (level * 0.5)
        fleet_direction = 1
        
        for row in range(5):
            for col in range(10):
                alien = Alien(60 + col * 60, 50 + row * 45)
                all_sprites.add(alien)
                aliens.add(alien)

def reset_game():
    global score, level, game_state, lives  
    score = 0
    level = 1
    lives = 3 
    all_sprites.empty()
    aliens.empty()
    boss_group.empty()
    player_lasers.empty()
    alien_lasers.empty()
    items_group.empty()
    
    global player
    player = Player()
    all_sprites.add(player)
    create_fleet(level)
    game_state = "PLAYING"
    pygame.mixer.music.play(-1)  

def save_game():
    save_data = {
        "score": score,
        "level": level,
        "lives": lives  
    }
    with open("save_game.json", "w") as f:
        json.dump(save_data, f)
    print("Game Saved!")

def load_game():
    global score, level, game_state, player
    if os.path.exists("save_game.json"):
        with open("save_game.json", "r") as f:
            save_data = json.load(f)
        
        # Load your saved progress
        score = save_data.get("score", 0)
        level = save_data.get("level", 1)
        lives = save_data.get("lives", 3)
        # Clear the old game world
        all_sprites.empty()
        aliens.empty()
        player_lasers.empty()
        alien_lasers.empty()
        items_group.empty()
        
        # Recreate the player and fleet
        player = Player()
        all_sprites.add(player)
        create_fleet(level)
        
        # Set state and restart the music loop
        game_state = "PLAYING"
        pygame.mixer.music.play(-1)
        
        print("Game Loaded Successfully!")
    else:
        print("No save file found.")

# --- Initialization ---
items_group = pygame.sprite.Group()

# --- Audio Initialization ---
pygame.mixer.init()
pygame.mixer.music.load("idoberg-deep-space-loop-401165.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

win_sound = pygame.mixer.Sound("you-win.mp3")
lose_sound = pygame.mixer.Sound("you-lose.mp3")
shoot_sound = pygame.mixer.Sound("mixkit-short-laser-gun-shot-1670.wav")
shoot_sound.set_volume(0.4)

all_sprites = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
aliens = pygame.sprite.Group()
player_lasers = pygame.sprite.Group()
alien_lasers = pygame.sprite.Group()

# Game State Variables
game_state = "MENU"
score = 0
level = 1
lives = 3

# Menu variables
menu_options = ["Insert your Soul token", "Load Game", "Quit"]
menu_selection = 0

font_large = pygame.font.SysFont(None, 60)
font_small = pygame.font.SysFont(None, 36)
save_notification_timer = 0

# --- Main Game Loop ---
running = True

while running:
    clock.tick(FPS)

    # --- 1. EVENT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if game_state == "MENU":
                if event.key == pygame.K_UP:
                    menu_selection = (menu_selection - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    menu_selection = (menu_selection + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if menu_selection == 0:    
                        reset_game()
                    elif menu_selection == 1:  
                        load_game()
                    elif menu_selection == 2:  
                        running = False
                        
            elif game_state == "PLAYING":
                if event.key == pygame.K_SPACE:
                    # --- POWERUP SHOOTING CONFIGURATIONS ---
                    if player.laser_boost:
                        # Cyan Hyper Laser: Moves at double speed (-16)
                        laser = Laser(player.rect.centerx, player.rect.top, -16, (0, 255, 255))
                        all_sprites.add(laser)
                        player_lasers.add(laser)
                    elif player.double_shot:
                        # Parallel Green lasers from left and right wings
                        laser1 = Laser(player.rect.left, player.rect.top, -8, (0, 255, 100))
                        laser2 = Laser(player.rect.right, player.rect.top, -8, (0, 255, 100))
                        all_sprites.add(laser1, laser2)
                        player_lasers.add(laser1, laser2)
                    else:
                        # Standard center laser configuration
                        laser = Laser(player.rect.centerx, player.rect.top, -8, ARCADE_BLUE)
                        all_sprites.add(laser)
                        player_lasers.add(laser)
                        
                    shoot_sound.play()
                    
                elif event.key == pygame.K_s:  
                    save_game()
                    save_notification_timer = 90  
                    
            elif game_state == "GAME_OVER":
                if event.key == pygame.K_RETURN:
                    game_state = "MENU"

    # --- 2. GAME UPDATE LOGIC ---
    if game_state == "PLAYING":
        for alien in aliens:
            alien.rect.x += fleet_speed * fleet_direction

        all_sprites.update()
        items_group.update() # Keep items dropping
        
        if level != 3 and len(aliens) == 0:
            level += 1
            create_fleet(level)

        # Fleet movement bouncing logic
        direction_change = False
        for alien in aliens:
            if alien.rect.right >= SCREEN_WIDTH:
                direction_change = True
                fleet_direction = -1  
                break
            elif alien.rect.left <= 0:
                direction_change = True
                fleet_direction = 1   
                break

        if direction_change:
            for alien in aliens:
                alien.rect.y += 15  
                alien.rect.x += fleet_speed * fleet_direction

        # Enemy AI shooting
        if level == 3 and len(boss_group) > 0:
            if random.randint(1, 20) == 1:
                active_boss = boss_group.sprites()[0]
                laser1 = Laser(active_boss.rect.left + 30, active_boss.rect.bottom, 6, YELLOW)
                laser2 = Laser(active_boss.rect.right - 30, active_boss.rect.bottom, 6, YELLOW)
                all_sprites.add(laser1, laser2)
                alien_lasers.add(laser1, laser2)
        elif len(aliens) > 0 and random.randint(1, 60) == 1:
            random_alien = random.choice(aliens.sprites())
            laser = Laser(random_alien.rect.centerx, random_alien.rect.bottom, 5, YELLOW)
            all_sprites.add(laser)
            alien_lasers.add(laser)

        # Collision: Player lasers hit enemies (Normal Levels)
        if level != 3:
            hits = pygame.sprite.groupcollide(aliens, player_lasers, True, True)
            if hits:
                score += len(hits) * 10
                for alien in hits:
                    if random.randint(1, 5) == 1:  # 20% drop rate chance
                        item = Item(alien.rect.centerx, alien.rect.bottom)
                        all_sprites.add(item)
                        items_group.add(item)
                        
        # Collision: Player lasers hit BOSS (Level 3)
        else:
            boss_hits = pygame.sprite.groupcollide(boss_group, player_lasers, False, True)
            if boss_hits:
                for active_boss in boss_hits:
                    active_boss.health -= 1  
                    score += 50             
                    if active_boss.health <= 0:
                        active_boss.kill()
                        score += 5000       
                        pygame.mixer.music.stop()
                        win_sound.play()
                        game_state = "GAME_OVER" 

        # Collision: Player catches an item drop
        item_caught = pygame.sprite.spritecollideany(player, items_group)
        if item_caught:
            if item_caught.type == "DOUBLE":
                player.double_shot = True
                player.laser_boost = False
                player.boost_timer = 240  # 4 seconds at 60 FPS
            elif item_caught.type == "BOOST":
                player.laser_boost = True
                player.double_shot = False
                player.boost_timer = 240  # 4 seconds at 60 FPS
            elif item_caught.type == "BAD_LIFE":
                lives -= 1  # Danger block!
                if lives <= 0:
                    pygame.mixer.music.stop()
                    lose_sound.play()
                    game_state = "GAME_OVER"
            item_caught.kill()

        # Collision: Alien/Boss lasers hit player
        if pygame.sprite.spritecollideany(player, alien_lasers):
            lives -= 1  
            alien_lasers.empty()  
            if lives <= 0:
                pygame.mixer.music.stop() 
                lose_sound.play()         
                game_state = "GAME_OVER"

        # Collision: Aliens reach player baseline (Normal Levels Only)
        if level != 3:
            for alien in aliens:
                if alien.rect.bottom >= player.rect.top:
                    lives -= 1
                    create_fleet(level)  
                    if lives <= 0:
                        pygame.mixer.music.stop() 
                        lose_sound.play()         
                        game_state = "GAME_OVER"
                    break

    # --- 3. RENDERING / DRAWING ---
    screen.fill(BLACK)

    for star in starfield:
        star.update()
        star.draw(screen)

    if game_state == "MENU":
        # Left Side: Player Matrix
        player_matrix = [
            "......X......", ".....XXX.....", ".....XXX.....", "....XXXXX....",
            "...XXXXXXX...", "..XXXXXXXXX..", ".XXXXXXXXXXX.", "XXXXXXXXXXXXX",
            "X.XXXXXXXXX.X", "X..X.....X..X"
        ]
        p_scale = 5
        player_surf = pygame.Surface((len(player_matrix[0]) * p_scale, len(player_matrix) * p_scale), pygame.SRCALPHA)
        for r_idx, row in enumerate(player_matrix):
            for c_idx, char in enumerate(row):
                if char == 'X':
                    pygame.draw.rect(player_surf, (0, 255, 100), (c_idx * p_scale, r_idx * p_scale, p_scale, p_scale))

        # Right Side: Boss Matrix
        boss_matrix = [
            ".......BBBBBBBB.......", "......BBBBBBBBBB......", "....GGGGGGGGGGGGGG....",
            "...GGGGGGGGGGGGGGGG...", "..GGGRGGGGGGGGGGGRGGG..", ".GGGGGGGGGGGGGGGGGGGGG.",
            "GGGGWGGGGWGGGGWGGGGWGGG", "GGGGGGGGGGGGGGGGGGGGGGG", "..G.RR.G.RR.G.RR.G.RR.G..",
            "....R....R....R....R...."
        ]
        b_scale = 5
        boss_surf = pygame.Surface((len(boss_matrix[0]) * b_scale, len(boss_matrix) * b_scale), pygame.SRCALPHA)
        boss_colors = {'B': (0, 150, 255), 'G': (60, 64, 72), 'W': (255, 255, 255), 'R': (255, 0, 50)}
        for r_idx, row in enumerate(boss_matrix):
            for c_idx, char in enumerate(row):
                if char in boss_colors:
                    pygame.draw.rect(boss_surf, boss_colors[char], (c_idx * b_scale, r_idx * b_scale, b_scale, b_scale))

        screen.blit(player_surf, (SCREEN_WIDTH // 6 - player_surf.get_width() // 2, 130))
        screen.blit(boss_surf, (5 * SCREEN_WIDTH // 6 - boss_surf.get_width() // 2, 120))
        
        # Draw Mountains
        mountain_points = [
            (0, SCREEN_HEIGHT), (0, SCREEN_HEIGHT - 80), (50, SCREEN_HEIGHT - 120),
            (110, SCREEN_HEIGHT - 70), (180, SCREEN_HEIGHT - 140), (260, SCREEN_HEIGHT - 90),
            (380, SCREEN_HEIGHT - 110), (490, SCREEN_HEIGHT - 60), (580, SCREEN_HEIGHT - 150),
            (680, SCREEN_HEIGHT - 130), (740, SCREEN_HEIGHT - 80), (800, SCREEN_HEIGHT - 110),
            (800, SCREEN_HEIGHT)         
        ]
        pygame.draw.polygon(screen, (130, 20, 0), mountain_points)
        pygame.draw.lines(screen, (200, 50, 0), False, mountain_points[1:-1], 3)

        # Title Text
        title_string_top, title_string_bottom = "SPACE", "INVADERS"
        shadow_color = (80, 40, 110)
        shadow_top = font_large.render(title_string_top, True, shadow_color)
        shadow_bottom = font_large.render(title_string_bottom, True, shadow_color)
        screen.blit(shadow_top, (SCREEN_WIDTH // 2 - shadow_top.get_width() // 2 + 5, 85))
        screen.blit(shadow_bottom, (SCREEN_WIDTH // 2 - shadow_bottom.get_width() // 2 + 5, 135))

        face_top = font_large.render(title_string_top, True, (255, 255, 0))
        face_bottom = font_large.render(title_string_bottom, True, (255, 255, 0))
        screen.blit(face_top, (SCREEN_WIDTH // 2 - face_top.get_width() // 2, 80))
        screen.blit(face_bottom, (SCREEN_WIDTH // 2 - face_bottom.get_width() // 2, 130))

        # Interactive Menu Options
        for i, option in enumerate(menu_options):
            if i == menu_selection:
                option_text = font_small.render(f"{option.upper()} ", True, WHITE)
            else:
                option_text = font_small.render(option, True, (100, 130, 180))
            text_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, 280 + i * 45))
            screen.blit(option_text, text_rect)

        # Copyright Footer
        footer_text1 = font_small.render("© SRH CORPORATION  2026", True, (180, 200, 255))
        footer_text2 = font_small.render("ALL RIGHTS RESERVED", True, (180, 200, 255))
        screen.blit(footer_text1, (SCREEN_WIDTH // 2 - footer_text1.get_width() // 2, SCREEN_HEIGHT - 80))
        screen.blit(footer_text2, (SCREEN_WIDTH // 2 - footer_text2.get_width() // 2, SCREEN_HEIGHT - 45))

    elif game_state == "PLAYING":
        all_sprites.draw(screen)
        items_group.draw(screen) # Render item modules visually
        
        # UI overlays
        score_text = font_small.render(f"Score: {score}", True, WHITE)
        level_text = font_small.render(f"Level: {level}", True, YELLOW)
        save_hint = font_small.render("Press 'S' to Save", True, GRAY)

        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 10))
        screen.blit(save_hint, (10, SCREEN_HEIGHT - 30))

        # Mini Player Counter
        for i in range(lives):
            mini_ship = pygame.transform.scale(player.image, (26, 20))
            x_pos = SCREEN_WIDTH - 40 - (i * 35)
            screen.blit(mini_ship, (x_pos, 12))

        # Save Tracker
        if save_notification_timer > 0:
            saved_text = font_small.render("GAME SAVED!", True, GREEN)
            screen.blit(saved_text, (SCREEN_WIDTH // 2 - saved_text.get_width() // 2, 20))
            save_notification_timer -= 1

    elif game_state == "GAME_OVER":
        game_over_text = font_large.render("GAME OVER", True, RED)
        final_score_text = font_small.render(f"Final Score: {score} (Level {level})", True, WHITE)
        restart_hint = font_small.render("Press ENTER to return to Menu", True, GRAY)
        
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, 280))
        screen.blit(restart_hint, (SCREEN_WIDTH // 2 - restart_hint.get_width() // 2, 350))

    pygame.display.flip()

pygame.quit()