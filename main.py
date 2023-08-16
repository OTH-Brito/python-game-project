import pygame
import spritesheet
import enemy
import random
from pygame.locals import *

# Inicializa o pygame
pygame.init()

# Janela
window_width = 1024
window_height = 768
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("META CITY - LSW")
background_image = pygame.image.load("bgimage.png")
background_rect = background_image.get_rect()
background_menu = pygame.image.load("meta_city_resized.png")
background_menu_rect = background_menu.get_rect()
# Clock do jogo
clock = pygame.time.Clock()

# Definir cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = ((255, 255, 0))
GRAY = ((128, 128, 128))
GREEN = ((0, 255, 0))

#Sprites
player_sprite_image = pygame.image.load('player_sheet.png').convert_alpha()
enemy1_sprite_image = pygame.image.load('enemy_sheet.png').convert_alpha()
botao_novo_jogo_image = pygame.image.load(
  'botao_novo_jogo.png').convert_alpha()
botao_sair_image = pygame.image.load('botao_sair.png').convert_alpha()
botao_credito_image = pygame.image.load('botao_credito.png').convert_alpha()
enemy1_sheet = spritesheet.SpriteSheet(enemy1_sprite_image)
player_sheet = spritesheet.SpriteSheet(player_sprite_image)
botao_novo_jogo_sheet = spritesheet.SpriteSheet(botao_novo_jogo_image)
botao_sair_sheet = spritesheet.SpriteSheet(botao_sair_image)
botao_credito_sheet = spritesheet.SpriteSheet(botao_credito_image)

#lista de animação

#Player
player_animation_list = []
player_animation_steps = [4, 4, 4, 4]
player_action = 0
player_last_update = pygame.time.get_ticks()
player_animation_cooldown = 100
player_frame = 0
player_step_counter = 0
player_surface = pygame.display.set_mode((window_width, window_height))

for animations in player_animation_steps:
  temp_img_list = []
  for _ in range(animations):
    temp_img_list.append(
      player_sheet.get_image(player_step_counter, 32, 32, 1, GREEN))
    player_step_counter += 1
  player_animation_list.append(temp_img_list)

#Enemy 1
enemy1_animation_list = []
enemy1_animation_steps = [7, 1, 7, 1, 7, 1, 7]
enemy1_action = 0
enemy1_last_update = pygame.time.get_ticks()
enemy1_animation_cooldown = 100
enemy1_frame = 0
enemy1_step_counter = 0
enemy1_surface = pygame.display.set_mode((window_width, window_height))

for animations in enemy1_animation_steps:
  temp_img_list = []
  for _ in range(animations):
    temp_img_list.append(
      enemy1_sheet.get_image(enemy1_step_counter, 32, 32, 1, BLACK))
    enemy1_step_counter += 1
  enemy1_animation_list.append(temp_img_list)

#Botão novo jogo
botao_novo_jogo_animation_list = []
botao_novo_jogo_animation_steps = [1, 7]
botao_novo_jogo_action = 0
botao_novo_jogo_last_update = pygame.time.get_ticks()
botao_novo_jogo_animation_cooldown = 100
botao_novo_jogo_frame = 0
botao_novo_jogo_step_counter = 0
botao_novo_jogo_surface = pygame.display.set_mode(
  (window_width, window_height))

for animations in botao_novo_jogo_animation_steps:
  temp_img_list = []
  for _ in range(animations):
    temp_img_list.append(
      botao_novo_jogo_sheet.get_image(botao_novo_jogo_step_counter, 64, 64, 3,
                                      BLACK))
    botao_novo_jogo_step_counter += 1
  botao_novo_jogo_animation_list.append(temp_img_list)

#Botão sair
botao_sair_animation_list = []
botao_sair_animation_steps = [1, 7]
botao_sair_action = 0
botao_sair_last_update = pygame.time.get_ticks()
botao_sair_animation_cooldown = 100
botao_sair_frame = 0
botao_sair_step_counter = 0
botao_sair_surface = pygame.display.set_mode((window_width, window_height))

for animations in botao_sair_animation_steps:
  temp_img_list = []
  for _ in range(animations):
    temp_img_list.append(
      botao_sair_sheet.get_image(botao_sair_step_counter, 64, 18, 1, BLACK))
    botao_sair_step_counter += 1
  botao_sair_animation_list.append(temp_img_list)

#Botão credito
botao_credito_animation_list = []
botao_credito_animation_steps = [1, 8]
botao_credito_action = 0
botao_credito_last_update = pygame.time.get_ticks()
botao_credito_animation_cooldown = 100
botao_credito_frame = 0
botao_credito_step_counter = 0
botao_credito_surface = pygame.display.set_mode((window_width, window_height))

