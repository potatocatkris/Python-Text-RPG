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

# Player Setup #
class player:
    def __init__(self):
        self.name = ''
        self.hp = 0
        self.mp = 0
        self.status_effects = []
        self.location = 'noob village'
myPLayer = player()

# Title Screen #
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

# Game Functionality #
def start_game():


# Map #
#
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
