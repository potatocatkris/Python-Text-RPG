import os
import random


# Define the Color class for ANSI color codes
class Color:
    ANSI_RESET = "\033[0m"
    ANSI_BLACK = "\033[1;90m"
    ANSI_RED = "\033[1;91m"
    ANSI_GREEN = "\033[38;5;28m"
    ANSI_LIGHT_GREEN = "\033[32;2m"
    ANSI_LIME_GREEN = "\033[38;5;10m"
    ANSI_YELLOW = "\033[1;93m"
    ANSI_BLUE = "\033[1;94m"
    ANSI_PURPLE = "\033[1;95m"
    ANSI_CYAN = "\033[1;96m"
    ANSI_WHITE = "\033[1;97m"
    ANSI_DARK_BLACK = "\033[0;30m"
    ANSI_DARK_RED = "\033[0;31m"
    ANSI_DARK_GREEN = "\033[38;5;22m"
    ANSI_DARK_YELLOW = "\033[38;5;100m"
    ANSI_DARK_BLUE = "\033[0;34m"
    ANSI_DARK_PURPLE = "\033[0;35m"
    ANSI_DARK_CYAN = "\033[36;2m"
    ANSI_DARK_WHITE = "\033[0;37m"
    ANSI_LIGHT_GRAY = "\033[0;37m"


# Define the Tile class
class Tile:
    def __init__(self, symbol: str, name: str, color: str = Color.ANSI_RESET, monster: str = None,
                 item: str = None) -> None:
        self.symbol = symbol
        self.name = name
        self.legend = f"{symbol} {name.upper()}"
        self.colored_symbol = f"{color}{symbol}{Color.ANSI_RESET}"
        self.colored_name = f"{color}{name.upper()}{Color.ANSI_RESET}"
        self.colored_legend = f"{self.colored_symbol} {self.colored_name}"


# Define various tiles
player_tile = Tile('P', 'player', Color.ANSI_RED)

# Biomes
plains = Tile('.', 'plains', Color.ANSI_DARK_YELLOW)
grasslands = Tile(',', 'grasslands', Color.ANSI_LIGHT_GREEN)
forest = Tile('Y', 'forest', Color.ANSI_GREEN)
dark_forest = Tile('8', 'dark_forest', Color.ANSI_DARK_GREEN)
mountain = Tile('A', 'mountain', Color.ANSI_WHITE)
river = Tile('=', 'river', Color.ANSI_CYAN)
lake = Tile('~', 'lake', Color.ANSI_CYAN)
deep_lake = Tile('#', 'deep_lake', Color.ANSI_BLUE)
jungle = Tile('&', 'jungle', Color.ANSI_LIME_GREEN)
enchanted_forest = Tile('$', 'enchanted_forest', Color.ANSI_DARK_CYAN)
frigid_mountain = Tile('M', 'frigid_mountain', Color.ANSI_WHITE)

# Buildings
town = Tile('T', 'town', Color.ANSI_YELLOW)
farmhouse = Tile('F', 'farmhouse', Color.ANSI_YELLOW)
castle = Tile('C', 'castle', Color.ANSI_DARK_WHITE)
old_ruins = Tile('O', 'old_ruins', Color.ANSI_LIGHT_GRAY)
jungle_temple = Tile('J', 'jungle_temple', Color.ANSI_YELLOW)
voodoo_village = Tile('V', 'voodoo_village', Color.ANSI_YELLOW)
goblin_fortress = Tile('G', 'goblin_village', Color.ANSI_YELLOW)

# NPC
store_clerk = Tile('S', 'store_clerk', Color.ANSI_DARK_RED)
blacksmith = Tile('B', 'blacksmith', Color.ANSI_DARK_RED)
ranger = Tile('R', 'ranger', Color.ANSI_DARK_RED)
herbalist = Tile('H', 'herbalist', Color.ANSI_DARK_RED)
wisdom_seeker = Tile('W', 'wisdom_seeker', Color.ANSI_DARK_RED)

unexplored_tile = Tile('?', 'unexplored', Color.ANSI_LIGHT_GRAY)

