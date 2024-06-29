import os
import pickle
import sys
import time

SCREEN_WIDTH = 100


# PLAYER SETUP #
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


# TITLE SCREEN #
def title_screen_selection():
    option = input(">").lower()
    if option == "play":
        start_game()
    elif option == "help":
        help_menu()
    elif option == "load":
        load_game()
        main_game_loop()
    elif option == "exit":
        sys.exit()
    while option not in ['play', 'help', 'load', 'exit']:
        print("Please enter a valid command")
        option = input("> ").lower()
        if option == "play":
            start_game()
        elif option == "help":
            help_menu()
        elif option == "load":
            load_game()
            main_game_loop()
        elif option == "exit":
            sys.exit()


def title_screen():
    os.system('clear')
    print('####################################################################################################')
    print('#                                                                                                  #')
    print('#                 #     # ### #       ######     #          #    #     # ######   #####            #')
    print('#                 #  #  #  #  #       #     #    #         # #   ##    # #     # #     #           #')
    print('#                 #  #  #  #  #       #     #    #        #   #  # #   # #     # #                 #')
    print('#                 #  #  #  #  #       #     #    #       #     # #  #  # #     #  #####            #')
    print('#                 #  #  #  #  #       #     #    #       ####### #   # # #     #       #           #')
    print('#                 #  #  #  #  #       #     #    #       #     # #    ## #     # #     #           #')
    print('#                  ## ##  ### ####### ######     ####### #     # #     # ######   #####            #')
    print('#                                                                                                  #')
    print('#                 ####### ####### #     # #######    ######  ######   #####                        #')
    print('#                    #    #        #   #     #       #     # #     # #     #                       #')
    print('#                    #    #         # #      #       #     # #     # #                             #')
    print('#                    #    #####      #       #       ######  ######  #  ####                       #')
    print('#                    #    #         # #      #       #   #   #       #     #                       #')
    print('#                    #    #        #   #     #       #    #  #       #     #                       #')
    print('#                    #    ####### #     #    #       #     # #        #####                        #')
    print('#                                                                                                  #')
    print('#                                           - Play -                                               #')
    print('#                                           - Load -                                               #')
    print('#                                           - Help -                                               #')
    print('#                                           - Exit -                                               #')
    print('#                                  Copyright 2024 Krystian S                                       #')
    print('####################################################################################################')

    title_screen_selection()


def help_menu():
    print('####################################################################################################')
    print('- use commands such as move, go,    ')
    print('- type your commands to do them     ')
    print('- use "look" to inspect something   ')
    print('- good luck, have fun!              ')
    print('####################################################################################################')
    title_screen()


