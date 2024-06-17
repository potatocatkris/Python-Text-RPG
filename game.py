# Python Text RPG
# Krystian Sumara
# This is my first Python project after self learning Python, learned to make a text rpg by Baober on YT
# Hope you enjoy this game, I will be adding more to it as I learn more about Python

import cmd
import textwrap
import sys
import os
import time
import random

screen_width = 100

### PLAYER SETUP ###
class player:
    def __init__(self):
        self.name = ''
        self.role = ''
        self.hp = 0
        self.mp = 0
        self.status_effects = []
        self.location = 'start'
        self.game_over = False
myPlayer = player()

### TITLE SCREEN ###
def title_screen_selection():
    option = input(">").lower()
    if option == "play":
        start_game() #placeholder until writen
    elif option == "help":
        help_menu()
    elif option == "quit":
        sys.exit()
    while option not in ['play', 'help', 'quit']:
        print("Please enter a valid command")
        option = input("> ")
        if option == "play":
            start_game()  # placeholder until writen
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
    title_screen()


### MAP ###

# player starts at b3
# ----------------
# |a1|a2|a3|a4|a5|
# ----------------
# |b1|b2|b3|b4|b5|
# ----------------
# |c1|c2|c3|c4|c5|
# ----------------
# |d1|d2|d3|d4|d5|
# ----------------


ZONENAME: str = ''
DESCRIPTION = 'description'
EXAMINATION = 'examine'
SOLVED = False
UP = 'up', 'north'
DOWN = 'down', 'south'
LEFT = 'left', 'west'
RIGHT = 'right', 'east'

solved_places = {'a1': False, 'a2': False, 'a3': False, 'a4': False, 'a5': False,
                'b1': False, 'b2': False, 'b3': False, 'b4': False, 'b5': False,
                'c1': False, 'c2': False, 'c3': False, 'c4': False, 'c5': False,
                'd1': False, 'd2': False, 'd3': False, 'd4': False, 'd5': False,
                 }

zonemap = {
    'a1': {
        'ZONENAME': 'Guard Tower',
        'DESCRIPTION': 'The village\'s archers are stationed here',
        'EXAMINATION': 'Archers watch down at you from up above',
        'SOLVED': False,
        'UP': None,
        'DOWN': 'b1',
        'LEFT': None,
        'RIGHT': 'a2',
    },
    'a2': {
        'ZONENAME': 'Town Market',
        'DESCRIPTION': 'Trader has items, if you have gold',
        'EXAMINATION': 'This trader has everything you need and more',
        'SOLVED': False,
        'UP': None,
        'DOWN': 'b2',
        'LEFT': 'a1',
        'RIGHT': 'a3',
    },
    'a3': {
        'ZONENAME': 'Town Square',
        'DESCRIPTION': 'The place to meet with everyone',
        'EXAMINATION': 'This place is always packed with people',
        'SOLVED': False,
        'UP': None,
        'DOWN': 'b3',
        'LEFT': 'a2',
        'RIGHT': 'a4',
    },
    'a4': {
        'ZONENAME': 'Blacksmith',
        'DESCRIPTION': 'Axes, shields, armors and such',
        'EXAMINATION': 'I better not touch anything',
        'SOLVED': False,
        'UP': None,
        'DOWN': 'b4',
        'LEFT': 'a3',
        'RIGHT': 'a5',
    },
    'a5': {
        'ZONENAME': 'Town Barracks',
        'DESCRIPTION': 'Guards and archers home',
        'EXAMINATION': 'Safest part of town',
        'SOLVED': False,
        'UP': None,
        'DOWN': 'b5',
        'LEFT': 'a4',
        'RIGHT': None,
    },
    'b1': {
        'ZONENAME': '',
        'DESCRIPTION': '',
        'EXAMINATION': '',
        'SOLVED': False,
        'UP': 'a1',
        'DOWN': 'c1',
        'LEFT': None,
        'RIGHT': 'b2',
    },
    'b2': {
        'ZONENAME': '',
        'DESCRIPTION': '',
        'EXAMINATION': '',
        'SOLVED': False,
        'UP': 'a2',
        'DOWN': 'c2',
        'LEFT': 'b1',
        'RIGHT': 'b3',
    },
    'b3': {
        'ZONENAME': '',
        'DESCRIPTION': '',
        'EXAMINATION': '',
        'SOLVED': False,
        'UP': 'a3',
        'DOWN': 'c3',
        'LEFT': 'b2',
        'RIGHT': 'b4',
    },
    'b4': {
        'ZONENAME': '',
        'DESCRIPTION': '',
        'EXAMINATION': '',
        'SOLVED': False,
        'UP': 'a4',
        'DOWN': 'c4',
        'LEFT': 'b3',
        'RIGHT': 'b5',
    },
    'b5': {
        'ZONENAME': '',
        'DESCRIPTION': '',
        'EXAMINATION': '',
        'SOLVED': False,
        'UP': 'a5',
        'DOWN': 'c5',
        'LEFT': 'b4',
        'RIGHT': None,
    },
    'c1': {
        'ZONENAME': '',
        'DESCRIPTION': '',
        'EXAMINATION': '',
        'SOLVED': False,
        'UP': 'b1',
        'DOWN': 'd1',
        'LEFT': None,
        'RIGHT': 'c2',
    },
    'c2': {
        'ZONENAME': '',
        'DESCRIPTION': '',
        'EXAMINATION': '',
        'SOLVED': False,
        'UP': 'b2',
        'DOWN': 'd2',
        'LEFT': 'c1',
        'RIGHT': 'c3',
    },
    'c3': {
        'ZONENAME': '',
        'DESCRIPTION': '',
        'EXAMINATION': '',
        'SOLVED': False,
        'UP': 'b3',
        'DOWN': 'd3',
        'LEFT': 'c2',
        'RIGHT': 'c4',
    },
    'c4': {
        'ZONENAME': '',
        'DESCRIPTION': '',
        'EXAMINATION': '',
        'SOLVED': False,
        'UP': 'b4',
        'DOWN': 'd4',
        'LEFT': 'c3',
        'RIGHT': 'c5',
    },
    'c5': {
        'ZONENAME': '',
        'DESCRIPTION': '',
        'EXAMINATION': '',
        'SOLVED': False,
        'UP': 'b5',
        'DOWN': 'd5',
        'LEFT': 'c4',
        'RIGHT': None,
    },
    'd1': {
        'ZONENAME': '',
        'DESCRIPTION': '',
        'EXAMINATION': '',
        'SOLVED': False,
        'UP': 'c1',
        'DOWN': None,
        'LEFT': None,
        'RIGHT': 'd2',
    },
    'd2': {
        'ZONENAME': '',
        'DESCRIPTION': '',
        'EXAMINATION': '',
        'SOLVED': False,
        'UP': 'c2',
        'DOWN': None,
        'LEFT': 'd1',
        'RIGHT': 'd3',
    },
    'd3': {
        'ZONENAME': '',
        'DESCRIPTION': '',
        'EXAMINATION': '',
        'SOLVED': False,
        'UP': 'c3',
        'DOWN': None,
        'LEFT': 'd2',
        'RIGHT': 'd4',
    },
    'd4': {
        'ZONENAME': '',
        'DESCRIPTION': '',
        'EXAMINATION': '',
        'SOLVED': False,
        'UP': 'c4',
        'DOWN': None,
        'LEFT': 'd3',
        'RIGHT': 'd5',
    },
    'd5': {
        'ZONENAME': '',
        'DESCRIPTION': '',
        'EXAMINATION': '',
        'SOLVED': False,
        'UP': 'c5',
        'DOWN': None,
        'LEFT': 'd4',
        'RIGHT': None,
    },
}

