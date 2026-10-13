import random
import math
import sys

try:
    pygame.init()
    pygame.font.init()
except Exception as e:
    print(f"Erro ao inicializar o Pygame: {e}")
    sys.exit(1)

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500

# Safe display initialization for mobile environments
try:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
except Exception:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Arcade Stage Fighter - Survival & Bosses")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (10, 15, 25)
GRAY = (148, 163, 184)
RED = (239, 68, 68)
GREEN = (34, 197, 94)
BLUE = (99, 102, 241)
GOLD = (245, 158, 11)
PURPLE = (168, 85, 247)
GROUND_Y = 410

try:
    FONT_SM = pygame.font.SysFont("Arial", 14, bold=True)
    FONT_MD = pygame.font.SysFont("Arial", 20, bold=True)
    FONT_LG = pygame.font.SysFont("Arial", 30, bold=True)
except:
    FONT_SM = pygame.font.Font(None, 24)
    FONT_MD = pygame.font.Font(None, 32)
    FONT_LG = pygame.font.Font(None, 44)

class Player:
    def __init__(self, char_type, team):
        self.char_type = char_type
        self.team = team
        self.x = 100
        self.y = GROUND_Y - 90
        self.width = 44
        self.height = 90
        self.vx = 0
        self.vy = 0
        self.max_health = 150
        self.health = 150
        self.super_meter = 0
        self.facing_right = True
        self.is_grounded = False
        self.state = "idle"
        self.attack_frame = 0
        self.score = 0
        
        if char_type == "walace":
            self.name = "Walace (Samurai)"
            self.emoji = "⚔️"
            self.color = BLUE
            self.attack_range = 80
            self.damage = 25
        elif char_type == "yann":
            self.name = "Yann (Atirador)"
            self.emoji = "🔫"
            self.color = GREEN
            self.attack_range = 140
            self.damage = 18
        elif char_type == "wender":
            self.name = "Wender (Cowboy)"
            self.emoji = "🤠"
            self.color = GOLD
            self.attack_range = 100
            self.damage = 22
        else:
            self.name = "Cleide (Mágica)"
            self.emoji = "🪄"
            self.color = PURPLE
            self.attack_range = 110
            self.damage = 20

    def update(self, keys):
        self.vy += 0.8
        self.y += self.vy
        self.x += self.vx

        if self.y >= GROUND_Y - self.height:
            self.y = GROUND_Y - self.height
            self.vy = 0
            self.is_grounded = True
        else:
            self.is_grounded = False

        if self.x < 10: self.x = 10
        if self.x > SCREEN_WIDTH - self.width - 10: self.x = SCREEN_WIDTH - self.width - 10

        self.vx = 0
        if self.state not in ["attacking", "hit"]:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.vx = -6
                self.facing_right = False
                self.state = "walking"
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.vx = 6
                self.facing_right = True
                self.state = "walking"
            else:
                self.state = "idle"

            if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.is_grounded:
                self.vy = -15
                self.is_grounded = False

        if self.state == "attacking":
            self.attack_frame += 1
            if self.attack_frame > 12:
                self.state = "idle"
                self.attack_frame = 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), self.width, self.height), border_radius=8)
        pygame.draw.circle(surface, (252, 165, 165), (int(self.x + self.width/2), int(self.y + 20)), 16)
        
        dir_mult = 1 if self.facing_right else -1
        hand_x = self.x + self.width/2 + (dir_mult * 25)
        hand_y = self.y + 40
        pygame.draw.circle(surface, GOLD, (int(hand_x), int(hand_y)), 6)

        txt = FONT_SM.render(self.name, True, WHITE)
        surface.blit(txt, (int(self.x - 10), int(self.y - 22)))

