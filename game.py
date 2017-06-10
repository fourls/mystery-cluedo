import sys, pygame
import framework as fw
pygame.init()

SIZE = WIDTH, HEIGHT = 320, 240
FPS = 40
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('mystery cluedo')

class Person(pygame.sprite.Sprite):

    def __init__(self, name, x, y):
       pygame.sprite.Sprite.__init__(self)
       self.name = name
       self.image = pygame.image.load('img/' + name + '.png')
       self.rect = self.image.get_rect()
       self.rect.x, self.rect.y = x, y


peopleGroup = pygame.sprite.Group()

x = 10
y = 10
for person in fw.people:
    personSprite = Person(person.name, x, y)
    peopleGroup.add(personSprite)

    x += 30
    y += 30

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

    screen.fill((0,0,0))
    peopleGroup.draw(screen)
    pygame.display.flip()