for animations in botao_credito_animation_steps:
  temp_img_list = []
  for _ in range(animations):
    temp_img_list.append(
      botao_credito_sheet.get_image(botao_credito_step_counter, 64, 18, 1,
                                    BLACK))
    botao_credito_step_counter += 1
  botao_credito_animation_list.append(temp_img_list)

#Efeitos sonoros e musicas
#player_walk = pygame.mixer.Sound("player_walk.wav")
enemy1_hit = pygame.mixer.Sound("enemy1_hit.wav")
sword_fx = pygame.mixer.Sound("sword_fx.wav")
menu_song = pygame.mixer.Sound("menu_song.wav")
stage_song = pygame.mixer.Sound("stage_song.wav")

stage_song.set_volume(0.1)
menu_song.set_volume(0.1)
sword_fx.set_volume(2)

# Debug
debug = False
speed_debug_font = pygame.font.SysFont(None, 48)


# Atributos do jogador
def setPlayerX(x):
  if x == None:
    return 400
  return x


def setPlayerY(y):
  if y == None:
    return 300
  return y


player_x = setPlayerX(None)
player_y = setPlayerY(None)
player_width = 32
player_height = 32
player_speed = 3
player_life = 3
player_color = WHITE
hit = False
player_frames = -99
player_frames_limit = -99
player_direction = None
old_player_direction = None
tick = 0

# Ataque da espada
flag_ataque = False
ataque_timer = 0
ataque_key = -999

sowrd_rect = None

up_down_sowrd_width = 3
up_down_sowrd_hight = 18
extended_up_down_sowrd_hight = 34

left_right_sowrd_hight = 3
left_right_sowrd_width = 18
extended_left_right_sowrd_width = 34

# Teclas
last_key_presed = -999
before_last_key_presed = -999


# Animação do jogador
def setStep(step):
  if step is None:
    return 2
  return step


def setDistance(distance):
  if distance is None:
    return 60
  return distance


step = 2
distance = 70


#Cria as areas de spawn
def createspawners():
  spawners = []
  spawnerstep = 32
  for i in range(33):
    spawners.append(pygame.Rect(spawnerstep * i, 0, 2, 2))
    spawners.append(pygame.Rect(spawnerstep * i, 768, 2, 2))
  for i in range(25):
    if i * spawnerstep != 0 and i * spawnerstep != 768:
      spawners.append(pygame.Rect(0, spawnerstep * i, 2, 2))
      spawners.append(pygame.Rect(1024, spawnerstep * i, 2, 2))
  return spawners


# Maximo de inimigos na tela
max_amount = 2
spawner_list = createspawners()
enemies = []


# "Spawna" os inimigos
def spawn(amount):
  for i in range(amount):
    spawner = random.choice(spawner_list)
    enemies.append(enemy.Enemy(spawner.x, spawner.y, pygame.time.get_ticks()))

# Gerais
def directionChanged(newdirection, olddirection):
  if newdirection != olddirection:
    return True
  return False


# Tela de inicio
intro_font = pygame.font.SysFont(None, 48)
start_button_rect = pygame.Rect(300, 400, 200, 50)

# Tela de fim de jogo
death_font = pygame.font.SysFont(None, 48)
menu_button_rect = pygame.Rect(300, 400, 200, 50)
retry_button_rect = pygame.Rect(300, 400, 200, 50)

# Stados de jogo
INTRO = 0
GAME = 1
DEAD = 2
game_state = INTRO

