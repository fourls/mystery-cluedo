from framework import *

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
        raw_input('When: ')
    ):
        print(match['who'] + ' ' + match['what'] + ' the ' + match['where'] + ' at ' + str(match['when']))