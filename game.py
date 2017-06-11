import sys, pygame, random
import framework as fw
pygame.init()

SIZE = WIDTH, HEIGHT = 400, 440
FPS = 40
ROOM_FONT = pygame.font.SysFont("Avenir", 11)
UI_FONT = pygame.font.SysFont('Avenir',15)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('MYSTERY CLUEDO')

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

        textSurf = ROOM_FONT.render(self.room.name, 1, (0,0,0))
        textRect = textSurf.get_rect(center=(self.rect.width/2, self.rect.height/2))
        self.image.blit(textSurf, textRect)

class UIText(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,text):
        pygame.sprite.Sprite.__init__(self)

        self.text = text
        self.image = pygame.Surface((width,height))
        self.rect = self.image.get_rect(x=x,y=y)

        self.buildText()

    def buildText(self):
        self.textSurf = UI_FONT.render(self.text,1,(0,0,0))
        self.textRect = self.textSurf.get_rect()
        self.textRect.center = [self.rect.width/2,self.rect.height/2]

        self.image.fill((255,255,255))
        self.image.blit(self.textSurf,self.textRect)

    def updateText(self,text):
        self.text = text
        self.buildText()

class Button(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,text,clicked):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((width,height))
        self.rect = self.image.get_rect(x=x,y=y)

        self.text = text
        self.clicked = clicked

        self.buildText()
    
    def buildText(self):
        self.textSurf = UI_FONT.render(self.text,1,(0,0,0))
        self.textRect = self.textSurf.get_rect()
        self.textRect.center = [self.rect.width/2,self.rect.height/2]

        self.image.fill((180,180,180))
        self.image.blit(self.textSurf,self.textRect)

    def update(self):
        mx, my = pygame.mouse.get_pos()

        if self.rect.collidepoint((mx,my)):
            self.image.fill((190,190,190))
        else:
            self.image.fill((180,180,180))
        
        self.image.blit(self.textSurf,self.textRect)


class ActionToggle(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,options):
        pygame.sprite.Sprite.__init__(self)
        self.options = options
        self.index = 0

        self.image = pygame.Surface((width,height))
        self.rect = self.image.get_rect(x=x,y=y)

        self.buildText()
    
    def buildText(self):
        self.textSurf = UI_FONT.render(self.options[self.index],1,(0,0,0))
        self.textRect = self.textSurf.get_rect()
        self.textRect.center = [self.rect.width/2,self.rect.height/2]

        self.image.fill((255,255,255))
        self.image.blit(self.textSurf,self.textRect)

    def update(self):
        mx, my = pygame.mouse.get_pos()

        if self.rect.collidepoint((mx,my)):
            self.image.fill((230,230,230))
        else:
            self.image.fill((220,220,220))
        
        self.image.blit(self.textSurf,self.textRect)
    
    def clicked(self):
        if self.index + 1 < len(self.options):
            if self.options[self.index + 1] == '?':
                for group in self.groups():
                    for sprite in group:
                        if sprite.options[sprite.index] == '?':
                            self.index += 1

        
        self.index += 1
        if self.index >= len(self.options):
            self.index = 0
        
        self.buildText()


peopleGroup = pygame.sprite.Group()
roomGroup = pygame.sprite.Group()
choiceGroup = pygame.sprite.Group()
uiGroup = pygame.sprite.Group()

personInputList = []
roomInputList = []

game = fw.Game([
    fw.Room('DINING ROOM'),
    fw.Room('OBSERVATORY'),
    fw.Room('KITCHEN'),
    fw.Room('BEDROOM'),
    fw.Room('LIVING ROOM'),
    fw.Room('BASEMENT'),
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
    
    roomInputList.append(room.name)


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

    personInputList.append(person.name)

personChoiceButton = ActionToggle(0,240,WIDTH,40,personInputList + ['?'])
choiceGroup.add(personChoiceButton)
actionChoiceButton = ActionToggle(0,280,WIDTH,40,['ENTER','IN','LEAVE'] + ['?'])
choiceGroup.add(actionChoiceButton)
placeChoiceButton = ActionToggle(0,320,WIDTH,40,roomInputList + ['?'])
choiceGroup.add(placeChoiceButton)
timeChoiceButton = ActionToggle(0,360,WIDTH,40,[str(x * 0.5) for x in range(2, 21)] + ['?'])
choiceGroup.add(timeChoiceButton)

talkingToText = UIText(0,200,WIDTH,40,'')
uiGroup.add(talkingToText)

selectedPerson = None

def onEnterButtonClicked(self):
    global selectedPerson
    asking = selectedPerson
    who = personChoiceButton.options[personChoiceButton.index]
    what = actionChoiceButton.options[actionChoiceButton.index]
    where = placeChoiceButton.options[placeChoiceButton.index]
    when = timeChoiceButton.options[timeChoiceButton.index]

    for match in fw.askPerson(asking.memory,asking.name,who,what,where,when):
        print(match)
    
    selectedPerson = None
    talkingToText.updateText('')

enterButton = Button(0,400,WIDTH,40,'Ask',onEnterButtonClicked)
uiGroup.add(enterButton)

while 1:
    choiceGroup.update()
    uiGroup.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            mx, my = pygame.mouse.get_pos()
            for personSprite in peopleGroup:
                if personSprite.rect.collidepoint((mx,my)):
                    talkingToText.updateText('You are talking to ' + personSprite.person.name)
                    selectedPerson = personSprite.person
            for choiceSprite in choiceGroup:
                if choiceSprite.rect.collidepoint((mx,my)):
                    choiceSprite.clicked()
            for uiSprite in uiGroup:
                if uiSprite.rect.collidepoint((mx,my)):
                    uiSprite.clicked(uiSprite)
                


    screen.fill((255,255,255))
    roomGroup.draw(screen)
    peopleGroup.draw(screen)
    if(selectedPerson is not None):
        choiceGroup.draw(screen)
    uiGroup.draw(screen)
    pygame.display.flip()