class Enemy:
    def __init__(self, enemy_type, difficulty_multiplier=1.0):
        self.enemy_type = enemy_type
        self.x = SCREEN_WIDTH + random.randint(50, 200)
        self.facing_right = False
        
        if enemy_type == "crawler":
            self.width = 40
            self.height = 30
            self.y = GROUND_Y - self.height
            self.speed = 3.5 * difficulty_multiplier
            self.health = int(30 * difficulty_multiplier)
            self.damage = 10
            self.color = (185, 28, 28)
            self.is_flying = False
        elif enemy_type == "flyer":
            self.width = 35
            self.height = 35
            self.y = GROUND_Y - 120 + random.randint(-20, 20)
            self.speed = 4.0 * difficulty_multiplier
            self.health = int(25 * difficulty_multiplier)
            self.damage = 12
            self.color = (217, 70, 239)
            self.is_flying = True
        elif enemy_type == "giant":
            self.width = 70
            self.height = 110
            self.y = GROUND_Y - self.height
            self.speed = 2.0 * difficulty_multiplier
            self.health = int(100 * difficulty_multiplier)
            self.damage = 25
            self.color = (120, 53, 15)
            self.is_flying = False
        elif enemy_type == "boss":
            self.width = 80
            self.height = 130
            self.y = GROUND_Y - self.height
            self.speed = 2.8 * difficulty_multiplier
            self.health = int(250 * difficulty_multiplier)
            self.max_health = self.health
            self.damage = 35
            self.color = (220, 38, 38)
            self.is_flying = False

    def update(self, player_x, player_y):
        if self.x < player_x:
            self.x += self.speed
            self.facing_right = True
        else:
            self.x -= self.speed
            self.facing_right = False

        if self.is_flying:
            self.y += math.sin(pygame.time.get_ticks() * 0.01) * 1.5

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), self.width, self.height), border_radius=6)
        if self.enemy_type == "boss":
            bar_w = self.width
            fill = max(0, (self.health / self.max_health) * bar_w)
            pygame.draw.rect(surface, (50, 50, 50), (int(self.x), int(self.y - 12), bar_w, 6))
            pygame.draw.rect(surface, RED, (int(self.x), int(self.y - 12), int(fill), 6))

class ItemPickup:
    def __init__(self, x, y, item_type="health"):
        self.x = x
        self.y = y
        self.item_type = item_type
        self.width = 24
        self.height = 24
        self.active = True

    def draw(self, surface):
        if not self.active: return
        color = GREEN if self.item_type == "health" else GOLD
        pygame.draw.circle(surface, color, (int(self.x + self.width/2), int(self.y + self.height/2)), 12)
        txt = FONT_SM.render("+" if self.item_type == "health" else "$", True, WHITE)
        surface.blit(txt, (int(self.x + 8), int(self.y + 4)))