# Define the world map
world_map = [
    'TTTT.....,,,,~~~~~~~~,,B.YY88AAA8Y,,,,===&&&JJ&&&&&&&&&VVV&&',
    'TTTT......,,,~~~~~~~~,,,,YY88AAA8Y,,,,===&&&JJ&&&&&&&&&VVV&&',
    'TTTT.......,,,~~~~~~~,,,,YYY8AA8Y,..,,.===&&&&&&&&&&&&&VVV&&',
    '.......R....,,==,,,...,,YYYYY88YY...,,,.===&&&&&JJ&&&&&&&&&&',
    '..FF..........,,==,,..,,,YYYYYYY.......,,,,===&&JJ&&&&&####&',
    '..FF..........,,==,,.......,,,,,,,........,,.===&&&&&&&###&&',
    '...........,,,,,==,,...S,TTT,,,,,........,,,,===&&&JJ&&==&,,',
    '...,,,,,W,...,,,,==,,...,TTT,,,,,,,,,......,,,,,===&JJ&&==,,',
    ',,YYYYYYYYY,,,,,,,==,,,,,,,,,,,,,,,,,,,,.....,,,,===,,,,,==,',
    'YYYYOOOYYYYYY,H,,,.==.YYYYYYYYYYYY,,,,,,,,,,,,,,,==,,,,,,,==',
    'YYYYOOOYYYYYY,,,,,,==YYYY8888888YYYYYY,,,,,,,,,,,==,,,,,,88=',
    'YYYYYYYYYYY,,,,,,,==YYYY888AAA888YYYYYYYY,,,,,,,,,==,,,88$$=',
    'YY888YYYYYYY,,,,,==YYY8888AAAAAA888YYYYYYY,,,,,,,==,,888$$$$',
    'Y888YY888YYYY,,==YYYY888AAAAAAAA88888YYYYYY,,,,,==,,,88$$MM$',
    '888YYY88888YYY==YYYY888AAAAAAAAAAA8888YYYYY,,,,==,,888$$MMMM',
    '888YY88888YYYY==YYYYY8888AAAAAAAAA888YYYYYYYY,==,,88$$$MMMMM',
    '88YY88YYY~~~~~~~~~~YYY8888AAAAAA888YYYYYYYYY,==,,88$$MMMMMMM',
    '8888888YY~~~~~~~~~~~YYY88AACCCCAAA8888YYYYYY==,,88$$$MMMMCCC',
    '888GGG8YYY~~~~~~~~~~YYY88AACCCCAAAA8888YYYY==,,88$$$MMMMMCCC',
    '888GGG88YY~~~~~~~~~~YYY88AACCCCAAAA8888YYYY==,,88$$$MMMMMCCC',
]


# Utility function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Define the legend for the map tiles in three categories: biomes, buildings, and NPCs/others
def get_legend():
    biomes = [
        f"{plains.colored_symbol} - {plains.name}          ",
        f"{grasslands.colored_symbol} - {grasslands.name}      ",
        f"{forest.colored_symbol} - {forest.name}          ",
        f"{dark_forest.colored_symbol} - {dark_forest.name}     ",
        f"{mountain.colored_symbol} - {mountain.name}        ",
        f"{river.colored_symbol} - {river.name}           ",
        f"{lake.colored_symbol} - {lake.name}            ",
        f"{deep_lake.colored_symbol} - {deep_lake.name}",
        f"{jungle.colored_symbol} - {jungle.name}",
        f"{enchanted_forest.colored_symbol} - {enchanted_forest.name}",
        f"{frigid_mountain.colored_symbol} - {frigid_mountain.name}",
    ]

    buildings = [
        f"{town.colored_symbol} - {town.name}           ",
        f"{farmhouse.colored_symbol} - {farmhouse.name}      ",
        f"{castle.colored_symbol} - {castle.name}         ",
        f"{old_ruins.colored_symbol} - {old_ruins.name}      ",
        f"{jungle_temple.colored_symbol} - {jungle_temple.name}  ",
        f"{voodoo_village.colored_symbol} - {voodoo_village.name} ",
        f"{goblin_fortress.colored_symbol} - {goblin_fortress.name} ",
    ]

    npcs_others = [
        f"{player_tile.colored_symbol} - {player_tile.name}",
        f"{store_clerk.colored_symbol} - {store_clerk.name}",
        f"{blacksmith.colored_symbol} - {blacksmith.name}",
        f"{ranger.colored_symbol} - {ranger.name}",
        f"{herbalist.colored_symbol} - {herbalist.name}",
        f"{wisdom_seeker.colored_symbol} - {wisdom_seeker.name}",
        f"{unexplored_tile.colored_symbol} - {unexplored_tile.name}   ",
    ]

    return biomes, buildings, npcs_others


