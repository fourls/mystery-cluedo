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
            {'who':'SCARLET','what':'LEAVE','where':'OBSERVATORY','when':5.5},
            {'who':'MUSTARD','what':'LEAVE','where':'OBSERVATORY','when':7.0},
            {'who':'MUSTARD','what':'ENTER','where':'DINING ROOM','when':7.0}
        ]

    def test_if_person_in_unknown_at_time(self):
        self.assertTrue(checkWhereSeen(self.memory,'MUSTARD',1.0) == ['DINING ROOM'])
        self.assertTrue(checkWhereSeen(self.memory,'MUSTARD',2.0) == ['DINING ROOM'])
        self.assertTrue(checkWhereSeen(self.memory,'MUSTARD',2.5) == ['OBSERVATORY'])
        self.assertTrue(checkWhereSeen(self.memory,'SCARLET',3.0) == ['OBSERVATORY'])
        self.assertTrue(len(checkWhereSeen(self.memory,'SCARLET',6.0)) == 0)

    def test_if_unknown_in_place_at_time(self):
        self.assertTrue(checkWhoInRoom(self.memory,'DINING ROOM',1.0) == ['MUSTARD'])
        self.assertTrue(checkWhoInRoom(self.memory,'DINING ROOM',2.5) == [])
        self.assertTrue(checkWhoInRoom(self.memory,'OBSERVATORY',2.5).sort() == ['MUSTARD','SCARLET'].sort())
        self.assertTrue(checkWhoInRoom(self.memory,'OBSERVATORY',5.5) == ['MUSTARD'])
        self.assertTrue(checkWhoInRoom(self.memory,'OBSERVATORY',6.0) == ['MUSTARD'])
    
    def test_if_person_in_place_at_unknown(self):
        self.assertTrue(checkWhenInRoom(self.memory,'MUSTARD','DINING ROOM') == [{'START':1.0,'END':2.5},{'START':7.0,'END':10.0}])
        self.assertTrue(checkWhenInRoom(self.memory,'MUSTARD','LIVING ROOM') == [])
        self.assertTrue(checkWhenInRoom(self.memory,'MUSTARD','OBSERVATORY') == [{'START':2.5,'END':7.0}])
        self.assertTrue(checkWhenInRoom(self.memory,'SCARLET','OBSERVATORY') == [{'START':2.5,'END':5.5}])
    
    def test_get_matching(self):
        self.assertTrue(getMatching(self.memory,'MUSTARD','ENTER','DINING ROOM','?').sort() == [{'who':'MUSTARD','what':'ENTER','where':'DINING ROOM','when':1.0},{'who':'MUSTARD','what':'ENTER','where':'DINING ROOM','when':7.0}].sort())
        self.assertTrue(getMatching(self.memory,'SCARLET','LEAVE','?',5.5).sort() == [{'who':'SCARLET','what':'LEAVE','where':'OBSERVATORY','when':5.5}].sort())
        self.assertTrue(getMatching(self.memory,'?','ENTER','OBSERVATORY',2.5).sort() == [{'who':'MUSTARD','what':'ENTER','where':'OBSERVATORY','when':2.5}].sort())
        self.assertTrue(getMatching(self.memory,'SCARLET','?','OBSERVATORY',5.5).sort() == [{'who':'SCARLET','what':'LEAVE','where':'OBSERVATORY','when':5.5}].sort())

    def test_ask_person_calls_check_x_in_room(self):
        self.assertTrue(askPerson(self.memory,'MUSTARD','IN','?',1.0) == ['DINING ROOM'])
        self.assertTrue(askPerson(self.memory,'?','IN','OBSERVATORY',2.5).sort() == ['MUSTARD','SCARLET'].sort())
        self.assertTrue(askPerson(self.memory,'MUSTARD','IN','OBSERVATORY','?') ==  [{'START':2.5,'END':7.0}])
    
    def test_ask_person_calls_get_matching(self):
        self.assertTrue(askPerson(self.memory,'SCARLET','?','OBSERVATORY',5.5).sort() == [{'who':'SCARLET','what':'LEAVE','where':'OBSERVATORY','when':5.5}].sort())
        self.assertTrue(askPerson(self.memory,'?','LEAVE','OBSERVATORY',5.5).sort() == [{'who':'SCARLET','what':'LEAVE','where':'OBSERVATORY','when':5.5}].sort())
        self.assertTrue(askPerson(self.memory,'SCARLET','LEAVE','OBSERVATORY','?').sort() == [{'who':'SCARLET','what':'LEAVE','where':'OBSERVATORY','when':5.5}].sort())

if __name__ == '__main__':
    unittest.main()