# MAP #
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
        ZONENAME: 'Ranger Tower',
        DESCRIPTION: 'The village\'s rangers are stationed here',
        EXAMINATION: 'There are new recruits being trained by the Lead Ranger. Inside the tower there are many books '
                     'on survival and cooking.',
        SOLVED: False,
        UP: None,
        DOWN: 'b1',
        LEFT: None,
        RIGHT: 'a2',
    },
    'a2': {
        ZONENAME: 'Town Market',
        DESCRIPTION: 'People from all over come here to trade and barter their goods',
        EXAMINATION: 'Many kiosks are set up with items from various vendors for sale. Everyone seems to be yelling '
                     'and spitting on each other',
        SOLVED: False,
        UP: None,
        DOWN: 'b2',
        LEFT: 'a1',
        RIGHT: 'a3',
    },
    'a3': {
        ZONENAME: 'Town Square',
        DESCRIPTION: 'The place to meet with everyone',
        EXAMINATION: 'Everywhere you look there are people talking amongst themselves. I should try talking to some '
                     'of the locals here and see what is going on in town. ',
        SOLVED: False,
        UP: None,
        DOWN: 'b3',
        LEFT: 'a2',
        RIGHT: 'a4',
    },
    'a4': {
        ZONENAME: 'Blacksmith',
        DESCRIPTION: 'Axes, shields, armors and such',
        EXAMINATION: 'For being a blacksmith shop, the place is surprisingly clean. There are many metals and '
                     'precious gems here. ',
        SOLVED: False,
        UP: None,
        DOWN: 'b4',
        LEFT: 'a3',
        RIGHT: 'a5',
    },
    'a5': {
        ZONENAME: 'Town Barracks',
        DESCRIPTION: 'Village guards work and sleep here',
        EXAMINATION: 'One of the captains is yelling at the new recruits while another is laughing at the recruits '
                     'for missing their shot with a bow ',
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


# GAME INTERACTIVITY #
def print_location():
    location = my_player.location
    print('\n' + ('#' * (4 + len(location))))
    print('# ' + zonemap[location][ZONENAME] + ' #')
    print('# ' + zonemap[location][DESCRIPTION] + ' #')
    print('\n' + ('#' * (4 + len(location))))


def prompt():
    print('\n===========================')
    print('What would you like to do?')
    action = input('>').lower()
    acceptable_actions = ['move', 'go', 'travel', 'walk', 'examine', 'inspect', 'interact', 'look', 'map', 'npc',
                          'save']
    while action not in acceptable_actions:
        print('I do not understand, try another command')
        action = input('>').lower()
    if action == 'quit':
        sys.exit()
    elif action in ['move', 'go', 'travel', 'walk']:
        player_move()
    elif action in ['examine', 'inspect', 'interact', 'look']:
        player_examine()
    elif action == 'map':
        display_map()
    elif action == 'npc':
        interact_with_npc()
    elif action == 'save':
        save_game()


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
        print('\nYou have moved to the ' + zonemap[destination][ZONENAME] + '.')
        my_player.location = destination
        print_location()
        display_map()  # Show the map after moving
    else:
        print("You can't go that way!")


def display_map():
    rows, cols = 4, 5
    map_grid = [["." for _ in range(cols)] for _ in range(rows)]
    location = my_player.location
    row = ord(location[0]) - ord('a')
    col = int(location[1]) - 1
    map_grid[row][col] = "P"
    print("\nMap:")
    for row in map_grid:
        print(" ".join(row))


def player_examine():
    location = my_player.location
    if zonemap[location][SOLVED]:
        print('You have already explored and solved this area')
    else:
        print(zonemap[location][EXAMINATION])


def interact_with_npc():
    location = my_player.location
    if location in npcs:
        for npc in npcs[location]:
            npc.talk()
            action = input(f"Would you like to (1) Accept quest (2) Trade (3) Hear rumors (4) Leave? ").lower()
            if action == '1':
                npc.offer_quests()
            elif action == '2':
                trade_item = input(f"What would you like to trade? ")
                receive_item = input(f"What do you want in return? ")
                npc.barter(trade_item, receive_item)
            elif action == '3':
                npc.share_rumors()
            elif action == '4':
                print("You decide to leave.")
            else:
                print("Invalid action.")
    else:
        print("There are no NPCs here.")


# GAME FUNCTIONALITY #
def start_game():
    setup_game()
    main_game_loop()


def main_game_loop():
    while not my_player.game_over:
        prompt()


def setup_game():
    os.system('clear')

    # NAME AND ROLE #
    question1 = ' Hello friend, what is your name?\n'
    for character in question1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    player_name = input('> ')
    my_player.name = player_name

    question2 = 'Tell me friend, what role do you want?\n'
    question2added = '(You can choose a warrior, mage, or archer)\n'
    for character in question2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in question2added:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    player_role = input('> ').lower()
    valid_roles = ['warrior', 'mage', 'archer']
    while player_role not in valid_roles:
        player_role = input('> ').lower()
    my_player.role = player_role
    print(f'You are now a {player_role}!\n')

    # PLAYER STATS #
    if my_player.role == 'warrior':
        my_player.hp = 150
        my_player.mp = 50
    elif my_player.role == 'mage':
        my_player.hp = 50
        my_player.mp = 150
    elif my_player.role == 'archer':
        my_player.hp = 100
        my_player.mp = 100

    # INTRO #
    intro_speeches = [
        f'Welcome, {player_name} the {player_role},\n',
        "This world is dangerous, you've picked a good role\n",
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
    print("############################")
    print("### Let's start the game ###")
    print("############################")
    main_game_loop()


# NPC's #
class NPC:
    def __init__(self, name, role, location, quests=None, inventory=None, rumors=None, dialogue=None):
        self.name = name
        self.role = role
        self.location = location
        self.quests = quests if quests else []
        self.inventory = inventory if inventory else []
        self.rumors = rumors if rumors else []
        self.dialogue = dialogue if dialogue else {}

    def talk(self):
        if 'greeting' in self.dialogue:
            print(f"{self.name} says: '{self.dialogue['greeting']}'")
        else:
            print(f"{self.name} says: 'Hello there, traveler!'")

    def offer_quests(self):
        if self.quests:
            for quest in self.quests:
                print(f"{self.name} offers you a quest: {quest}")
        else:
            print(f"{self.name} has no quests for you.")

    def buy(self, item):
        self.inventory.append(item)
        print(f"{self.name} buys {item}")

    def sell(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"{self.name} sells {item}")
        else:
            print(f"{self.name} doesn't have {item}")

    def barter(self, item_to_give, item_to_receive):
        if item_to_give in self.inventory:
            self.inventory.remove(item_to_give)
            self.inventory.append(item_to_receive)
            print(f"{self.name} barters {item_to_give} for {item_to_receive}")
        else:
            print(f"{self.name} doesn't have {item_to_give}")

    def share_rumors(self):
        if self.rumors:
            for rumor in self.rumors:
                print(f"{self.name} whispers: '{rumor}'")
        else:
            print(f"{self.name} has no rumors to share.")


# Example NPCs
npc1 = NPC(
    name="Harry",
    role="Blacksmith",
    location="a4",
    quests=["Find the lost sword"],
    inventory=["Iron Sword"],
    rumors=["The king is looking for brave adventurers."],
    dialogue={'greeting': "Welcome to my blacksmith shop, adventurer! How can I assist you today?"}
)
npc2 = NPC(
    name="Elara",
    role="Merchant",
    location="a2",
    quests=["Deliver this package"],
    inventory=["Health Potion", "Mana Potion"],
    rumors=["A dragon was seen near the mountains."],
    dialogue={'greeting': "Hello! Care to trade some goods?"}
)
npc3 = NPC(
    name="Arwen",
    role="Head Ranger",
    location="a1",
    quests=["Collect materials for a basic bow and arrow"],
    inventory=["Basic Bow", "Arrows"],
    rumors=["Something is disturbing the forrest at night time."],
    dialogue={
        'greeting': "Welcome to the Ranger Tower, brave adventurer. I'm here to help you survive the wild.",
        'quest_offer': "I have a quest for you. Can you collect the materials needed for a basic bow and some arrows?",
        'trade': "I can trade you a Basic Bow and some Arrows for the right materials."
    }
)

npcs = {
    'a1': [npc3],
    'a2': [npc2],
    'a4': [npc1]
}


# Save and Load Functions
def save_game(filename='savefile.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(my_player, f)
        print("Game saved successfully.")


def load_game(filename='savefile.pkl'):
    global my_player
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            my_player = pickle.load(f)
            print("Game loaded successfully.")
            print_location()  # Display the current location after loading
    else:
        print("No save file found.")


title_screen()
