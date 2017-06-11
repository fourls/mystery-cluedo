import random

class Room ():
    def __init__(self,name):
        self.name = name
        self.history = []
        self.people = []
    
    def event(self,name,action,time):
        if action == 'ENTER':
            self.people.append({'name':name,'time':time})
        elif action == 'LEAVE':
            for per in self.people:
                if per['name'] == name:
                    self.people.remove(per)

        self.history.append({'who':name,'what':action,'when':time,'where':self.name})

class Person ():
    def __init__(self, name):
        self.name = name
        self.memory = []
        self.room = -1
        self.timeEnteredRoom = 1.0
    
    '''
    def leave(self,time):
        rooms[self.room].event(self.name,'LEAVE',time)
        self.getHistoryOfRoom()
        self.room = None

    def enter(self,time,room):
        self.room = room
        rooms[self.room].event(self.name,'ENTER',time)
        for per in rooms[self.room].people:
            if per['name'] != self.name: 
                timeOfEvent = time
                if per['time'] != time:
                    self.memory.append({'who':per['name'],'what':'IN','when':timeOfEvent,'where':rooms[self.room].name})
                else:
                    for mem in self.memory:
                        if not (mem['who'] == per['name'] and mem['when'] == timeOfEvent):
                            self.memory.append({'who':per['name'],'what':'ENTER','when':timeOfEvent,'where':rooms[self.room].name})
                    

        self.timeEnteredRoom = time
    
    def at(self,room):
        return self.room == room
    
    def getHistoryOfRoom(self):

        historyWhileInRoom = []
        for event in rooms[self.room].history:
            if event['when'] >= self.timeEnteredRoom:
                historyWhileInRoom.append(event)
        self.memory += historyWhileInRoom
    '''


class Game ():
    def __init__(self, r, p):
        self.rooms = r
        self.people = p
        for p in self.people:
            self.personEnter(p,1.0,random.randint(0,len(self.rooms)-1))
        self.initialise()
    
    def initialise(self,time=1.5):
        while time <= 10.0:
            for person in self.people:
                action = whatPersonDoes()
                if action == 'LEAVE':
                    newroom = random.randint(0,len(self.rooms) - 1)
                    if not self.personAt(person,newroom):
                        person = self.personLeave(person,time)
                        person = self.personEnter(person,time,newroom)

            time += 0.5
        for person in self.people: 
            person = self.givePersonHistoryOfRoom(person,person.room)
        
        return True

    def personAt(self,person,room):
        return person.room == room

    def personEnter(self,person,time,room):
        person.room = room
        self.rooms[room].event(person.name,'ENTER',time)
        for per in self.rooms[room].people:
            if per['name'] != person.name: 
                timeOfEvent = time
                if per['time'] != time:
                    person.memory.append({'who':per['name'],'what':'IN','when':timeOfEvent,'where':self.rooms[room].name})
                else:
                    for mem in person.memory:
                        if not (mem['who'] == per['name'] and mem['when'] == timeOfEvent):
                            person.memory.append({'who':per['name'],'what':'ENTER','when':timeOfEvent,'where':self.rooms[room].name})
                    
        person.timeEnteredRoom = time
        return person
    
    def personLeave(self,person,time):
        self.rooms[person.room].event(person.name,'LEAVE',time)
        self.givePersonHistoryOfRoom(person,person.room)
        person.room = None
        return person

    def givePersonHistoryOfRoom(self,person,room):
        historyWhileInRoom = []

        for event in self.rooms[room].history:
            if event['when'] >= person.timeEnteredRoom:
                historyWhileInRoom.append(event)
        person.memory += historyWhileInRoom

        return person

def askPerson(memoryInput, askingInput, whoInput, whatInput, whereInput, whenInput):
    if whenInput != '?':
        whenInput = float(whenInput)


    if whatInput == 'IN':
        if whoInput == '?':
            return checkWhoInRoom(memoryInput,askingInput,whereInput,whenInput)
        elif whenInput == '?':
            return checkWhenInRoom(memoryInput,askingInput,whoInput,whereInput)
        elif whereInput == '?':
            return checkWhereSeen(memoryInput,askingInput,whoInput,whenInput)
        return []
    else:
        matchList = []

        matching = getMatching(memoryInput,whoInput,whatInput,whereInput,whenInput)
        matchList += matching

        return matchList

def whatPersonDoes():
    percent = random.random()
    if percent <= 0.2:
        return 'LEAVE'
    elif percent <= 0.5:
        return 'DO'
    else:
        return 'NOTHING'

# ____ in PLACE at TIME
def checkWhoInRoom(memory,asking,where,when):
    peopleInRoom = []

    for i in range(len(memory)):
        if memory[i]['where'] == where:
            if memory[i]['what'] == 'ENTER' or memory[i]['what'] == 'IN':
                if memory[i]['when'] <= when:
                    peopleInRoom.append(memory[i]['who'])
            elif memory[i]['what'] == 'LEAVE':
                if memory[i]['when'] <= when:
                    peopleInRoom.remove(memory[i]['who'])
                    if memory[i]['who'] == asking:
                        peopleInRoom = []
    
    return peopleInRoom

# NAME in PLACE at _____
def checkWhenInRoom(memory,asking,who,where):
    placesSeen = []

    for i in range(len(memory)):
        if memory[i]['where'] == where:
            if (memory[i]['what'] == 'ENTER' or memory[i]['what'] == 'IN') and memory[i]['who'] == who:
                placesSeen.append({'START':memory[i]['when'],'END':10.0})
            elif memory[i]['what'] == 'LEAVE' and (memory[i]['who'] == who or memory[i]['who'] == asking):
                placesSeen[len(placesSeen)-1]['END'] = memory[i]['when']
    

    return placesSeen

# NAME in _______ at TIME
def checkWhereSeen(memory,asking,who,when):
    placesSeen = []

    for i in range(len(memory)):
        if memory[i]['when'] <= when:
            if (memory[i]['what'] == 'ENTER' or memory[i]['what'] == 'IN') and memory[i]['who'] == who:
                placesSeen.append(memory[i]['where'])
            elif memory[i]['what'] == 'LEAVE' and memory[i]['when'] <= when and (memory[i]['who'] == who or memory[i]['who'] == asking):
                if memory[i]['where'] in placesSeen:
                    placesSeen.remove(memory[i]['where'])
    

    return placesSeen

def getMatching(mem,who,what,where,when):
    matchList = []
    
    for item in mem:
        Ywho = False
        Ywhat = False
        Ywhen = False
        Ywhere = False

        if item['who'] == who or who == '?':
            Ywho = True
        if item['what'] == what or what == '?':
            Ywhat = True
        if str(item['when']) == str(when) or when == '?':
            Ywhen = True
        if item['where'] == where or where == '?':
            Ywhere = True
        
        if Ywho and Ywhat and Ywhen and Ywhere:
            matchList.append(item)

    return matchList