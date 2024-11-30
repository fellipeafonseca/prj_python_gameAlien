import pgzrun  
import random


# Configurações da Tela
WIDTH = 800
HEIGHT = 600

# Estado do Jogo
state = 'menu'
points = 0  # Pontos do Jogador
speed_enemys = 3  # Velocidade dos Inimigos
points_to_win = 60  # Pontos necessários para vencer
sound_on = True  # Variavel do Som

# Carregar a música de fundo
sounds.background.play()
sounds.background.set_volume(0.5)

# Variáveis dos botões
button_start = Rect((300, 200), (200, 60))
button_exit = Rect((300, 300), (200, 60))
button_sound = Rect((300, 400), (200, 60))  # Botão to ligar/desligar Som

# Ator (Personagem do jogo)
character = Actor('alien')
character.pos = (WIDTH // 2, HEIGHT - 50)

# Lista de inimigos (3 inimigos)
enemys = [Actor('alien', (random.randint(50, WIDTH - 50), random.randint(-100, -40))) for _ in range(3)]

# Função to desenhar na tela
def draw():
    screen.clear()
    if state == 'menu':
        draw_menu()
    elif state == 'game':
        draw_game()
    elif state == 'win':
        draw_win()

# draw a tela do menu
def draw_menu():
    screen.fill((50, 150, 200))
    screen.draw.filled_rect(button_start, (0, 200, 0))
    screen.draw.filled_rect(button_exit, (200, 0, 0))
    screen.draw.filled_rect(button_sound, (100, 100, 100))
    screen.draw.text("Start Game", center=button_start.center, color="white", fontsize=30)
    screen.draw.text("Exit", center=button_exit.center, color="white", fontsize=30)
    screen.draw.text("Sound: " + ("On" if sound_on else "off"), center=button_sound.center, color="white", fontsize=30)

# draw a tela do game
def draw_game():
    screen.fill((100, 200, 100))
    character.draw()
    for enemy in enemys:
        enemy.draw()
    screen.draw.text(f"points: {points}", (10, 10), fontsize=30, color="white")

# Desenhar a tela da vitória
def draw_win():
    screen.fill((0, 0, 0))
    screen.draw.text("You Win!", center=(WIDTH // 2, HEIGHT // 2), color="yellow", fontsize=60)

# Captura cliques do mouse
def on_mouse_down(pos):
    global state, sound_on
    if state == 'menu':
        if button_start.collidepoint(pos):
            restart_game()
        elif button_exit.collidepoint(pos):
            exit()
        elif button_sound.collidepoint(pos):
            sound_on = not sound_on
            if sound_on:
                sounds.background.play()
            else:
                sounds.background.stop()

# Função de atualização do game
def update():
    global state, points, speed_enemys
    
    if state == 'game':
        move_character()
        move_enemys()
        check_collisions()

# Movimentação do character
def move_character():
    if keyboard.left and character.left > 0:
        character.x -= 10
    if keyboard.right and character.right < WIDTH:
        character.x += 10

# move dos enemys
def move_enemys():
    global points, speed_enemys
    
    for enemy in enemys:
        enemy.y += speed_enemys
        if enemy.y > HEIGHT:
            enemy.y = random.randint(-100, -40)
            enemy.x = random.randint(50, WIDTH - 50)
            points += 1  # Ganha pontos ao evitar o inimigo!
            
            # Aumenta a velocidade dos inimigos a cada 5 pontos
            if points % 5 == 0:
                speed_enemys += 1

# check colisões e condição de vitória
def check_collisions():
    global state
    
    # Colisão com enemys
    for enemy in enemys:
        if character.colliderect(enemy):
            animation_collisions()
            clock.schedule_unique(back_menu, 0.02)  # Espera 0.5 segundos antes de back ao menu
           

    # Condição de vitória
    if points >= points_to_win:
        state = 'win'

# Animação de colisão
def animation_collisions():
    character.image = 'alien_hurt'  # Muda a imagem to uma de colisão
    sounds.eep.play()  # Tocar som de colisão

# Volta ao menu após a colisão
def back_menu():
    global state
    character.image = 'alien'  # Restaurar a imagem original
    state = 'menu'

# Função recomeçar o jogo
def restart_game():
    global state, points, speed_enemys
    state = 'game'
    points = 0
    speed_enemys = 3
    character.pos = (WIDTH // 2, HEIGHT - 50)
    for enemy in enemys:
        enemy.pos = (random.randint(50, WIDTH - 50), random.randint(-100, -40))

pgzrun.go()
