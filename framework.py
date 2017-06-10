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
    def __init__(self, name, room):
        self.name = name
        self.memory = []
        self.timeEnteredRoom = 1.0
        self.enter(1.0,room)
    
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

    #def sees(self,name,action,time,place):
    #    self.memory.append({'who':name,'what':action,'when':time,'where':place})

rooms = [
    Room('DINING ROOM'),
    Room('OBSERVATORY'),
    Room('KITCHEN'),
    Room('BEDROOM'),
    Room('LIVING ROOM'),
    Room('BASEMENT')
]

people = [
    Person('MUSTARD',0),
    Person('CYAN',0),
    Person('SCARLET',0),
    Person('BLACK',0),
    Person('WHITE',0)
]

def initialise(time=1.5):
    while time <= 10.0:
        for person in people:
            action = whatPersonDoes(person)
            if action == 'LEAVE':
                newroom = random.randint(0,len(rooms) - 1)
                if not person.at(newroom):
                    person.leave(time)
                    person.enter(time,newroom)

        time += 0.5
        #print(time)
    for person in people: 
        person.getHistoryOfRoom()

def whatPersonDoes(person):
    percent = random.random()
    if percent <= 0.2:
        return 'LEAVE'
    elif percent <= 0.5:
        return 'DO'
    else:
        return 'NOTHING'

def checkIfPersonInRoom(asker,person,time,room):
    times = []

    for mem in asker.memory:
        if mem['who'] == person and mem['where'] == room:
            if mem['what'] == 'ENTER' or mem['what'] == 'IN':
                times.append({'what':'ENTER','when':mem['when']})
            if mem['what'] == 'LEAVE':
                times.append({'what':'LEAVE','when':mem['when']})
        if mem['who'] == asker.name and mem['where'] == room and mem['what'] == 'LEAVE':
            times.append({'what':'LEAVE','when':mem['when']})
    
    lastEnter = -1
    for i in range(len(times)):
        if times[i]['what'] == 'ENTER':
            lastEnter = i;
        elif times[i]['what'] == 'LEAVE':
            if lastEnter is not -1:
                if times[lastEnter]['when'] <= float(time) and times[i]['when'] > float(time):
                    return True
        elif i >= len(times) - 1:
            if times[lastEnter]['when'] <= float(time):
                return True
    return False

def getMatching(per,who,what,when,where):
    matchList = []

    if what == 'IN':
        if when == '?':
            matchList = getMatching(per,who,'ENTER',when,where) + getMatching(per,who,'LEAVE',when,where)
        else: 
            if checkIfPersonInRoom(per,who,when,where):
                matchList.append({'who':who,'what':'IN','when':when,'where':where})

    lis = per.memory
    for item in lis:
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
    
    if what == '?':
        if checkIfPersonInRoom(per,who,when,where):
            skip = False
            for match in matchList:
                if (match['who'] == who and str(match['when']) == str(when)):
                    skip = True
            
            if not skip:
                matchList.append({'who':who,'what':'IN','when':float(when),'where':where})
    
    return matchList

def askPerson():
    personInput = raw_input('Talking to: ')
    whoInput = raw_input('Who: ')
    whatInput = raw_input('What: ')
    whereInput = raw_input('Where: ')
    whenInput = raw_input('When: ')

    for person in people:
        if person.name == personInput:
            matching = getMatching(person,whoInput,whatInput,whenInput,whereInput)
            if len(matching) == 0:
                print(person.name + " says they don't know.")
            else:
                for match in matching:
                    print(person.name + ' says they saw ' + match['who'] + ' ' + match['what'] + ' the ' + match['where'] + ' at ' + str(match['when']))

#--------- main run --------#
initialise()

for person in people:
    #print(person.name)

    for mem in person.memory:
        print(person.name + " saw " + str(mem["who"]) + " " + str(mem["what"]) + " the " + str(mem["where"]) + " at " + str(mem["when"]))
    
    print("\n")

#for room in rooms:
#    #print(room.name)
#
#    for his in room.history:
#        print(room.name + " saw " + his["who"] + " " + his["what"] + " the " + his["where"] + " at " + str(his["when"]))
#
#    print("\n")

while True:
    askPerson()
    print("\n")
    #personIndex = int(raw_input('Asking #: '))
    #if(checkIfPersonInRoom(people[personIndex],raw_input('Person: '),raw_input('Time: '),raw_input('Room: '))):
    #    print('They were there then.')
    #else:
    #    print('They weren\'t there then.')