# Game loop
running = True
while running:
  # Eventos
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    # Mouse Click
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if game_state == INTRO:
        if start_button_rect.collidepoint(event.pos):
          game_state = GAME

    if start_button_rect.collidepoint(pygame.mouse.get_pos()):
      botao_novo_jogo_action = 1
    else:
      botao_novo_jogo_action = 0
      botao_novo_jogo_frame = 0

  # Backend do jogo
  if game_state == GAME:
    # Inimigos
    if len(enemies) < max_amount:
      spawn(max_amount - len(enemies))

    # Knock back
    if hit is True:
      for e in enemies:
        e.knockback()
      if last_key_presed == pygame.K_UP:
        player_y += step
        distance -= step
      if last_key_presed == pygame.K_DOWN:
        player_y -= step
        distance -= step
      if last_key_presed == pygame.K_LEFT:
        player_x += step
        distance -= step
      if last_key_presed == pygame.K_RIGHT:
        player_x -= step
        distance -= step
      if distance == 0:
        hit = False
        distance = 70
        for e in enemies:
          if e.getcolided() is True:
            e.setcolided(False)

    # Entradas
    keys = pygame.key.get_pressed()
    if hit is not True and flag_ataque is not True:

      # Debug
      if keys[pygame.K_F8]:
        debug = True
      if debug is True:
        if keys[pygame.K_0]:
          player_speed += 0.1
          print(player_speed)
        if keys[pygame.K_1]:
          if player_speed - 0.1 > 0:
            player_speed -= 0.1
            print(player_speed)

      # Movimento
      if keys[pygame.K_UP] and player_y > (0 + 80):
        player_y -= player_speed
        last_key_presed = pygame.K_UP
        player_direction = "side_up"
        if directionChanged(player_direction, old_player_direction) is True:
          player_frames = 12
          player_frames_limit = 15
          #print(player_direction)
      if keys[pygame.K_DOWN] and player_y < (window_height - player_height -
                                             80):
        player_y += player_speed
        last_key_presed = pygame.K_DOWN
        player_direction = "side_down"
        if directionChanged(player_direction, old_player_direction) is True:
          player_frames = 0
          player_frames_limit = 3
          #print(player_direction)
      if keys[pygame.K_LEFT] and player_x > (0 + 80):
        player_x -= player_speed
        last_key_presed = pygame.K_LEFT
        player_direction = "side_left"
        if directionChanged(player_direction, old_player_direction) is True:
          player_frames = 8
          player_frames_limit = 11
          #print(player_direction)
      if keys[pygame.K_RIGHT] and player_x < (window_width - player_width -
                                              80):
        player_x += player_speed
        last_key_presed = pygame.K_RIGHT
        player_direction = "side_right"
        if directionChanged(player_direction, old_player_direction) is True:
          player_frames = 4
          player_frames_limit = 7
          #print(player_direction)
      if keys[pygame.K_x]:
        if last_key_presed != -999:
          flag_ataque = True

      if player_direction == "side_down":
        player_action = 0
      if player_direction == "side_right":
        player_action = 1
      if player_direction == "side_left":
        player_action = 2
      if player_direction == "side_up":
        player_action = 3

    for e in enemies:
      e.update(player_x, player_y)
    # Direção da espada
    if last_key_presed == pygame.K_UP:
      sowrd_rect = pygame.Rect(player_x + 15.5, player_y - up_down_sowrd_hight,
                               up_down_sowrd_width, up_down_sowrd_hight)
      ataque_key = pygame.K_UP
    if last_key_presed == pygame.K_DOWN:
      sowrd_rect = pygame.Rect(player_x + 15.5,
                               player_y + (up_down_sowrd_hight * 1.75),
                               up_down_sowrd_width, up_down_sowrd_hight)
      ataque_key = pygame.K_DOWN
    if last_key_presed == pygame.K_LEFT:
      sowrd_rect = pygame.Rect(player_x - left_right_sowrd_width,
                               player_y + 15.5, left_right_sowrd_width,
                               left_right_sowrd_hight)
      ataque_key = pygame.K_LEFT
    if last_key_presed == pygame.K_RIGHT:
      sowrd_rect = pygame.Rect(player_x + (left_right_sowrd_width * 1.75),
                               player_y + 15.5, left_right_sowrd_width,
                               left_right_sowrd_hight)
      ataque_key = pygame.K_RIGHT

      # Colisão player x inimigo
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    for e in enemies:
      if e.isdead is not True:
        if player_rect.colliderect(e.getrect()):
          hit = True
          player_life -= 1
          e.setcolided(True)

    # Ataque do player & Morte do inimigo
    if flag_ataque is True and ataque_timer <= 30:
      ataque_timer += 1
      if ataque_key == pygame.K_UP:
        sowrd_rect = pygame.Rect(player_x + 15.5,
                                 player_y - extended_up_down_sowrd_hight,
                                 up_down_sowrd_width,
                                 extended_up_down_sowrd_hight)
        for e in enemies:
          if sowrd_rect.colliderect(e.getrect()):
            e.kill()
            enemies.remove(e)
          if ataque_timer == 30:
            ataque_timer = 0
            flag_ataque = False
            sowrd_rect = pygame.Rect(player_x + 15.5,
                                     player_y - up_down_sowrd_hight,
                                     up_down_sowrd_width, up_down_sowrd_hight)

      if ataque_key == pygame.K_DOWN:
        sowrd_rect = pygame.Rect(player_x + 15.5,
                                 player_y + extended_up_down_sowrd_hight - 2,
                                 up_down_sowrd_width,
                                 extended_up_down_sowrd_hight)
        for e in enemies:
          if sowrd_rect.colliderect(e.getrect()):
            e.kill()
            enemies.remove(e)
          if ataque_timer == 30:
            ataque_timer = 0
            flag_ataque = False
            sowrd_rect = pygame.Rect(player_x + 15.5,
                                     player_y + (up_down_sowrd_hight * 1.75),
                                     up_down_sowrd_width, up_down_sowrd_hight)

      if ataque_key == pygame.K_LEFT:
        sowrd_rect = pygame.Rect(player_x - extended_left_right_sowrd_width,
                                 player_y + 15.5,
                                 extended_left_right_sowrd_width,
                                 left_right_sowrd_hight)
        for e in enemies:
          if sowrd_rect.colliderect(e.getrect()):
            e.kill()
            enemies.remove(e)
          if ataque_timer == 30:
            ataque_timer = 0
            flag_ataque = False
            sowrd_rect = pygame.Rect(
              player_x - (left_right_sowrd_width * 1.75), player_y + 15.5,
              left_right_sowrd_width, left_right_sowrd_hight)

      if ataque_key == pygame.K_RIGHT:
        sowrd_rect = pygame.Rect(
          player_x + extended_left_right_sowrd_width - 2, player_y + 15.5,
          extended_left_right_sowrd_width, left_right_sowrd_hight)
        for e in enemies:
          if sowrd_rect.colliderect(e.getrect()):
            e.kill()
            enemies.remove(e)
          if ataque_timer == 30:
            ataque_timer = 0
            flag_ataque = False
            sowrd_rect = pygame.Rect(player_x + (up_down_sowrd_hight * 1.75),
                                     player_y + 15.5, left_right_sowrd_width,
                                     left_right_sowrd_hight)

  # Renderiza o jogo
  window.fill(BLACK)

  #atualiza animação player
  current_time = pygame.time.get_ticks()
  if current_time - player_last_update >= player_animation_cooldown:
    player_frame += 1
    player_last_update = current_time
    if player_frame >= len(player_animation_list[player_action]):
      player_frame = 0

  for e in enemies:
    e.animate(current_time)

  #atualiza animação botao novo jogo
  current_time = pygame.time.get_ticks()
  if current_time - botao_novo_jogo_last_update >= botao_novo_jogo_animation_cooldown:
    botao_novo_jogo_frame += 1
    botao_novo_jogo_last_update = current_time
    if botao_novo_jogo_frame >= len(
        botao_novo_jogo_animation_list[botao_novo_jogo_action]):
      botao_novo_jogo_frame = 0

  if game_state == INTRO:
    #carrega a musica
    stage_song.stop()
    menu_song.play(-1)

    #carrega o background
    window.blit(background_menu, background_menu_rect)
    #intro_text = intro_font.render("META CITY", True, WHITE)
    #start_button = intro_font.render("Novo Jogo", True, BLACK)

    #intro_text_rect = intro_text.get_rect(center=(window_width // 2, window_height // 2 - 50))
    start_button_rect.center = (window_width // 2, (window_height // 2) + 10)

    #window.blit(intro_text, intro_text_rect)
    #pygame.draw.rect(window, WHITE, start_button_rect)
    window.blit(
      botao_novo_jogo_animation_list[botao_novo_jogo_action]
      [botao_novo_jogo_frame], (start_button_rect.x, start_button_rect.y - 64))
    #window.blit(start_button, start_button_rect)

  elif game_state == GAME:
    #carrega a musica
    menu_song.stop()
    stage_song.play(-1)

    #carrega o background
    window.blit(background_image, background_rect)

    #DEBUG mostra quadro de animação
    #window.blit(animation_list[action][frame],(0,0))

    # Inimigo e player
    #pygame.draw.rect(window, player_color, player_rect)
    player_surface.blit(player_animation_list[player_action][player_frame],
                        player_rect)
    #pygame.draw.rect(window, WHITE, enemy_rect)
    for e in enemies:
      e.render(background_image, background_rect, player_surface,
               player_animation_list, player_action, player_frame, player_rect)

    if sowrd_rect is not None:
      pygame.draw.rect(window, RED, sowrd_rect)
    if debug is True:
      speed_debug_text = speed_debug_font.render(str(player_speed), True,
                                                 WHITE)
      speed_debug_text_rect = speed_debug_text.get_rect(topleft=(0, 0))
      window.blit(speed_debug_text, speed_debug_text_rect)
  pygame.display.flip()

  # Limita os frames por segundo
  clock.tick(60)

# Sai do jogo
pygame.quit()
