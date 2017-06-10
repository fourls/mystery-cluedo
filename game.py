import sys, pygame, random
import framework as fw
pygame.init()

SIZE = WIDTH, HEIGHT = 400, 400
FPS = 40
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('mystery cluedo')

class Person(pygame.sprite.Sprite):
    def __init__(self, person, x, y):
       pygame.sprite.Sprite.__init__(self)
       self.person = person
       self.image = pygame.image.load('img/' + person.name + '.png')
       self.rect = self.image.get_rect()
       self.rect.x, self.rect.y = x, y

class Room(pygame.sprite.Sprite):
    def __init__(self,room, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.room = room
        self.image = pygame.image.load('img/room.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

fw.initialise()

peopleGroup = pygame.sprite.Group()
roomGroup = pygame.sprite.Group()

rx = 0
ry = 0
for room in fw.rooms:
    roomSprite = Room(room,rx,ry)
    roomGroup.add(roomSprite)

    rx += 100
    if rx >= 400:
        ry += 100
        rx = 0


for person in fw.people:
    px = 300
    py = 300
    for roomSprite in roomGroup:
        print(person.name + ' in ' + roomSprite.room.name + '? roomSprite.room.people = ' + str(roomSprite.room.people))
        for p2 in roomSprite.room.people:
            if p2['name'] == person.name:
                px = roomSprite.rect.x + ((roomSprite.room.people.index(p2)) * 20)
                py = roomSprite.rect.y + ((roomSprite.room.people.index(p2)) * 20)
                print(person.name + ' is in ' + roomSprite.room.name)
    
    print('x = ' + str(px) + ', y = ' + str(py))
    personSprite = Person(person, px, py)
    peopleGroup.add(personSprite)


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

    screen.fill((0,0,0))
    roomGroup.draw(screen)
    peopleGroup.draw(screen)
    pygame.display.flip()