import os
import pickle
import sys
import time
import random

SCREEN_WIDTH = 100


# Function to clear the console based on the operating system
def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix-based systems (Linux and macOS)
        os.system('clear')


# PLAYER SETUP #
class Player:
    def __init__(self):
        self.name = ''
        self.role = ''
        self.hp = 0
        self.mp = 0
        self.strength = 0
        self.agility = 0
        self.intelligence = 0
        self.spirit = 0
        self.luck = 0
        self.armor = 0
        self.status_effects = []
        self.location = 'b3'
        self.game_over = False
        self.turn_count = 0  # For spirit-based regeneration

    def assign_stats(self):
        if self.role == 'warrior':
            self.strength = 5
            self.agility = 3
            self.intelligence = 1
            self.spirit = 3
            self.luck = 2
        elif self.role == 'mage':
            self.strength = 1
            self.agility = 2
            self.intelligence = 5
            self.spirit = 3
            self.luck = 3
        elif self.role == 'archer':
            self.strength = 3
            self.agility = 5
            self.intelligence = 2
            self.spirit = 3
            self.luck = 1

        self.hp = 100 + self.strength * 1
        self.mp = 50 + self.intelligence * 1
        self.armor = self.agility * 1

    def melee_damage(self):
        return self.strength * 2

    def ranged_damage(self):
        return self.agility * 2

    def magic_damage(self):
        return self.intelligence * 2

    def regenerate(self):
        if self.turn_count % 2 == 0:
            self.hp += self.spirit
            self.mp += self.spirit

    def update_turn(self):
        self.turn_count += 1
        self.regenerate()


class Monster:
    def __init__(self, name, hp, mp, strength, agility, intelligence, spirit, luck):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.spirit = spirit
        self.luck = luck
        self.armor = agility * 1
        self.status_effects = []
        self.turn_count = 0

    def melee_damage(self):
        return self.strength * 2

    def ranged_damage(self):
        return self.agility * 2

    def magic_damage(self):
        return self.intelligence * 2

    def regenerate(self):
        if self.turn_count % 2 == 0:
            self.hp += self.spirit
            self.mp += self.spirit

    def update_turn(self):
        self.turn_count += 1
        self.regenerate()

    def attack(self, player):
        damage = self.melee_damage() - player.armor
        player.hp -= max(0, damage)
        print(f"{self.name} attacks {player.name} for {damage} damage!")

    def is_alive(self):
        return self.hp > 0


class Item:
    def __init__(self, name, quality, stat_effects):
        self.name = name
        self.quality = quality
        self.stat_effects = stat_effects

    def __str__(self):
        effects = ', '.join(f"{stat}: {value}" for stat, value in self.stat_effects.items())
        return f"{self.quality.title()} {self.name} ({effects})"


# Game Items

# Common Items
training_sword = Item("Training Sword", "common", {"strength": 1})
old_bow = Item("Old Bow", "common", {"agility": 1})
used_staff = Item("Used Staff", "common", {"intelligence": 1})

# Uncommon Items
iron_mace = Item("Iron Sword", "uncommon", {"strength": 2, "agility": 1})
oak_staff = Item("Oak Staff", "common", {"intelligence": 2, "spirit": 2})
willow_bow = Item("Willow Bow", "common", {"agility": 2, "luck": 2})

# Rare Items
mithril_axe = Item("Mithril Axe", "rare", {"strength": 5, "agility": 4, "hp": 20})
ebony_staff = Item("Ebony Staff", "rare", {"intelligence": 5, "spirit": 4, "mp": 20})
maple_bow = Item("Maple Bow", "rare", {"agility": 5, "luck": 4, "spirit": 2})

#Epic Items
troll_slayer = Item("Troll Slayer", "epic", {"strength": 12, "agility": 10, "hp": 50, "spirit": 6})
rising_tides - Item("Rising Tides", "epic", {"intelligence": 12, "spirit": 10, "mp": 50, "luck": 6})
nightdraw - Item("Nightdraw", "epic", {"agility": 12, "luck": 10, "spirit": 6, "hp": 50})

# Loot tables for each rarity
common_loot = [training_sword, Item("Training Sword", "common", {"strength": 1}),
               old_bow, Item("Old Bow", "common", {"agility": 1}),
               used_staff, Item("Old Staff", "common", {"intelligence": 1})
               ]

uncommon_loot = [iron_mace, Item("Iron Sword", "uncommon", {"strength": 2, "agility": 1}),
                 oak_staff, Item("Oak Staff", "common", {"intelligence": 2, "spirit": 2}),
                 willow_bow, Item("Willow Bow", "common", {"agility": 2, "luck": 2})
                 ]

rare_loot = [mithril_axe, Item("Mithril Axe", "rare", {"strength": 5, "agility": 4, "hp": 20}),
             ebony_staff, Item("Ebony Staff", "rare", {"intelligence": 5, "spirit": 4, "mp": 20}),
             maple_bow, Item("Maple Bow", "rare", {"agility": 5, "luck": 4, "spirit": 2})
             ]

