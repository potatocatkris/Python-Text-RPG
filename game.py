import cmd
import textwrap
import sys
import os
import time
import random

SCREEN_WIDTH = 100

### PLAYER SETUP ###
class Player:
    def __init__(self):
        self.name = ''
        self.role = ''
        self.hp = 0
        self.mp = 0
        self.status_effects = []
        self.location = 'b3'
        self.game_over = False

my_player = Player()

### TITLE SCREEN ###
def title_screen_selection():
    option = input(">").lower()
    if option == "play":
        start_game() # Placeholder until written
    elif option == "help":
        help_menu()
    elif option == "quit":
        sys.exit()
    while option not in ['play', 'help', 'quit']:
        print("Please enter a valid command")
        option = input("> ").lower()
        if option == "play":
            start_game()  # Placeholder until written
        elif option == "help":
            help_menu()
        elif option == "quit":
            sys.exit()

def title_screen():
    os.system('clear')
    print('###############################')
    print('### Welcome to the Text RPG ###')
    print('###############################')
    print('#           - Play -          #')
    print('#           - Help -          #')
    print('#           - Quit -          #')
    print('#  Copyright 2024 Krystian S  #')
    title_screen_selection()

def help_menu():
    print('####################################')
    print('- use up, down, left, right to move ')
    print('- type your commands to do them     ')
    print('- use "look" to inspect something   ')
    print('- good luck, have fun!              ')
    print('####################################')
    title_screen()


### MAP ###

ZONENAME = 'zonename'
DESCRIPTION = 'description'
EXAMINATION = 'examine'
SOLVED = 'solved'
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

solved_places = {f'{row}{col}': False for row in 'abcd' for col in '12345'}

zonemap = {
    'a1': {
        ZONENAME: 'Guard Tower',
        DESCRIPTION: 'The village\'s archers are stationed here',
        EXAMINATION: 'Archers watch down at you from up above',
        SOLVED: False,
        UP: None,
        DOWN: 'b1',
        LEFT: None,
        RIGHT: 'a2',
    },
    'a2': {
        ZONENAME: 'Town Market',
        DESCRIPTION: 'Trader has items, if you have gold',
        EXAMINATION: 'This trader has everything you need and more',
        SOLVED: False,
        UP: None,
        DOWN: 'b2',
        LEFT: 'a1',
        RIGHT: 'a3',
    },
    'a3': {
        ZONENAME: 'Town Square',
        DESCRIPTION: 'The place to meet with everyone',
        EXAMINATION: 'This place is always packed with people',
        SOLVED: False,
        UP: None,
        DOWN: 'b3',
        LEFT: 'a2',
        RIGHT: 'a4',
    },
    'a4': {
        ZONENAME: 'Blacksmith',
        DESCRIPTION: 'Axes, shields, armors and such',
        EXAMINATION: 'I better not touch anything',
        SOLVED: False,
        UP: None,
        DOWN: 'b4',
        LEFT: 'a3',
        RIGHT: 'a5',
    },
    'a5': {
        ZONENAME: 'Town Barracks',
        DESCRIPTION: 'Guards and archers home',
        EXAMINATION: 'Safest part of town',
        SOLVED: False,
        UP: None,
        DOWN: 'b5',
        LEFT: 'a4',
        RIGHT: None,
    },
    'b1': {
        ZONENAME: '',
        DESCRIPTION: '',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'a1',
        DOWN: 'c1',
        LEFT: None,
        RIGHT: 'b2',
    },
    'b2': {
        ZONENAME: '',
        DESCRIPTION: '',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'a2',
        DOWN: 'c2',
        LEFT: 'b1',
        RIGHT: 'b3',
    },
    'b3': {
        ZONENAME: '',
        DESCRIPTION: '',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'a3',
        DOWN: 'c3',
        LEFT: 'b2',
        RIGHT: 'b4',
    },
    'b4': {
        ZONENAME: '',
        DESCRIPTION: '',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'a4',
        DOWN: 'c4',
        LEFT: 'b3',
        RIGHT: 'b5',
    },
    'b5': {
        ZONENAME: '',
        DESCRIPTION: '',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'a5',
        DOWN: 'c5',
        LEFT: 'b4',
        RIGHT: None,
    },
    'c1': {
        ZONENAME: '',
        DESCRIPTION: '',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'b1',
        DOWN: 'd1',
        LEFT: None,
        RIGHT: 'c2',
    },
    'c2': {
        ZONENAME: '',
        DESCRIPTION: '',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'b2',
        DOWN: 'd2',
        LEFT: 'c1',
        RIGHT: 'c3',
    },
    'c3': {
        ZONENAME: '',
        DESCRIPTION: '',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'b3',
        DOWN: 'd3',
        LEFT: 'c2',
        RIGHT: 'c4',
    },
    'c4': {
        ZONENAME: '',
        DESCRIPTION: '',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'b4',
        DOWN: 'd4',
        LEFT: 'c3',
        RIGHT: 'c5',
    },
    'c5': {
        ZONENAME: '',
        DESCRIPTION: '',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'b5',
        DOWN: 'd5',
        LEFT: 'c4',
        RIGHT: None,
    },
    'd1': {
        ZONENAME: '',
        DESCRIPTION: '',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'c1',
        DOWN: None,
        LEFT: None,
        RIGHT: 'd2',
    },
    'd2': {
        ZONENAME: '',
        DESCRIPTION: '',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'c2',
        DOWN: None,
        LEFT: 'd1',
        RIGHT: 'd3',
    },
    'd3': {
        ZONENAME: '',
        DESCRIPTION: '',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'c3',
        DOWN: None,
        LEFT: 'd2',
        RIGHT: 'd4',
    },
    'd4': {
        ZONENAME: '',
        DESCRIPTION: '',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'c4',
        DOWN: None,
        LEFT: 'd3',
        RIGHT: 'd5',
    },
    'd5': {
        ZONENAME: '',
        DESCRIPTION: '',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'c5',
        DOWN: None,
        LEFT: 'd4',
        RIGHT: None,
    },
}

