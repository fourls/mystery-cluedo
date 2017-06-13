import unittest
from framework import *
'''
game = Game(
    [
        Room('DINING ROOM'),
        Room('OBSERVATORY'),
        Room('KITCHEN'),
        Room('BEDROOM'),
        Room('LIVING ROOM'),
        Room('BASEMENT'),
        Room('CLASSROOM'),
        Room('HALLWAY'),
        Room('SWIMMING POOL')
    ], 
    [
        Person('MUSTARD'),
        Person('BLUE'),
        Person('SCARLET'),
        Person('NAVY'),
        Person('GREEN')
    ]
)

while True:
    for match in game.askPerson(
        raw_input('Talk to: '),
        raw_input('Who: '),
        raw_input('What: '),
        raw_input('Where: '),
        float(raw_input('When: '))
    ):
        print(match)
'''

class TestGameInit(unittest.TestCase):
    def test_person_init(self):
        game = Game(
            [
                Room('DINING ROOM')
            ], 
            [
                Person('MUSTARD'),
                Person('BLUE'),
                Person('SCARLET'),
                Person('NAVY'),
                Person('GREEN')
            ]
        )
        people = ['MUSTARD','BLUE','SCARLET','NAVY','GREEN']

        for person in game.people:
            self.assertTrue(person.name in people)
            self.assertTrue(type(person.memory) is list)
            self.assertTrue(person.room == 0)
            self.assertEqual(person.room,0)
    def test_room_init(self):
        dining_room = Room('DINING ROOM')
        game = Game(
            [
                dining_room,
                Room('OBSERVATORY'),
                Room('KITCHEN'),
                Room('BEDROOM'),
                Room('LIVING ROOM'),
                Room('BASEMENT'),
                Room('CLASSROOM'),
                Room('HALLWAY'),
                Room('SWIMMING POOL')
            ], 
            [
                Person('MUSTARD')
            ]
        )

        self.assertEqual(game.rooms[0],dining_room)

        for room in game.rooms:
            self.assertTrue(type(room.name) is str)
            self.assertTrue(type(room.history) is list)
            self.assertTrue(type(room.people) is list)
            
class TestQuestionAsking(unittest.TestCase):
    def setUp(self):
        self.memory = [
            {'who':'MUSTARD','what':'ENTER','where':'DINING ROOM','when':1.0},
            {'who':'MUSTARD','what':'LEAVE','where':'DINING ROOM','when':2.5},
            {'who':'SCARLET','what':'IN','where':'OBSERVATORY','when':2.5},
            {'who':'MUSTARD','what':'ENTER','where':'OBSERVATORY','when':2.5},
            {'who':'MUSTARD','what':'LEAVE','where':'OBSERVATORY','when':7.0},
            {'who':'MUSTARD','what':'ENTER','where':'DINING ROOM','when':7.0},
            {'who':'MUSTARD','what':'LEAVE','where':'DINING ROOM','when':9.0},
            {'who':'MUSTARD','what':'ENTER','where':'SWIMMING POOL','when':9.0},
            {'who':'SCARLET','what':'IN','where':'SWIMMING POOL','when':9.0}
        ]

#   checkWhereSeen(memory,asking,who,when)

    def test_checkWhereSeen_when_you_enter_room(self):
        self.assertTrue(checkWhereSeen(self.memory,'MUSTARD','MUSTARD',1.0) == ['DINING ROOM'])
    
    def test_checkWhereSeen_when_you_are_in_room(self):
        self.assertTrue(checkWhereSeen(self.memory,'MUSTARD','MUSTARD',2.0) == ['DINING ROOM'])
    
    def test_checkWhereSeen_when_you_leave_and_enter_a_new_room(self):
        self.assertTrue(checkWhereSeen(self.memory,'MUSTARD','MUSTARD',2.5) == ['OBSERVATORY'])
    
    def test_checkWhereSeen_when_somebody_else_is_in_on_enter(self):
        self.assertTrue(checkWhereSeen(self.memory,'MUSTARD','SCARLET',2.5) == ['OBSERVATORY'])

    def test_checkWhereSeen_when_you_leave_but_they_stay(self):
        self.assertTrue(len(checkWhereSeen(self.memory,'MUSTARD','SCARLET',7.0)) == 0)

    def test_checkWhereSeen_when_you_are_in_room_at_end_of_game(self):
        self.assertTrue(checkWhereSeen(self.memory,'MUSTARD','SCARLET',10.0) == ['SWIMMING POOL'])

#   checkWhoInRoom(memory,where,when)

    def test_checkWhoInRoom_when_you_enter_room(self):
        self.assertTrue(checkWhoInRoom(self.memory,'MUSTARD','DINING ROOM',1.0) == ['MUSTARD'])
    
    def test_checkWhoInRoom_when_you_leave_room(self):
        self.assertTrue(checkWhoInRoom(self.memory,'MUSTARD','DINING ROOM',2.5) == [])
    
    def test_checkWhoInRoom_when_you_enter_a_room_they_are_in(self):
        self.assertTrue(sorted(checkWhoInRoom(self.memory,'MUSTARD','OBSERVATORY',2.5)) == sorted(['MUSTARD','SCARLET']))
    
    def test_checkWhoInRoom_after_you_have_left(self):
        self.assertTrue(checkWhoInRoom(self.memory,'MUSTARD','OBSERVATORY',7.5) == [])
    
    def test_checkWhoInRoom_when_multiple_people_are_in_room(self):
        self.assertTrue(sorted(checkWhoInRoom(self.memory,'MUSTARD','OBSERVATORY',6.0)) == sorted(['MUSTARD','SCARLET']))
    