epic_loot = [troll_slayer, Item("Troll Slayer", "epic", {"strength": 12, "agility": 10, "hp": 50, "spirit": 6}),
             rising_tide, Item("Rising Tides", "epic", {"intelligence": 12, "spirit": 10, "mp": 50, "luck": 6}),
             nightdraw, Item("Nightdraw", "epic", {"agility": 12, "luck": 10, "spirit": 6, "hp": 50})
             ]


def drop_item(player):
    luck_modifier = player.luck * 1  # Each point of luck increases drop chance by 1%
    roll = random.randint(1, 100)

    if roll <= 2 + luck_modifier:
        return random.choice(epic_loot)
    elif roll <= 10 + luck_modifier:
        return random.choice(rare_loot)
    elif roll <= 30 + luck_modifier:
        return random.choice(uncommon_loot)
    else:
        return random.choice(common_loot)


def battle(monster):
    print(f"A wild {monster.name} appears!")
    while monster.is_alive() and my_player.hp > 0:
        print(f"{my_player.name}'s HP: {my_player.hp}, MP: {my_player.mp}")
        print(f"{monster.name}'s HP: {monster.hp}, MP: {monster.mp}")
        action = input("Choose an action: (1) Attack (2) Use Skill (3) Use Item (4) Flee: ").lower()
        if action == '1':
            damage = my_player.melee_damage()  # Or ranged_damage() or magic_damage() based on action
            monster.hp -= damage
            print(f"{my_player.name} attacks {monster.name} for {damage} damage!")
        elif action == '2':
            pass  # Implement skill logic
        elif action == '3':
            pass  # Implement item usage
        elif action == '4':
            print("You fled the battle.")
            return
        else:
            print("Invalid action!")

        if monster.is_alive():
            monster.attack(my_player)
            my_player.update_turn()

    if my_player.hp <= 0:
        print("You have been defeated.")
        my_player.game_over = True
    elif not monster.is_alive():
        print(f"You defeated the {monster.name}!")
        dropped_item = drop_item(my_player)
        print(f"You found a {dropped_item}!")