class Map:
    def __init__(self, width: int, height: int, discovery_size: int = 4) -> None:
        self.width = width
        self.height = height
        self.discovery_size = discovery_size
        self.full_map_data = [list(row.replace("'", "")) for row in world_map]
        self.discovered_map = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.player_x = 0
        self.player_y = 0
        self.map_data = [[unexplored_tile for _ in range(self.width)] for _ in range(self.height)]
        self.discover_area()

    def get_tile(self, symbol):
        tile_mapping = {
            '.': plains,
            ',': grasslands,
            'Y': forest,
            '8': dark_forest,
            'A': mountain,
            '=': river,
            '~': lake,
            '#': deep_lake,
            '&': jungle,
            'T': town,
            'F': farmhouse,
            'C': castle,
            'S': store_clerk,
            'B': blacksmith,
            'R': ranger,
            'H': herbalist,
            'P': player_tile,
            'O': old_ruins,
            'J': jungle_temple,
            'V': voodoo_village,
            '$': enchanted_forest,
            'M': frigid_mountain,
            'G': goblin_fortress,
            'W': wisdom_seeker,
        }
        return tile_mapping.get(symbol, unexplored_tile)

    def discover_area(self):
        for y in range(max(0, self.player_y - self.discovery_size),
                       min(self.height, self.player_y + self.discovery_size + 1)):
            for x in range(max(0, self.player_x - self.discovery_size),
                           min(self.width, self.player_x + self.discovery_size + 1)):
                self.discovered_map[y][x] = True

    def move_player(self, direction):
        # Movement logic based on user input ('w', 'a', 's', 'd')
        if direction == 'w' and self.player_y > 0:
            self.player_y -= 1
        elif direction == 's' and self.player_y < self.height - 1:
            self.player_y += 1
        elif direction == 'a' and self.player_x > 0:
            self.player_x -= 1
        elif direction == 'd' and self.player_x < self.width - 1:
            self.player_x += 1

        # After moving, update the discovered area around the player
        self.discover_area()

    def display_map(self):
        clear_screen()
        biomes, buildings, npcs_others = get_legend()

        print(f"{' ' * 23}- World Map -{' ' * 50}- Legend -")
        print(f"x{'-' * self.width}x-----Biomes---------------Buildings-----------NPC-----------x")

        map_lines = []
        for y, row in enumerate(self.full_map_data):
            line = "|"
            for x, symbol in enumerate(row):
                if x == self.player_x and y == self.player_y:
                    line += player_tile.colored_symbol
                elif self.discovered_map[y][x]:
                    tile = self.get_tile(symbol)
                    line += tile.colored_symbol
                else:
                    line += unexplored_tile.colored_symbol
            line += "|"
            map_lines.append(line)

        max_legend_length = max(len(biomes), len(buildings), len(npcs_others))
        for i in range(max(len(map_lines), max_legend_length)):
            map_part = map_lines[i] if i < len(map_lines) else " " * (self.width + 2)
            biomes_part = biomes[i] if i < len(biomes) else " " * 18
            buildings_part = buildings[i] if i < len(buildings) else " " * 18
            npcs_part = npcs_others[i] if i < len(npcs_others) else ""

            print(f"{map_part:<65} {biomes_part:<25} {buildings_part:<18} {npcs_part:<18}")

        print(f"x{'-' * self.width}x------------------------------------------------------------x")


# Define the Player class
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
        self.game_over = False
        self.gold = 100
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None
        self.quests = {''}

    def assign_stats(self):
        role_stats = {
            'warrior': (5, 3, 1, 3, 2, 150, 50),
            'mage': (1, 2, 5, 3, 3, 50, 150),
            'archer': (3, 5, 2, 3, 1, 75, 75)
        }
        self.strength, self.agility, self.intelligence, self.spirit, self.luck, self.hp, self.mp = role_stats[self.role]
        self.hp += self.strength
        self.mp += self.intelligence

    def display_stats(self):
        print("|                     - Player Stats -                       x")
        print(f"|Name: {self.name}            Role: {self.role}            Gold: {self.gold}     x")
        print(f"|HP: {self.hp}                             MP: {self.mp}                  x")
        print(f"|{self.equipped_weapon}: Equipped Weapon                                       x")
        print(f"|{self.equipped_armor}: Equipped Armor                                        x")
        print(f"|{self.strength} :Strength            {self.agility} :Agility                           x")
        print(f"|{self.intelligence} :Intelligence        {self.spirit} : Spirit                           x")
        print(f"|{self.luck} : Luck               {self.armor} : Armor                            x")
        print("x------------------------------------------------------------x")


# Global player instance
my_player = Player()


# Setup the game (Player creation and role assignment)
def setup_game():
    clear_screen()

    question1 = 'Hello friend, what is your name?\n'
    player_name = input(question1)
    my_player.name = player_name

    question2 = 'Tell me friend, what role do you want?\n(You can choose warrior, mage, or archer)\n'
    player_role = input(question2).lower()
    valid_roles = ['warrior', 'mage', 'archer']

    while player_role not in valid_roles:
        player_role = input('Please choose a valid role (warrior, mage, or archer): ').lower()

    my_player.role = player_role
    my_player.assign_stats()  # Assign the appropriate stats based on the role
    print(f'You are now a {player_role}!\n')


# Main game function
def start_game():
    # Setup player and world
    setup_game()

    # Create a Map object with appropriate dimensions
    game_map = Map(width=len(world_map[0]), height=len(world_map))

    while not my_player.game_over:  # The main game loop continues until the player loses
        game_map.display_map()  # Show the map
        my_player.display_stats()  # Show the player's stats below the map
        move = input("Enter your move (w/a/s/d): ").lower()  # Get player movement

        if move in ['w', 'a', 's', 'd']:
            game_map.move_player(move)
        else:
            print("Invalid input! Please use 'w', 'a', 's', or 'd' to move.")


# Title screen
def title_screen():
    clear_screen()
    print('##############################')
    print('#          - Play -          #')
    print('#          - Load -          #')
    print('#          - Help -          #')
    print('#          - Exit -          #')
    print('##############################')

    option = input("> ").lower()
    if option == "play":
        start_game()
    elif option == "help":
        help_menu()
    elif option == "exit":
        exit()
    else:
        print("Invalid selection, please choose again.")
        title_screen()


# Help menu
def help_menu():
    print('##############################################')
    print('- Move with w, a, s, d to navigate the map    ')
    print('- Interact with the environment using commands')
    print('##############################################')

    title_screen()


# Main entry point
if __name__ == "__main__":
    title_screen()