def main():
    selected_char = "walace"
    selected_team = "corinthians"
    current_stage = 1
    max_stages = 4
    
    player = Player(selected_char, selected_team)
    enemies = []
    items = []
    stage_score = 0
    game_state = "menu"

    def load_stage(stage_num):
        nonlocal enemies, items
        enemies.clear()
        items.clear()
        difficulty = 1.0 + (stage_num - 1) * 0.35

        if stage_num == 1:
            for _ in range(5):
                enemies.append(Enemy("crawler", difficulty))
        elif stage_num == 2:
            for _ in range(6):
                enemies.append(Enemy("flyer", difficulty))
        elif stage_num == 3:
            for _ in range(3):
                enemies.append(Enemy("giant", difficulty))
        elif stage_num == 4:
            for _ in range(3): enemies.append(Enemy("crawler", difficulty))
            for _ in range(3): enemies.append(Enemy("flyer", difficulty))
            for _ in range(2): enemies.append(Enemy("giant", difficulty))
            enemies.append(Enemy("boss", difficulty))

        items.append(ItemPickup(SCREEN_WIDTH // 2, GROUND_Y - 30, "health"))

    running = True
    while running:
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_state == "menu":
                    if event.key == pygame.K_RETURN:
                        player = Player(selected_char, selected_team)
                        current_stage = 1
                        load_stage(current_stage)
                        game_state = "playing"
                    elif event.key == pygame.K_1: selected_char = "walace"
                    elif event.key == pygame.K_2: selected_char = "yann"
                    elif event.key == pygame.K_3: selected_char = "wender"
                    elif event.key == pygame.K_4: selected_char = "cleide"
                elif game_state == "playing":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_j:
                        player.state = "attacking"
                        player.attack_frame = 0
                        for e in enemies[:]:
                            if abs(player.x - e.x) < player.attack_range:
                                e.health -= player.damage
                                if e.health <= 0:
                                    enemies.remove(e)
                                    stage_score += 100
                elif game_state in ["gameover", "victory"]:
                    if event.key == pygame.K_RETURN:
                        game_state = "menu"

        if game_state == "menu":
            title = FONT_LG.render("ARCADE STAGE FIGHTER", True, GOLD)
            sub = FONT_MD.render(f"Personagem: {player.name} (Pressione 1-4 para trocar)", True, WHITE)
            inst = FONT_MD.render("Pressione ENTER para Iniciar a Batalha", True, GREEN)
            
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 120))
            screen.blit(sub, (SCREEN_WIDTH//2 - sub.get_width()//2, 200))
            screen.blit(inst, (SCREEN_WIDTH//2 - inst.get_width()//2, 280))

            chars_info = [
                "[1] Walace (Samurai ⚔️)", 
                "[2] Yann (Atirador 🔫)", 
                "[3] Wender (Cowboy 🤠)", 
                "[4] Cleide (Mágica 🪄)"
            ]
            for idx, info in enumerate(chars_info):
                char_keys = ["walace", "yann", "wender", "cleide"]
                c_txt = FONT_SM.render(info, True, BLUE if selected_char == char_keys[idx] else GRAY)
                screen.blit(c_txt, (SCREEN_WIDTH//2 - 100, 340 + (idx * 25)))

        elif game_state == "playing":
            player.update(keys)

            for e in enemies:
                e.update(player.x, player.y)
                if abs(player.x - e.x) < 30 and abs(player.y - e.y) < 30:
                    player.health -= 0.5
                    if player.health <= 0:
                        game_state = "gameover"

            for item in items:
                if item.active and abs(player.x - item.x) < 30:
                    if item.item_type == "health":
                        player.health = min(player.max_health, player.health + 50)
                    item.active = False

            if len(enemies) == 0:
                current_stage += 1
                if current_stage > max_stages:
                    game_state = "victory"
                else:
                    load_stage(current_stage)

            pygame.draw.rect(screen, (30, 41, 59), (0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))
            pygame.draw.line(screen, GREEN, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 4)

            for item in items: item.draw(screen)
            for e in enemies: e.draw(screen)
            player.draw(screen)

            h_txt = FONT_MD.render(f"HP: {int(player.health)}/{player.max_health}", True, RED)
            s_txt = FONT_MD.render(f"Fase: {current_stage}/{max_stages}", True, GOLD)
            score_txt = FONT_MD.render(f"Pontos: {stage_score}", True, WHITE)
            screen.blit(h_txt, (20, 20))
            screen.blit(s_txt, (SCREEN_WIDTH // 2 - 50, 20))
            screen.blit(score_txt, (SCREEN_WIDTH - 160, 20))

        elif game_state == "gameover":
            msg = FONT_LG.render("FIM DE JOGO - VOCÊ FOI DERROTADO", True, RED)
            ret = FONT_MD.render("Pressione ENTER para voltar ao Menu", True, WHITE)
            screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, 200))
            screen.blit(ret, (SCREEN_WIDTH//2 - ret.get_width()//2, 260))

        elif game_state == "victory":
            msg = FONT_LG.render("🏆 PARABÉNS! VOCÊ VENCEU TODAS AS FASES! 🏆", True, GOLD)
            ret = FONT_MD.render("Pressione ENTER para voltar ao Menu", True, WHITE)
            screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, 200))
            screen.blit(ret, (SCREEN_WIDTH//2 - ret.get_width()//2, 260))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