def hunt():
    location = my_player.location
    if 'monsters' in zonemap[location]:
        possible_monsters = zonemap[location]['monsters']
        monster = random.choice(possible_monsters)
        battle(monster)
    else:
        print("There are no monsters to hunt here.")


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
    clear_screen()
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
    print('-                  use commands such go, examine, description, npc                                  ')
    print('-                              type your commands to do them                                        ')
    print('-                                                                                                   ')
    print('-                                      good luck, have fun!                                         ')
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
                     'on survival and cooking',
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
                     'of the locals here and see what is going on around town ',
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
                     'precious gems here ',
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
                     'for missing their shot with a bow',
        SOLVED: False,
        UP: None,
        DOWN: 'b5',
        LEFT: 'a4',
        RIGHT: None,
    },
    'b1': {
        ZONENAME: 'Wizard Tower',
        DESCRIPTION: 'The dark tower has dark windows with no visible light inside',
        EXAMINATION: 'Young wizards are training their magic by shooting fireballs at training dummies. Inside the tower'
                     'is a massive library of books',
        SOLVED: False,
        UP: 'a1',
        DOWN: 'c1',
        LEFT: None,
        RIGHT: 'b2',
    },
    'b2': {
        ZONENAME: 'Alchemy Shop',
        DESCRIPTION: 'You smell something very pleasant as you walk in, the shop owner greets you with a smile',
        EXAMINATION: 'The shop is covered in herbs and potions. In the other room is recipes and books on alchemy',
        SOLVED: False,
        UP: 'a2',
        DOWN: 'c2',
        LEFT: 'b1',
        RIGHT: 'b3',
    },
    'b3': {
        ZONENAME: 'Home',
        DESCRIPTION: 'It ain\'t much, but it\'s honest living',
        EXAMINATION: 'This is the home I grew up in, I still have my hunting trophies on the walls',
        SOLVED: False,
        UP: 'a3',
        DOWN: 'c3',
        LEFT: 'b2',
        RIGHT: 'b4',
    },
    'b4': {
        ZONENAME: 'Butcher Shop',
        DESCRIPTION: 'This place definitely doesn\'t smell as good as the alchemy shop',
        EXAMINATION: 'You hear the hacking and pounding noises as an apprentice butcher chops a boar. There is a list '
                     'animals that need to be hunted',
        SOLVED: False,
        UP: 'a4',
        DOWN: 'c4',
        LEFT: 'b3',
        RIGHT: 'b5',
    },
    'b5': {
        ZONENAME: 'Tavern',
        DESCRIPTION: 'Townspeople favorite spot once they got off work',
        EXAMINATION: 'Tavern owner greets you warmly with a pint of ale, the tavern\'s wife offers you some food. There is '
                     'a bard playing in the background',
        SOLVED: False,
        UP: 'a5',
        DOWN: 'c5',
        LEFT: 'b4',
        RIGHT: None,
    },
    'c1': {
        ZONENAME: 'Grasslands Farm',
        DESCRIPTION: 'A humble farm that supplies the town',
        EXAMINATION: 'You see a family of farmers tending to their land. There are plenty of livestock roaming around',
        SOLVED: False,
        UP: 'b1',
        DOWN: 'd1',
        LEFT: None,
        RIGHT: 'c2',
        'monsters': [Monster("Boar", 20, 0, 5, 3, 1, 3, 1)]
    },
    'c2': {
        ZONENAME: 'Grasslands Outpost',
        DESCRIPTION: 'A small outpost outside of town to protect the outside perimeter',
        EXAMINATION: 'There are mounted archers roaming around. The infantry is protecting the farmers',
        SOLVED: False,
        UP: 'b2',
        DOWN: 'd2',
        LEFT: 'c1',
        RIGHT: 'c3',
        'monsters': [Monster("Boar", 20, 0, 5, 3, 1, 3, 1)]
    },
    'c3': {
        ZONENAME: 'Grasslands',
        DESCRIPTION: 'Open fields with some hills',
        EXAMINATION: 'A gentle breeze blows towards you, there are some houses built on the hills. You can see people'
                     'walking around on the roads',
        SOLVED: False,
        UP: 'b3',
        DOWN: 'd3',
        LEFT: 'c2',
        RIGHT: 'c4',
        'monsters': [Monster("Boar", 20, 0, 5, 3, 1, 3, 1)]
    },
    'c4': {
        ZONENAME: 'Grasslands',
        DESCRIPTION: 'Open fields with some hills',
        EXAMINATION: 'A gentle breeze blows towards you, there are some houses built on the hills. You can see people'
                     'walking around on the roads',
        SOLVED: False,
        UP: 'b4',
        DOWN: 'd4',
        LEFT: 'c3',
        RIGHT: 'c5',
        'monsters': [Monster("Boar", 20, 0, 5, 3, 1, 3, 1)]
    },
    'c5': {
        ZONENAME: 'Forest',
        DESCRIPTION: 'A dark forest',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'b5',
        DOWN: 'd5',
        LEFT: 'c4',
        RIGHT: None,
        'monsters': [Monster("Wolf", 50, 0, 7, 6, 3, 4, 2)]
    },
    'd1': {
        ZONENAME: 'Dense Forest',
        DESCRIPTION: '',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'c1',
        DOWN: None,
        LEFT: None,
        RIGHT: 'd2',
        'monsters': [Monster("Wolf", 50, 0, 7, 6, 3, 4, 2)]
    },
    'd2': {
        ZONENAME: 'Dense Forest',
        DESCRIPTION: '',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'c2',
        DOWN: None,
        LEFT: 'd1',
        RIGHT: 'd3',
        'monsters': [Monster("Wolf", 50, 0, 7, 6, 3, 4, 2), Monster("Bandit", 100, 0, 6, 5, 3, 5, 3)]
    },
    'd3': {
        ZONENAME: 'Lumber Mill',
        DESCRIPTION: 'An old lumber mill that is still being used by the village',
        EXAMINATION: 'It seems no one is around, the whole place looks like a mess, it looks like a fight was here not '
                     'that long ago',
        SOLVED: False,
        UP: 'c3',
        DOWN: None,
        LEFT: 'd2',
        RIGHT: 'd4',
        'monsters': [Monster("Bandit", 100, 0, 6, 5, 3, 5, 3)]
    },
    'd4': {
        ZONENAME: 'Old Ruins',
        DESCRIPTION: 'Old stone structures with vegetation growing all over it',
        EXAMINATION: "There are letters carved into the rock you don't understand, you feel a strong magical force here",
        SOLVED: False,
        UP: 'c4',
        DOWN: None,
        LEFT: 'd3',
        RIGHT: 'd5',
        'monsters': [Monster("Bandit", 100, 0, 6, 5, 3, 5, 3)]
    },
    'd5': {
        ZONENAME: 'Hidden Cave',
        DESCRIPTION: '',
        EXAMINATION: '',
        SOLVED: False,
        UP: 'c5',
        DOWN: None,
        LEFT: 'd4',
        RIGHT: None,
        'monsters': [Monster("Forest Troll", 250, 100, 10, 10, 6, 5, 3)]
    },
}


# GAME INTERACTIVITY #
def print_location():
    location = my_player.location
    print('\n' + ('#' * (80 + len(location))))
    print('# ' + zonemap[location][DESCRIPTION] + ' #')


def prompt():
    print('\n=========================')
    print('What would you like to do?')
    action = input('>').lower()
    acceptable_actions = ['move', 'go', 'travel', 'walk', 'examine', 'inspect', 'interact', 'look', 'map', 'npc',
                          'save', 'hunt']
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
    elif action == 'hunt':
        hunt()


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
    print(f"\nMap:")
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
    clear_screen()

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
    my_player.assign_stats()
    print(f'You are now a {player_role}!\n')

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

    clear_screen()
    print("############################")
    print("### Let's start the game ###")
    print("############################")
    main_game_loop()


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
