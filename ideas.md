# INITIALISATION STEPS
  1. rooms initialised
  2. people initialised
  3. the day is programatically written from start to finish
    a. Iterates through every Room


# EXAMPLE ITERATION
## Method A - via Room
###  DINING ROOM
    MUSTARD ENTERS 3:30 DINING ROOM 
    SCARLET ENTERS 3:30 DINING ROOM
    SCARLET LEAVES 4:00 DINING ROOM
    MUSTARD LEAVES 4:30 DINING ROOM
## Method B - via Time
### 3:30
    MUSTARD ENTERS 3:30 DINING ROOM
    SCARLET ENTERS 3:30 DINING ROOM
    SCARLET LEAVES 4:00 DINING ROOM
    SCARLET ENTERS 4:00 KITCHEN
    MUSTARD LEAVES 4:30 DINING ROOM
    MUSTARD ENTERS 4:30 OBSERVATORY

# PSEUDOCODE
# Functions
### `initialisation_loop(time=1.00)`
```python
while time < 10.00:
    for person in people:
        action = what_person_does(person)
        if action == 'LEAVE':
            person.leave(time)
            person.enter(time,random_room)
        elif action == 'DO':
            person.do(whatever)
    
    time += 0.50
```
### `what_person_does(person)`
```python
percent = random_percentage()

if percent <= 20%:
    return 'LEAVE'
elif percent <= 50%:
    return 'DO'
else
    return 'NOTHING'
```
### `person.leave(time)`
```python
for person in people:
    if person.at(this.room):
        person.sees(this.name,'LEAVES',time,this.room)
        
this.room = None
```
### `person.sees(name,action,time,place)`
```python
this.memory += {'who':name,'what':action,'when':time,'where':place}
```
### `person.enter(time,room)`
```python
this.room = room
for person in people:
    if person.at(this.room):
        person.sees(this.name,'ENTERS',time,this.room)

```
## Classes
```python
Day = {
  'rooms': [],
  'people': []
}

Room = {
  'name': 'DINING ROOM'
}

Person = {
  'name': 'MUSTARD',
  'room': None,
  'memory': [
    {
      'who': 'MUSTARD',
      'what': 'ENTERS',
      'when': '3:30',
      'where': 'DINING ROOM'
    },
    {
      'who': 'SCARLET',
      'what': 'ENTERS',
      'when': '3:30',
      'where': 'DINING ROOM'
    },
    {
      'who': 'SCARLET',
      'what': 'LEAVES',
      'when': '4:00',
      'where': 'DINING ROOM'
    },
    {
      'who': 'MUSTARD',
      'what': 'LEAVES',
      'when': '4:30',
      'where': 'DINING ROOM'
    }
  ]
}
```

# Checking if somebody is in a room
    MUSTARD IN DINING ROOM 4.0
    ? IN DINING ROOM 4.0
    MUSTARD ? DINING ROOM 4.0
    MUSTARD IN ? 4.0
    MUSTARD IN DINING ROOM ?

### `checkIfInRoom(memory,who,what,where,when)`
```python
if who == '?':
    peopleInRoom = []
    lastEnter = {}
    for i in range(len(memory)):
        if memory[i]['what'] == 'ENTER':
            lastEnter[memory[i]['who']] = i;
        elif memory[i]['what'] == 'LEAVE':
            if lastEnter[memory[i]['who']] is not None:
                if memory[lastEnter[memory[i]['who']]]['when'] <= float(when) and memory[i]['when'] > float(when):
                    peopleInRoom.append(memory[i]['who'])
                    lastEnter[memory[i]['who']] = None
        elif i >= len(times) - 1:
                for key, value in lastEnter.iteritems():
                    if memory[value]['when'] <= float(when):
                        peopleInRoom.append(key)
elif what == '?':
    pass
elif where == '?':
    pass
elif when == '?':
    pass
```