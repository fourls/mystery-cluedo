import sys, pygame, random
import framework as fw
pygame.init()

SIZE = WIDTH, HEIGHT = 400, 400
FPS = 40
FONT = pygame.font.SysFont("Arial", 10)
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

        if self.rect.x % 200 != 0:
            self.image = pygame.image.load('img/room-alt.png')

        textSurf = FONT.render(self.room.name, 1, (0,0,0))
        textRect = textSurf.get_rect(center=(self.rect.width/2, self.rect.height/2))
        self.image.blit(textSurf, textRect)

peopleGroup = pygame.sprite.Group()
roomGroup = pygame.sprite.Group()

game = fw.Game([
    fw.Room('DINING ROOM'),
    fw.Room('OBSERVATORY'),
    fw.Room('KITCHEN'),
    fw.Room('BEDROOM'),
    fw.Room('LIVING ROOM'),
    fw.Room('BASEMENT'),
    fw.Room('CLASSROOM'),
    fw.Room('HALLWAY'),
    fw.Room('SWIMMING POOL')
],[
    fw.Person('MUSTARD'),
    fw.Person('BLUE'),
    fw.Person('SCARLET'),
    fw.Person('NAVY'),
    fw.Person('GREEN')
])

rx = 0
ry = 0
for room in game.rooms:
    roomSprite = Room(room,rx,ry)
    roomGroup.add(roomSprite)

    rx += 100
    if rx >= 400:
        ry += 100
        rx = 0


for person in game.people:
    px = 300
    py = 300
    for roomSprite in roomGroup:
        for p2 in roomSprite.room.people:
            if p2['name'] == person.name:
                px = roomSprite.rect.x + ((roomSprite.room.people.index(p2)) * 20)
                py = roomSprite.rect.y + 20 + ((roomSprite.room.people.index(p2)) * 20)
    
    personSprite = Person(person, px, py)
    peopleGroup.add(personSprite)


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            mx, my = pygame.mouse.get_pos()
            for personSprite in peopleGroup:
                if personSprite.rect.collidepoint((mx,my)):
                    for match in fw.askPerson(personSprite.person.memory,raw_input('who: '),raw_input('what: '),raw_input('where: '),float(raw_input('when: '))):
                        print(match)

    screen.fill((0,0,0))
    roomGroup.draw(screen)
    peopleGroup.draw(screen)
    pygame.display.flip()