### GAME INTERACTIVITY ###
def print_location():
    location = my_player.location
    print('\n' + ('#' * (4 + len(location))))
    print('# ' + location.upper() + ' #')
    print('# ' + zonemap[location][DESCRIPTION] + ' #')
    print('\n' + ('#' * (4 + len(location))))

def prompt():
    print('\n===========================')
    print('What would you like to do?')
    action = input('>').lower()
    acceptable_actions = ['move', 'go', 'travel', 'walk', 'examine', 'inspect', 'interact', 'look']
    while action not in acceptable_actions:
        print('I do not understand, try another command')
        action = input('>').lower()
    if action == 'quit':
        sys.exit()
    elif action in ['move', 'go', 'travel', 'walk']:
        player_move()
    elif action in ['examine', 'inspect', 'interact', 'look']:
        player_examine()

def player_move():
    ask = 'Where would you like to go?\n'
    dest = input(ask).lower()
    if dest in ['up', 'north']:
        destination = zonemap[my_player.location][UP]
    elif dest in ['left', 'west']:
        destination = zonemap[my_player.location][LEFT]
    elif dest in ['right', 'east']:
        destination = zonemap[my_player.location][RIGHT]
    elif dest in ['down', 'south']:
        destination = zonemap[my_player.location][DOWN]
    else:
        print("Invalid direction!")
        return
    movement_handler(destination)

def movement_handler(destination):
    if destination:
        print('\nYou have moved to the ' + destination + '.')
        my_player.location = destination
        print_location()
    else:
        print("You can't go that way!")

def player_examine():
    location = my_player.location
    if zonemap[location][SOLVED]:
        print('You have already explored and solved this area')
    else:
        print(zonemap[location][EXAMINATION])

### GAME FUNCTIONALITY ###
def start_game():
    setup_game()
    main_game_loop()

def main_game_loop():
    while not my_player.game_over:
        prompt()

def setup_game():
    os.system('clear')

    ### NAME AND ROLE ###
    question1 = ' Hello friend, what is your name?\n'
    for character in question1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.1)
    player_name = input('> ')
    my_player.name = player_name

    question2 = 'Tell me friend, what role do you want?\n'
    question2added = '(You can choose a warrior, mage, or archer)\n'
    for character in question2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.1)
    for character in question2added:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.01)
    player_role = input('> ').lower()
    valid_roles = ['warrior', 'mage', 'archer']
    while player_role not in valid_roles:
        player_role = input('> ').lower()
    my_player.role = player_role
    print(f'You are now a {player_role}!\n')

    ### PLAYER STATS ###
    if my_player.role == 'warrior':
        my_player.hp = 150
        my_player.mp = 50
    elif my_player.role == 'mage':
        my_player.hp = 50
        my_player.mp = 150
    elif my_player.role == 'archer':
        my_player.hp = 100
        my_player.mp = 100

    ### INTRO ###
    intro_speeches = [
        f'Welcome, {player_name} the {player_role},\n',
        "This world is dangerous, you picked a good role\n",
        "I hope you survive these wild lands\n",
        "Make sure to grab health and mana potions\n",
        "Good luck to you\n"
    ]
    for speech in intro_speeches:
        for character in speech:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.05)

    os.system('clear')
    print("###########################")
    print("### Let's start the game ###")
    print("###########################")
    main_game_loop()

title_screen()
