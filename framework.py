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
        self.alive = True
        self.timeEnteredRoom = 1.0

class Game ():
    def __init__(self, r, p):
        self.rooms = r
        self.people = p
        for p in self.people:
            self.personEnter(p,1.0,random.randint(0,len(self.rooms)-1))
        self.murderer = random.choice(self.people)
        self.target = random.choice(self.people)
        self.timeOfDeath = random.choice([1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0])
        self.timeMurdererEnters = self.timeOfDeath - (float(random.randrange(1,4))/2)
        self.timeTargetEnters = self.timeOfDeath - (float(random.randrange(1,4))/2)
        self.placeOfDeath = random.randint(0,len(self.rooms)-1)
        self.initialise()
    
    def initialise(self,time=1.5):
        while time <= 10.0:

            if self.timeOfDeath == time:
                self.target.alive = False
                self.rooms[self.placeOfDeath].event(self.murderer.name,'KILL',time)
                self.rooms[self.placeOfDeath].event(self.target.name,'DIE',time)

            for person in self.people:
                if not person.alive:
                    continue

                if person is self.murderer and self.timeMurdererEnters == time:
                    newroom = self.placeOfDeath

                    if not self.personAt(person,newroom):
                        person = self.personLeave(person,time)
                        person = self.personEnter(person,time,newroom)

                elif person is self.target and self.timeTargetEnters == time:
                    newroom = self.placeOfDeath

                    if not self.personAt(person,newroom):
                        person = self.personLeave(person,time)
                        person = self.personEnter(person,time,newroom)
                
                
                else:
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
            return createReturnDict(checkWhoInRoom(memoryInput,askingInput,whereInput,whenInput),'checkWhoInRoom')
        elif whenInput == '?':
            return createReturnDict(checkWhenInRoom(memoryInput,askingInput,whoInput,whereInput),'checkWhenInRoom')
        elif whereInput == '?':
            return createReturnDict(checkWhereSeen(memoryInput,askingInput,whoInput,whenInput), 'checkWhereSeen')
        return {'type':'emptyIn','result':[]}
    else:
        matchList = []

        matching = getMatching(memoryInput,whoInput,whatInput,whereInput,whenInput)
        matchList += matching

        if len(matchList) == 0 and whatInput == '?':
            if whoInput in checkWhoInRoom(memoryInput,askingInput,whereInput,whenInput):
                matchList.append({'who':whoInput,'what':'IN','where':whereInput,'when':whenInput})
            

        return createReturnDict(matchList,'matched')

def createReturnDict(result,context):
    retval = {'type':context,'result':result}
    return retval

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

def handleResult(result,asker,who,what,where,when):
    retString = 'something\'s gone weird lol'
    res = result['result']
    if result['type'] == 'matchedIn':
        return asker + 'doesn\'t know.'
    if result['type'] == 'matched':
        retString = asker + ' saw '
        for per in range(len(res)):
            retString += res['who'] + ' ' + res['what'] + ' the ' + res['where'] + ' at ' + str(res['when'])
            if per < len(res) - 2:
                retString += ', '
            elif per < len(res) - 1:
                retString += ' and '
        retString += '.'
    elif result['type'] == 'checkWhoInRoom':
        if len(res) == 0:
            retString = asker + ' doesn\'t know.'
        else:
            retString = ''
            for per in range(len(res)):
                retString += res[per]
                if per < len(res) - 2:
                    retString += ', '
                elif per < len(res) - 1:
                    retString += ' and '
            if len(res) == 1:
                retString += ' was '
            else: 
                retString += ' were '
            retString += 'in the ' + where + ' at ' + when + '.'
    elif result['type'] == 'checkWhereSeen':
        if len(res) == 0:
            retString = asker + ' didn\'t see ' + who + '.'
        else:
            retString = 'According to ' + asker + ', ' + who + ' was in the '
            for per in range(len(res)):
                retString += res[per]
                if per < len(res) - 2:
                    retString += ', '
                elif per < len(res) - 1:
                    retString += ' and '
            retString += ' at ' + when + '.'
    elif result['type'] == 'checkWhenInRoom':
        if len(res) == 0:
            retString = asker + ' never saw ' + who + ' in the ' + where + '.'
        else:
            retString = who + ' was in the ' + where + ' from '
            for period in range(len(res)):
                retString += str(res[period]['START']) + '-' + str(res[period]['END'])
                if period < len(res) - 2:
                    retString += ', '
                elif period < len(res) - 1:
                    retString += ' and from '
                elif period == len(res) - 1:
                    retString += '.'
    return retString