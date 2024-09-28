import pygame
import random
pygame.init()
size = width, height = 600,550
screen = pygame.display.set_mode(size)
fpsclock = pygame.time.Clock()
game_font = pygame.font.SysFont('Arial', 44)
black = 0,0,0
white = 255,255,255
#obstacle car class
class Obstacle_car:
    """
    Obstacle car class includes all information for the obstacle cars movements.
    properties: obstacle cars image, rect, position, and speed
    methods: init(self,lane), move(self), rotate(self)
    """
    def __init__(self,lane,rotate):
        obstacle_cars = ["car_3_resized__3_-removebg-preview.png", "obicargreen.png","police car (1) - COPY.png", "truck.png"]
        self.image2 = pygame.image.load(random.choice(obstacle_cars)).convert_alpha()
        if self.image2 == obstacle_cars[0]:
            self.image2 = pygame.transform.scale(self.image2, (70,90))

        self.ob_rect = self.image2.get_rect()
        self.rotation = 0
        self.lane = lane
        if lane == 1:
            self.is_rotating = False
            self.ob_rect.centerx = width/2 - 80
            self.speed = [0,4]
            self.ob_rect.centery = 0 - 50
        elif lane == 2:
            self.is_rotating = False
            self.ob_rect.centerx = width/ 2 + 160
            self.ob_rect.centery = 0 -50
            self.speed = [0,5]
        elif lane == 3:
            self.is_rotating = False
            self.speed = [0,5]
            self.ob_rect.centerx = width/2 + 180
            self.ob_rect.centery = 0 - 50
        elif lane == 4:
             self.is_rotating = False
             self.ob_rect.centerx = width/ 2 - 150
             self.speed = [0,5]
             self.ob_rect.centery = 0 - 50
        elif lane == 5:
            self.is_rotating = False
            self.ob_rect.centerx = width/ 2 + 10
            self.speed = [0,5]
            self.ob_rect.centery = 0 - 50
        elif lane == 6:
            self.is_rotating = False
            self.ob_rect.centerx = width/2 + 30
            self.speed = [0,5]
            self.ob_rect.centery = 0 - 50
    def move(self):
           self.ob_rect = self.ob_rect.move(self.speed)
           if self.ob_rect.top > height:
                self.ob_rect.top = -1 * self.ob_rect.height
           if self.is_rotating:
                self.rotate()
    def rotate(self):
            inital_centerx = self.ob_rect.centerx
            intial_centery = self.ob_rect.centery
            self.rotation += 7.2
            if self.rotation > 360:
               self.rotation -= 360
            self.image3 = pygame.transform.rotate(self.image2, self.rotation)
            self.ob_rect = self.image3.get_rect()
            self.ob_rect.centerx = width/ 2 - 200+ (self.lane - 1) * 150
            self.ob_rect.centery  = intial_centery



class Player1:
    """
    player class includes all information for the player to play the game.
    properties: image,rect, speed
    methods: init(self), move(self), update(self), stop(self)
    """
    def __init__(self):
        self.image = pygame.image.load("maincarupdated - Copy.png").convert_alpha()
        #this changes the dimensions of the image
        self.image = pygame.transform.scale(self.image, (70,120))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(white)
        self.speed = [0,0]
        self.rect.centerx = width/2
        self.rect.bottom = height

    def move(self):
        #keeping the player from going off the screen
        if self.rect.top <= 0 and self.speed[1] < 0:
            self.speed[1] = 0
        if self.rect.bottom >= height and self.speed[1] > 0:
            self.speed[1] = 0
            #prevents the player from going off the road
        if self.rect.left <= 70 and self.speed[0] < 0:
            self.speed[0] = 0
        if self.rect.right >= 530 and self.speed[0] > 0:
            self.speed[0] = 0
        self.rect = self.rect.move(self.speed)

    def stop(self):
        self.speed = [0,0]
#road
road = pygame.image.load("road_image.jpg")
road_rect = road.get_rect()
road_rect.centerx = width/2
road_rect.bottom = height



player1 = Player1()
obstacle1 = [Obstacle_car(1, False), Obstacle_car(2, False)]
game = True
frame_counter = 0
black = 0,0,0
last_car = 0
car_delay = 0
#this is a difficulty assignment, as the frame count increases the difficuly level decreases resulting in more cars being added
difficulty = 100
while game:
    last_car += 1
    frame_counter += 1
    score = frame_counter
    #decreasing the difficulty level
    """if frame_counter > 400:
        difficulty -= 10
    elif frame_counter > 700:
        difficulty -= 10
    elif frame_counter > 1000:
        difficulty -= 10
    elif frame_counter > 2000:
        difficulty -= 10"""
    frame_image = game_font.render(f" Score:{frame_counter}", False, black)
    frame_rect = frame_image.get_rect()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player1.speed = [-4,0]
            elif event.key == pygame.K_RIGHT:
                player1.speed = [4,0]
            elif event.key == pygame.K_UP:
                player1.speed = [0, -4]
            elif event.key == pygame.K_DOWN:
                player1.speed = [0,4]
        if event.type == pygame.KEYUP:
            player1.speed = [0,0]
    road_rect = road_rect.move(0,4)
    if road_rect.top >= 0:
            road_rect.top  = road_rect.top - road_rect.height + height
    removed_cars = []
    player1.move()
    for cars in obstacle1:
        cars.move()
    #collection of cars that went off the screen
    for cars in obstacle1:
        if cars.ob_rect.top > height:
            removed_cars.append(cars)
    for car in removed_cars:
        obstacle1.remove(cars)
    if last_car > car_delay:
        obstacle_rects = []
        for car in obstacle1:
            obstacle_rects.append(car.ob_rect)
        new_obstacle = Obstacle_car(random.randint(1,6), False)
        while new_obstacle.ob_rect.collidelist(obstacle_rects) != -1:
            new_obstacle = Obstacle_car(random.randint(1,6), False)
        obstacle1.append(new_obstacle)
        last_car = 0
        #car adding, the difficulty level decides at what rate to add
        car_delay = random.randint(3,5) * 60
    black = 0,0,0
    screen.fill(white)
    screen.blit(road,road_rect)
    screen.blit(player1.image, player1.rect)
    screen.blit(frame_image, frame_rect)
    for cars in obstacle1:
        screen.blit(cars.image2,cars.ob_rect)
    #if the player collides with the obstacle cars, print gameover and exit the game
    for cars in obstacle1:
        if player1.rect.colliderect(cars.ob_rect):
          font_image = game_font.render(f"Game over! You scored {score}", False, black)
          font_rect = font_image.get_rect()
          font_rect.centerx = width/2
          font_rect.centery = height/2
          screen.blit(font_image,font_rect)
          game = False

    pygame.display.flip()
    fpsclock.tick(50)

#freezing the screen, after the collision.
while True:
    for event in pygame.event.get():
         if event.type == pygame.QUIT:
             exit()