#   checkWhenInRoom(memory,asking,who,where)

    def test_checkWhenInRoom_when_you_visit_multiple_times(self):
        self.assertTrue(checkWhenInRoom(self.memory,'MUSTARD','MUSTARD','DINING ROOM') == [{'START':1.0,'END':2.5},{'START':7.0,'END':9.0}])
    
    def test_checkWhenInRoom_when_you_never_visit(self):
        self.assertTrue(checkWhenInRoom(self.memory,'MUSTARD','MUSTARD','LIVING ROOM') == [])
    
    def test_checkWhenInRoom_when_you_enter(self):
        self.assertTrue(checkWhenInRoom(self.memory,'MUSTARD','MUSTARD','OBSERVATORY') == [{'START':2.5,'END':7.0}])
    
    def test_checkWhenInRoom_when_you_leave_before_them(self):
        self.assertTrue(checkWhenInRoom(self.memory,'MUSTARD','SCARLET','OBSERVATORY') == [{'START':2.5,'END':7.0}])

#   getMatching(memory,who,what,where,when)

    def test_getMatching_when(self):
        self.assertTrue(sorted(getMatching(self.memory,'MUSTARD','ENTER','DINING ROOM','?')) == sorted([{'who':'MUSTARD','what':'ENTER','where':'DINING ROOM','when':1.0},{'who':'MUSTARD','what':'ENTER','where':'DINING ROOM','when':7.0}]))
    
    def test_getMatching_where(self):
        gmResult = sorted(getMatching(self.memory,'MUSTARD','ENTER','?',2.5))
        expected = sorted([{'who':'MUSTARD','what':'ENTER','where':'OBSERVATORY','when':2.5}])
        self.assertTrue(gmResult == expected)
    
    def test_getMatching_who(self):
        self.assertTrue(sorted(getMatching(self.memory,'?','ENTER','OBSERVATORY',2.5)) == sorted([{'who':'MUSTARD','what':'ENTER','where':'OBSERVATORY','when':2.5}]))
        
    def test_getMatching_what(self):
        gmResult = sorted(getMatching(self.memory,'SCARLET','?','SWIMMING POOL',9.0))
        expected = sorted([{'who':'SCARLET','what':'IN','where':'SWIMMING POOL','when':9.0}])
        self.assertTrue(gmResult == expected)

#   askPerson(memory,asking,who,what,where,when)

    def test_askPerson_calls_checkWhereSeen(self):
        apResult = askPerson(self.memory,'MUSTARD','MUSTARD','IN','?',1.0)
        expected = createReturnDict(['DINING ROOM'],'checkWhereSeen')
        print(apResult)
        self.assertTrue(apResult == expected)
    
    def test_askPerson_calls_checkWhoInRoom(self):
        apResult = askPerson(self.memory,'MUSTARD','?','IN','OBSERVATORY',2.5)
        expected = createReturnDict(['SCARLET','MUSTARD'],'checkWhoInRoom')
        print(apResult)
        self.assertTrue(apResult == expected)

    def test_askPerson_calls_checkWhenInRoom(self):
        apResult = askPerson(self.memory,'MUSTARD','MUSTARD','IN','OBSERVATORY','?')
        expected = createReturnDict([{'START':2.5,'END':7.0}],'checkWhenInRoom')
        print(apResult)
        self.assertTrue(apResult == expected)
    
    def test_askPerson_calls_getMatching_what(self):
        mem = self.memory
        asking = 'MUSTARD'
        who = 'MUSTARD'
        what = '?'
        where = 'OBSERVATORY'
        when = 7.0

        apResult = askPerson(self.memory,asking,who,what,where,when)
        gmResult = createReturnDict(getMatching(self.memory,who,what,where,when),'matched')
        self.assertTrue(apResult == gmResult)
    
    def test_askPerson_calls_getMatching_who(self):
        mem = self.memory
        asking = 'MUSTARD'
        who = '?'
        what = 'LEAVE'
        where = 'OBSERVATORY'
        when = 5.5

        apResult = askPerson(self.memory,asking,who,what,where,when)
        gmResult = createReturnDict(getMatching(self.memory,who,what,where,when),'matched')
        self.assertTrue(apResult == gmResult)
    
    def test_askPerson_calls_getMatching_when(self):
        mem = self.memory
        asking = 'MUSTARD'
        who = 'SCARLET'
        what = 'LEAVE'
        where = 'OBSERVATORY'
        when = '?'

        apResult = askPerson(self.memory,asking,who,what,where,when)
        gmResult = createReturnDict(getMatching(self.memory,who,what,where,when),'matched')
        self.assertTrue(apResult == gmResult)

    def test_askPerson_calls_getMatching_where(self):
        mem = self.memory
        asking = 'MUSTARD'
        who = 'SCARLET'
        what = 'LEAVE'
        where = '?'
        when = 5.5

        apResult = askPerson(self.memory,asking,who,what,where,when)
        gmResult = createReturnDict(getMatching(self.memory,who,what,where,when),'matched')
        self.assertTrue(apResult == gmResult)
        
    def test_askPerson_tells_if_person_in_room_at_time(self):
        gmResult = askPerson(self.memory,'MUSTARD','SCARLET','?','OBSERVATORY',4.5)
        expected = createReturnDict([{'who':'SCARLET','what':'IN','where':'OBSERVATORY','when':4.5}],'matched')
        self.assertTrue(gmResult == expected)
    
#   createReturnDict(result,context)
    def test_createReturnDict(self):
        result = [{'who':'SCARLET','what':'IN','where':'OBSERVATORY','when':4.5}]
        context = 'matched'
        self.assertTrue(createReturnDict(result,context) == {'type':context,'result':result})

if __name__ == '__main__':
    unittest.main()