import pygame
import spritesheet

class Enemy ():  
  def __init__(self, x, y, last_update):
    self.x = x
    self.y = y
    self.last_update = last_update
    self.colided = False
    self.step = 5
    self.rect = pygame.Rect(x, y, 32, 32)
    self.killed = False
    self.side = None
    self.old_side = None
    self.frame = -99
    self.frame_limit = -99
    self.animation_steps = [7,1,7,1,7,1,7]
    self.action = 0
    self.animation_cooldown = 100
    self.animation_list = []
    self.frame = 0
    self.step_counter = 0
    self.surface = pygame.display.set_mode((1024, 768))

    for animations in self.animation_steps:
      temp_img_list = []
      for _ in range(animations):
        temp_img_list.append(spritesheet.SpriteSheet(pygame.image.load('enemy_sheet.png').convert_alpha()).get_image(self.step_counter,32,32,1,(0, 255, 0)))
        self.step_counter += 1
      self.animation_list.append(temp_img_list)
    print(self.animation_list)
    
    
  def isdead(self):
    return self.killed

  def kill(self):
    self.rect = pygame.Rect(0,0,self.x,self.y)
    self.killed = True

  def directionChanged(self, newdirection, olddirection):
    if newdirection != olddirection:
      return True
    return False

  def knockback(self):
    if self.colided is True:
      if self.side == "side_up":
        self.y -= 2
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
      if self.side == "side_down":
        self.y += 2
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
      if self.side == "side_left":
        self.x += 2
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
      if self.side == "side_right":
        self.x -= 2
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
    
  def update(self, player_x, player_y):
    if self.isdead() == False and self.colided == False:
      player_vector = pygame.math.Vector2(player_x, player_y)
      enemy_vector = pygame.math.Vector2(self.x, self.y)
      new_enemy_vector = pygame.math.Vector2(self.x, self.y)
    
      direction_vector = (player_vector - enemy_vector) / 70
      enemy_step_distance = self.step  * 0.5
      new_enemy_vector = enemy_vector + direction_vector * enemy_step_distance

      animation_vector = pygame.Vector2(self.x, self.y)
      animation_vector = enemy_vector + direction_vector

      old_enemy_x = animation_vector.x
      old_enemy_y = animation_vector.y

      new_enemy_x = new_enemy_vector.x
      new_enemy_y = new_enemy_vector.y

      self.x = new_enemy_x
      self.y = new_enemy_y
    
      self.rect = pygame.Rect(self.x, self.y, 32, 32)

      #Horizontal
      if abs(old_enemy_x - player_x) > abs(old_enemy_y - player_y):
        #Left
        if old_enemy_x - player_x > 0:
          self.side = "side_left"
          if self.directionChanged(self.side, self.old_side) is True:
            self.old_side = self.side
            print(self.side)
        #Right
        if old_enemy_x - player_x < 0:
          self.side = "side_right"
          if self.directionChanged(self.side, self.old_side) is True:
            self.old_side = self.side
            print(self.side)
      #Vertical
      if abs(old_enemy_x - player_x) < abs(old_enemy_y - player_y):
        #Up
        if old_enemy_y - player_y > 0:
          self.side = "side_up"
          if self.directionChanged(self.side, self.old_side) is True:
            self.old_side = self.side
            print(self.side)
        #Down        
        if old_enemy_y - player_y < 0:
          self.side = "side_down"
          if self.directionChanged(self.side, self.old_side) is True:
            self.old_side = self.side
            print(self.side)

      if self.side == "side_down":
        self.action = 0
      if self.side == "side_right":
        self.action = 6
      if self.side == "side_left":
        self.action = 2
      if self.side == "side_up":
        self.action = 4
        
  def animate(self, tick):
    if tick - self.last_update >= self.animation_cooldown:
      self.frame += 1
      self.last_update = tick
      if self.frame >= len(self.animation_list[self.action]):
        self.frame = 0
    
  def render(self, background_image, background_rect, player_surface, player_animation_list, player_action, player_frame, player_rect):
    self.surface.blit(self.animation_list[self.action][self.frame], self.rect)

    if self.isdead() is not False:
      self.surface.blit(self.animation_list[1][0],self.rect)
      self.surface.blit(background_image, background_rect)
      player_surface.blit(player_animation_list[player_action][player_frame], player_rect)

      

  def getrect(self):
    return self.rect

  def setcolided(self, state):
    self.colided = state

  def getcolided(self):
    return self.colided
    