### GAME INTERACTIVITY ###
def print_location():
    print('\n' + ('#' * (4 + len(myPlayer.location))))
    print('#' + myPlayer.location.upper() + ' #')
    print('#' + zonemap[myPlayer.position][DESCRIPTION] + ' #')
    print('\n' + ('#' * (4 + len(myPlayer.location))))


def prompt():
    print('\n' '===========================')
    print('What would you like to do?')
    action = input('>')
    acceptable_actions = ['move' 'go', 'travel', 'walk', 'examine', 'inspect', 'interact', 'look']
    while action.lower() not in acceptable_actions:
        print('I do not understand, try another command')
        action = input('>')
    if action.lower() == 'quit':
        sys.exit()
    elif action.lower() in ['move' 'go', 'travel', 'walk']:
        player_move(action.lower())
    elif action.lower() in ['examine', 'inspect', 'interact', 'look']:
        player_examine(action.lower())


def player_move(myAction):
    ask = 'Where would you like to go?\n'
    dest = input(ask)
    if dest in ['up', 'north']:
        destination = zonemap[myPlayer.location][UP]
        movement_handler(destination)
    elif dest in ['left', 'west']:
        destination = zonemap[myPlayer.location][LEFT]
        movement_handler(destination)
    elif dest in ['east', 'right']:
        destination = zonemap[myPlayer.location][RIGHT]
        movement_handler(destination)
    elif dest in ['south', 'down']:
        destination = zonemap[myPlayer.location][DOWN]
        movement_handler(destination)

def movement_handler(destination):
    print('\n' + 'You have moved to the ' + destination + '.')
    myPlayer.location = destination
    print_location()

def player_examine(action):
    if [myPlayer.location][SOLVED]:
        print('You have already explored and solved this area')
    else:
        print('You need to solve something here')

### GAME FUNCTIONALITY ###
def start_game():
    return

def main_game_loop():
    while myPlayer.game_over is False:
        prompt()
        # handle if puzzles have been solved, boss defeated, explored everything, etc



def setup_game():
    os.system('clear')

    #### NAME AND ROLE ###
    question1 = 'Hello friend, what is your name?\n'
    for character in question1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    player_name = input('> ')
    myPlayer.name = player_name
    ### ROLE HANDLING ###
    question2 = 'Tell me friend, what role do you want?\n'
    question2added = '(You can choose a warrior, mage or archer)\n'
    for character in question2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
        for character in question2added:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.01)
    player_job = input('> ')
    valid_jobs = ['warrior', 'mage', 'archer']
    if player_job.lower() in valid_jobs:
        myPlayer.job = player_job
        print('You are now a' + player_job + '!\n')
    while player_job.lower() not in valid_jobs:
            player_job = input('> ')
            if player_job.lower() in valid_jobs:
                myPlayer.job = player_job
                print('You are now a' + player_job + '!\n')

    myPlayer.job = player_job


title_screen()
