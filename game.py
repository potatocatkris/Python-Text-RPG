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
