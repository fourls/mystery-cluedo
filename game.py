import sys, pygame
pygame.init()

SIZE = WIDTH, HEIGHT = 320, 240
FPS = 40
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('hey look its a box')

class Person(pygame.sprite.Sprite):

    def __init__(self, color):
       pygame.sprite.Sprite.__init__(self)

       self.image = pygame.image.load('img/' + color + '.png')
       self.rect = self.image.get_rect()


peopleGroup = pygame.sprite.Group()
personSprite = Person('green')
peopleGroup.add(personSprite)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

    screen.fill((0,0,0))
    peopleGroup.draw(screen)
    pygame.display.flip()