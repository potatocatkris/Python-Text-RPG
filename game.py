import os
import pickle
import sys
import time
import random

SCREEN_WIDTH = 100


# Utility functions
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def drop_item(player):
    luck_modifier = player.luck * 1
    roll = random.randint(1, 100)

    if roll <= 3 + luck_modifier:
        return random.choice(epic_loot)
    elif roll <= 15 + luck_modifier:
        return random.choice(rare_loot)
    elif roll <= 40 + luck_modifier:
        return random.choice(uncommon_loot)
    else:
        return random.choice(common_loot)


# Class Definitions
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
        self.turn_count = 0
        self.inventory = []
        self.defense_buff_turns = 0
        self.equipped_weapon = None
        self.equipped_armor = None
        self.gold = 100
        self.quests = {
            'harry': {'active': False, 'completed': False},
            'emily': {'active': False, 'completed': False},
            'archy': {'active': False, 'completed': False, 'boars_slayed': 0}
        }

    def assign_stats(self):
        role_stats = {
            'warrior': (5, 3, 1, 3, 2, 150, 50),
            'mage': (1, 2, 5, 3, 3, 50, 150),
            'archer': (3, 5, 2, 3, 1, 75, 75)
        }
        self.strength, self.agility, self.intelligence, self.spirit, self.luck, self.hp, self.mp = role_stats[self.role]
        self.hp += self.strength
        self.mp += self.intelligence
        self.armor = self.agility

    def melee_damage(self):
        return self.strength * 2

    def ranged_damage(self):
        return self.agility * 2

    def magic_damage(self):
        return self.intelligence * 2

    def regenerate(self):
        if self.turn_count % 2 == 0:
            self.mp += self.spirit

    def update_turn(self):
        self.turn_count += 1
        self.regenerate()
        if self.defense_buff_turns > 0:
            self.defense_buff_turns -= 1

    def add_to_inventory(self, item):
        if len(self.inventory) < 10:
            self.inventory.append(item)
            print(f"{item.name} added to inventory.")
        else:
            print("Inventory is full!")

    def remove_from_inventory(self, item_name):
        for item in self.inventory:
            if item.name == item_name:
                self.inventory.remove(item)
                print(f"{item_name} removed from inventory.")
                return item
        print(f"No item named {item_name} in inventory.")
        return None

    def show_inventory(self):
        if not self.inventory:
            print("Inventory is empty.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"- {item}")

    def deep_wound(self, monster):
        if self.mp >= 30:
            self.mp -= 30
            damage = 20 + self.melee_damage()
            monster.hp -= damage
            monster.status_effects.append({'effect': 'bleed', 'turns': 5, 'damage': 2})
            print(f"{self.name} uses Deep Wound on {monster.name} for {damage} damage and causes bleed!")
        else:
            print("Not enough MP to use Deep Wound!")

    def slam(self, monster):
        if self.mp >= 40:
            self.mp -= 40
            damage = 20 + self.melee_damage()
            monster.hp -= damage
            monster.status_effects.append({'effect': 'stun', 'turns': 2})
            print(f"{self.name} uses Slam on {monster.name} for {damage} damage and stuns it for 2 turns!")
        else:
            print("Not enough MP to use Slam!")

    def to_arms(self, monster):
        if self.mp >= 20:
            self.mp -= 20
            self.defense_buff_turns = 3
            monster.status_effects.append({'effect': 'damage_reduction', 'turns': 3, 'reduction': 0.3})
            print(f"{self.name} uses To Arms! Reduces {monster.name}'s damage by 30% for 3 turns.")
        else:
            print("Not enough MP to use To Arms!")

    def fireball(self, monster):
        if self.mp >= 15:
            self.mp -= 15
            damage = 25 + self.magic_damage()
            monster.hp -= damage
            monster.status_effects.append({'effect': 'burn', 'turns': 2, 'damage': 5})
            print(f"{self.name} uses Fireball on {monster.name} for {damage} and burns it for 2 turns!")
        else:
            print("Not enough MP to use Fireball!")

    def sparks(self, monster):
        if self.mp >= 10:
            self.mp -= 10
            damage = 15 + self.magic_damage()
            if random.random() <= 0.25:
                extra_damage = 25
                damage += extra_damage
                print(
                    f"{self.name} uses Sparks on {monster.name} for {damage} damage! It deals an extra {extra_damage} damage!")
            else:
                print(f"{self.name} uses Sparks on {monster.name} for {damage} damage!")
            monster.hp -= damage
            monster.status_effects.append({'effect': 'shocked', 'turns': 1, 'damage': 25})
        else:
            print("Not enough MP to use Sparks!")

    def magic_barrier(self, monster):
        if self.mp >= 50:
            self.mp -= 50
            self.defense_buff_turns = 3
            self.status_effects.append({'effect': 'damage_reduction', 'turns': 3, 'reduction': 0.3})
            print(f"{self.name} uses Magic Barrier, reducing 30% damage for 3 turns")
        else:
            print("Not enough MP to use Magic Barrier")

    def steady_shot(self, monster):
        if self.mp >= 10:
            self.mp -= 10
            damage = 10 + self.ranged_damage()
            if random.random() <= 0.1:
                extra_damage = 20
                damage += extra_damage
                print(
                    f"{self.name} uses Steady Shot on {monster.name} for {damage}! It deals an extra {extra_damage} damage!")
            else:
                print(f"{self.name} uses Steady Shot on {monster.name} for {damage}!")
            monster.hp -= damage
        else:
            print("Not enough MP to use Steady Shot!")

    def arrow_to_knee(self, monster):
        if self.mp >= 25:
            self.mp -= 25
            damage = 25 + self.ranged_damage()
            monster.status_effects.append({'effect': 'bleed', 'turns': 2, 'damage': 5})
            monster.status_effects.append({'effect': 'immobilize', 'turns': 2})
            print(
                f"{self.name} uses Arrow to the knee on {monster.name} for {damage}, causing it to bleed and be immobilized for 2 turns!")
        else:
            print("Not enough MP to use Arrow to the knee!")

    def desperate_shot(self, monster):
        if self.mp >= 40 and self.hp <= 40:
            self.mp -= 40
            damage = 40 + self.ranged_damage()
            print(f"{self.name} uses Desperate Shot on {monster.name} for {damage}!")
            monster.hp -= damage
        else:
            print("Not enough MP to use Desperate Shot!")

    def equip(self, item):
        if isinstance(item, Armor):
            self.equip_armor(item)
        elif isinstance(item, Weapon):
            self.equip_weapon(item)
        else:
            print("Cannot equip this item.")

    def equip_armor(self, armor):
        if self.equipped_armor:
            self.unequip_armor()
        self.equipped_armor = armor
        self.armor += armor.armor_value
        self.strength += armor.stat_effects.get('strength', 0)
        self.agility += armor.stat_effects.get('agility', 0)
        self.intelligence += armor.stat_effects.get('intelligence', 0)
        print(f"{self.name} equipped {armor.name}.")

    def unequip_armor(self):
        if self.equipped_armor:
            armor = self.equipped_armor
            self.armor -= armor.armor_value
            self.strength -= armor.stat_effects.get('strength', 0)
            self.agility -= armor.stat_effects.get('agility', 0)
            self.intelligence -= armor.stat_effects.get('intelligence', 0)
            self.add_to_inventory(armor)  # Add back to inventory after updating stats
            self.equipped_armor = None
            print(f"{self.name} unequipped {armor.name}.")

    def equip_weapon(self, weapon):
        if self.equipped_weapon:
            self.unequip_weapon()
        self.equipped_weapon = weapon
        self.strength += weapon.stat_effects.get('strength', 0)
        self.agility += weapon.stat_effects.get('agility', 0)
        self.intelligence += weapon.stat_effects.get('intelligence', 0)
        print(f"{self.name} equipped {weapon.name}.")

    def unequip_weapon(self):
        if self.equipped_weapon:
            weapon = self.equipped_weapon
            self.strength -= weapon.stat_effects.get('strength', 0)
            self.agility -= weapon.stat_effects.get('agility', 0)
            self.intelligence -= weapon.stat_effects.get('intelligence', 0)
            self.add_to_inventory(weapon)  # Add back to inventory after updating stats
            self.equipped_weapon = None
            print(f"{self.name} unequipped {weapon.name}.")

    def calculate_damage_reduction(self, damage_type):
        reduction = self.armor * 0.01
        if self.equipped_armor:
            if damage_type == 'melee':
                reduction += self.equipped_armor.melee_reduction
            elif damage_type == 'ranged':
                reduction += self.equipped_armor.ranged_reduction
            elif damage_type == 'magic':
                reduction += self.equipped_armor.magic_reduction
        return reduction


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
        self.armor = agility
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
            self.mp += self.spirit

    def update_turn(self):
        self.turn_count += 1
        self.regenerate()
        for effect in self.status_effects[:]:
            if effect['effect'] == 'bleed':
                self.hp -= effect['damage']
                print(f"{self.name} takes {effect['damage']} bleed damage!")
            effect['turns'] -= 1
            if effect['turns'] <= 0:
                self.status_effects.remove(effect)

    def attack(self, player):
        if any(effect['effect'] == 'stun' for effect in self.status_effects):
            print(f"{self.name} is stunned and cannot attack!")
        else:
            damage = self.melee_damage() - player.armor
            damage_type = 'melee'
            reduction = player.calculate_damage_reduction(damage_type)
            damage = int(damage * (1 - reduction))
            if player.defense_buff_turns > 0:
                damage = int(damage * 0.7)
            if any(effect['effect'] == 'damage_reduction' for effect in self.status_effects):
                damage_reduction_effect = next(
                    effect for effect in self.status_effects if effect['effect'] == 'damage_reduction')
                damage = int(damage * (1 - damage_reduction_effect['reduction']))
            player.hp -= max(0, damage)
            print(f"{self.name} attacks {player.name} for {damage} damage!")

    def is_alive(self):
        return self.hp > 0


class Item:
    def __init__(self, name, quality, stat_effects, turn_count=0):
        self.name = name
        self.quality = quality
        self.stat_effects = stat_effects
        self.turn_count = turn_count

    def __str__(self):
        effects = ', '.join(f"{stat}: {value}" for stat, value in self.stat_effects.items())
        return f"{self.quality.title()} {self.name} ({effects})"


class Armor(Item):
    def __init__(self, name, quality, stat_effects, armor_value, armor_type, melee_reduction, ranged_reduction,
                 magic_reduction):
        super().__init__(name, quality, stat_effects)
        self.armor_value = armor_value
        self.armor_type = armor_type
        self.melee_reduction = melee_reduction
        self.ranged_reduction = ranged_reduction
        self.magic_reduction = magic_reduction

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}, Armor: {self.armor_value}, Type: {self.armor_type}, Reductions (Melee: {self.melee_reduction * 100}%, Ranged: {self.ranged_reduction * 100}%, Magic: {self.magic_reduction * 100}%)"


class Weapon(Item):
    def __init__(self, name, quality, stat_effects, turn_count=0):
        super().__init__(name, quality, stat_effects, turn_count)

    def __str__(self):
        effects = ', '.join(f"{stat}: {value}" for stat, value in self.stat_effects.items())
        return f"{self.quality.title()} {self.name} ({effects})"


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

    def offer_quests(self, player):
        if self.role == "Blacksmith" and not player.quests['harry']['completed']:
            print(f"{self.name} offers you a quest: Retrieve the Lost Sword from the Old Ruins.")
            player.quests['harry']['active'] = True
        elif self.role == "Alchemist" and not player.quests['emily']['completed']:
            print(f"{self.name} offers you a quest: Create a Health or Mana Potion.")
            player.quests['emily']['active'] = True
        elif self.role == "Ranger" and not player.quests['archy']['completed']:
            print(f"{self.name} offers you a quest: Slay 6 Boars.")
            player.quests['archy']['active'] = True
        else:
            print(f"{self.name} has no quests for you.")

    def check_quest_completion(self, player):
        if self.role == "Blacksmith" and player.quests['harry']['active']:
            if any(item.name == 'Lost Sword' for item in player.inventory):
                player.gold += 250
                player.quests['harry']['completed'] = True
                player.quests['harry']['active'] = False
                print(f"{self.name}: Thank you for retrieving the Lost Sword! Here is your reward: 250 gold.")
        elif self.role == "Alchemist" and player.quests['emily']['active']:
            if any(item.name in ['Health Potion', 'Mana Potion'] for item in player.inventory):
                player.gold += 250
                player.quests['emily']['completed'] = True
                player.quests['emily']['active'] = False
                print(f"{self.name}: Thank you for creating the potion! Here is your reward: 250 gold.")
        elif self.role == "Ranger" and player.quests['archy']['active']:
            if player.quests['archy']['boars_slayed'] >= 6:
                player.gold += 250
                player.quests['archy']['completed'] = True
                player.quests['archy']['active'] = False
                print(f"{self.name}: Thank you for slaying the boars! Here is your reward: 250 gold.")

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


# Data Initialization
rusty_armor = Armor("Rusty Armor", "common", {"strength": 3}, 7, "plate", 0.3, 0.2, 0.1)
torn_tunic = Armor("Torn Tunic", "common", {"agility": 3}, 5, "leather", 0.2, 0.3, 0.1)
raggedy_robes = Armor("Raggedy Robes", "common", {"intelligence": 3}, 3, "cloth", 0.1, 0.2, 0.3)
guards_armor = Armor("Guards Armor", "uncommon", {"strength": 5, "spirit": 3}, 13, "plate", 0.3, 0.2, 0.1)
ranger_armor = Armor("Rangers Armor", "uncommon", {"agility": 5, "luck": 3}, 9, "leather", 0.2, 0.3, 0.1)
pupils_robes = Armor("Pupils Robes", "uncommon", {"intelligence": 5, "spirit": 3}, 5, "cloth", 0.1, 0.2, 0.3)
mithril_armor = Armor("Mithril Armor", "rare", {"strength": 9, "spirit": 5, "hp": 30}, 21, "plate", 0.3, 0.2, 0.1)
duskleather_armor = Armor("Duskleather Armor", "rare", {"agility": 9, "luck": 5, "hp": 30}, 15, "leather", 0.2, 0.3,
                          0.1)
radiant_robes = Armor("Radiant Robes", "rare", {"intelligence": 9, "spirit": 5, "mp": 30}, 9, "cloth", 0.1, 0.2, 0.3)
stonewall = Armor("Stonewall", "epic", {"strength": 17, "agility": 9, "spirit": 5, "hp": 50}, 37, "plate", 0.3, 0.2,
                  0.1)
cloak_of_shadows = Armor("Cloak of Shadows", "epic", {"agility": 17, "luck": 9, "spirit": 5, "hp": 50}, 28, "leather",
                         0.2, 0.3, 0.1)
moons_grace = Armor("Moons Grace", "epic", {"intelligence": 17, "spirit": 9, "luck": 5, "mp": 50}, 17, "cloth", 0.1,
                    0.2, 0.3)
training_sword = Weapon("Training Sword", "common", {"strength": 1})
old_bow = Weapon("Old Bow", "common", {"agility": 1})
used_staff = Weapon("Used Staff", "common", {"intelligence": 1})
iron_mace = Weapon("Iron Mace", "uncommon", {"strength": 2, "agility": 1})
oak_staff = Weapon("Oak Staff", "uncommon", {"intelligence": 2, "spirit": 2})
willow_bow = Weapon("Willow Bow", "uncommon", {"agility": 2, "luck": 2})
mithril_axe = Weapon("Mithril Axe", "rare", {"strength": 5, "agility": 4, "hp": 20})
ebony_staff = Weapon("Ebony Staff", "rare", {"intelligence": 5, "spirit": 4, "mp": 20})
maple_bow = Weapon("Maple Bow", "rare", {"agility": 5, "luck": 4, "spirit": 2})
troll_slayer = Weapon("Troll Slayer", "epic", {"strength": 12, "agility": 10, "hp": 50, "spirit": 6})
rising_tides = Weapon("Rising Tides", "epic", {"intelligence": 12, "spirit": 10, "mp": 50, "luck": 6})
nightdraw = Weapon("Nightdraw", "epic", {"agility": 12, "luck": 10, "spirit": 6, "hp": 50})
empty_vial = Item("Empty Vial", "common", {})
bloodrose = Item("Bloodrose", "common", {})
lifeseed = Item("Lifeseed", "common", {})
rockweed = Item("Rockweed", "common", {})
health_potion = Item("Health Potion", "common", {"hp_restore": 40})
mana_potion = Item("Mana Potion", "common", {"mp_restore": 40})
rock_solid_potion = Item("Rock Solid Potion", "common", {"armor": 20}, 3)
common_loot = [training_sword, old_bow, used_staff, rusty_armor, torn_tunic, raggedy_robes]
uncommon_loot = [iron_mace, oak_staff, willow_bow, guards_armor, ranger_armor, pupils_robes]
rare_loot = [mithril_axe, ebony_staff, maple_bow, mithril_armor, duskleather_armor, radiant_robes]
epic_loot = [troll_slayer, rising_tides, nightdraw, stonewall, cloak_of_shadows, moons_grace]
herbs = [bloodrose, lifeseed, rockweed]
consumables = [health_potion, mana_potion]
lost_sword = Item("Lost Sword", "common", {})
ITEM_PRICES = {
    'common': 10,
    'uncommon': 25,
    'rare': 500,
    'epic': 3000,
    'consumables': 30,
    'bloodrose': 5,
    'lifeseed': 10,
    'rockweed': 10,
    'empty vial': 5
}
boar_template = Monster("Boar", 20, 0, 5, 3, 1, 3, 1)
wolf_template = Monster("Wolf", 50, 0, 7, 6, 3, 4, 2)
bandit_template = Monster("Bandit", 100, 0, 6, 5, 3, 5, 3)
troll_template = Monster("Forest Troll", 250, 100, 10, 10, 6, 5, 3)

npc1 = NPC(
    name="Harry",
    role="Blacksmith",
    location="a4",
    quests=["Find the lost sword"],
    inventory=["Training Sword", "Iron Mace", "Rusty Armor"],
    rumors=["Scouts located lost ruins somewhere south from here, search for the ruins and retrieve the sword"],
    dialogue={'greeting': "Welcome to my blacksmith shop, adventurer! How can I assist you today?"}
)
npc2 = NPC(
    name="Emily",
    role="Alchemist",
    location="b2",
    quests=["Create your first potion"],
    inventory=["Health Potion", "Mana Potion", "Rock Solid Potion"],
    rumors=["You can try to forage in the forest and dense forest for herbs"],
    dialogue={'greeting': "Hello! Care to trade some goods?"},
)

npc3 = NPC(
    name="Archy",
    role="Ranger",
    location="a1",
    quests=["Slay 6 boars"],
    inventory=[""],
    rumors=["Boars usually roam the grasslands and forest"],
)

npcs = {
    'a2': [npc2],
    'a4': [npc1],
    'a1': [npc3],
    'b2': [npc2]  # Ensure Emily is here in the Alchemy Shop
}

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
        'monsters': [boar_template]
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
        'monsters': [boar_template]
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
        'monsters': [boar_template]
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
        'monsters': [boar_template]
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
        'monsters': [wolf_template]
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
        'monsters': [wolf_template]
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
        'monsters': [wolf_template, bandit_template]
    },
    'd3': {
        ZONENAME: 'Lumber Mill',
        DESCRIPTION: 'An old lumber mill used by the village',
        EXAMINATION: 'It seems no one is around, the whole place looks like a mess, it looks like a fight was here not '
                     'that long ago',
        SOLVED: False,
        UP: 'c3',
        DOWN: None,
        LEFT: 'd2',
        RIGHT: 'd4',
        'monsters': [bandit_template]
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
        'monsters': [bandit_template]
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
        'monsters': [troll_template]
    },
}


# Game Logic Functions
def create_monster(monster_template):
    return Monster(monster_template.name, monster_template.hp, monster_template.mp, monster_template.strength,
                   monster_template.agility, monster_template.intelligence, monster_template.spirit,
                   monster_template.luck)


def battle(monster):
    print(f"A wild {monster.name} appears!")
    while monster.is_alive() and my_player.hp > 0:
        display_battle_ui(my_player, monster)
        action = input("Choose an action: (1) Attack (2) Use Skill (3) Use Item (4) Flee: ").lower()
        if action == '1':
            damage = my_player.melee_damage()
            monster.hp -= damage
            print(f"{my_player.name} attacks {monster.name} for {damage} damage!")
        elif action == '2':
            if my_player.role == 'warrior':
                skill = input("Choose a skill: (1) Deep Wound (2) Slam (3) To Arms: ").lower()
                if skill == '1':
                    my_player.deep_wound(monster)
                elif skill == '2':
                    my_player.slam(monster)
                elif skill == '3':
                    my_player.to_arms(monster)
                else:
                    print("Invalid skill!")
            elif my_player.role == 'mage':
                skill = input("Choose a spell: (1) Fireball (2) Sparks (3) Magic Barrier: ").lower()
                if skill == '1':
                    my_player.fireball(monster)
                elif skill == '2':
                    my_player.sparks(monster)
                elif skill == '3':
                    my_player.magic_barrier(monster)
                else:
                    print("Invalid spell!")
            elif my_player.role == 'archer':
                skill = input("Choose a skill: (1) Steady Shot (2) Arrow to the knee (3) Desperate Shot: ").lower()
                if skill == '1':
                    my_player.steady_shot(monster)
                elif skill == '2':
                    my_player.arrow_to_knee(monster)
                elif skill == '3':
                    my_player.desperate_shot(monster)
                else:
                    print("Invalid skill!")
        elif action == '3':
            pass
        elif action == '4':
            print("You fled the battle.")
            return
        else:
            print("Invalid action!")

        if monster.is_alive():
            monster.attack(my_player)
            my_player.update_turn()
            monster.update_turn()

    if my_player.hp <= 0:
        print("You have been defeated.")
        my_player.game_over = True
    elif not monster.is_alive():
        print(f"You defeated the {monster.name}!")
        if monster.name == "Boar" and my_player.quests['archy']['active']:
            my_player.quests['archy']['boars_slayed'] += 1
        dropped_item = drop_item(my_player)
        print(f"You found a {dropped_item}!")
        my_player.add_to_inventory(dropped_item)


def hunt():
    location = my_player.location
    if 'monsters' in zonemap[location]:
        possible_monsters = zonemap[location]['monsters']
        monster_template = random.choice(possible_monsters)
        monster = create_monster(monster_template)
        battle(monster)
    else:
        print("There are no monsters to hunt here.")


def forage():
    roll = random.randint(1, 100)

    if roll <= 20:
        location = my_player.location
        if 'monsters' in zonemap[location]:
            possible_monsters = zonemap[location]['monsters']
            monster_template = random.choice(possible_monsters)
            monster = create_monster(monster_template)
            battle(monster)
        return
    elif roll <= 40:
        found_items = [Item("Bloodrose", "common", {}), Item("Lifeseed", "common", {}), Item("Rockweed", "common", {})]
        print("Lucky me, I found a Bloodrose, Lifeseed, and Rockweed")
        for item in found_items:
            my_player.add_to_inventory(item)
    elif roll <= 60:
        found_item = Item("Bloodrose", "common", {})
        print("You found a Bloodrose!")
        my_player.add_to_inventory(found_item)
    elif roll <= 80:
        found_item = Item("Lifeseed", "common", {})
        print("You found a Lifeseed!")
        my_player.add_to_inventory(found_item)
    elif roll <= 100:
        found_item = Item("Rockweed", "common", {})
        print("You found a Rockweed!")
        my_player.add_to_inventory(found_item)
    else:
        print("You didn't find anything.")


def buy_item(player, npc):
    if npc == "Harry":
        items_for_sale = [item for item in player.inventory if isinstance(item, Armor) or isinstance(item, Item)]
    elif npc == "Emily":
        items_for_sale = [Item("Health Potion", "common", {"hp_restore": 40}),
                          Item("Mana Potion", "common", {"mp_restore": 40}),
                          Item("Rock Solid Potion", "common", {"armor": 20})]
    else:
        return

    print(f"{npc} has the following items for sale:")
    for i, item in enumerate(items_for_sale):
        price = ITEM_PRICES.get(item.quality, 0)
        print(f"{i + 1}. {item} - {price}g")

    choice = int(input("Which item would you like to buy? (Enter number): ")) - 1
    if choice < 0 or choice >= len(items_for_sale):
        print("Invalid choice.")
        return

    item = items_for_sale[choice]
    price = ITEM_PRICES.get(item.quality, 0)
    if player.gold >= price:
        player.gold -= price
        player.add_to_inventory(item)
        print(f"Bought {item.name} for {price}g.")
    else:
        print("Not enough gold.")


def sell_item(player, npc):
    if npc != "Harry":
        print(f"{npc} does not buy items.")
        return

    player.show_inventory()
    item_name = input("Which item would you like to sell? (Enter name): ")
    item = player.remove_from_inventory(item_name)
    if item:
        price = ITEM_PRICES.get(item.quality, 0) // 2
        player.gold += price
        print(f"Sold {item.name} for {price}g.")
    else:
        print(f"No item named {item_name} found in inventory.")


def create_potion(player):
    required_items = {'empty vial': 1, 'bloodrose': 2, 'lifeseed': 1}

    for item, quantity in required_items.items():
        count = sum(1 for i in player.inventory if i.name == item)
        if count < quantity:
            print(f"Not enough {item}.")
            return

    for item, quantity in required_items.items():
        for _ in range(quantity):
            player.remove_from_inventory(item)

    potion = Item("Health Potion", "common", {"hp_restore": 30})
    player.add_to_inventory(potion)
    print("Created Health Potion.")

    if player.quests['emily']['active']:
        player.quests['emily']['completed'] = True
        player.gold += 250
        player.quests['emily']['active'] = False
        print("You have completed Emily's quest! You earned 250 gold.")


def buy_ingredients(player):
    ingredients = [Item("Bloodrose", "common", {}), Item("Lifeseed", "common", {})]
    for ingredient in ingredients:
        print(f"{ingredient.name} - {ITEM_PRICES[ingredient.name.lower()]}g")

    ingredient_name = input("Which ingredient would you like to buy? ")
    quantity = int(input(f"How many {ingredient_name}s would you like to buy? "))
    price = ITEM_PRICES[ingredient_name.lower()] * quantity

    if player.gold >= price:
        player.gold -= price
        for _ in range(quantity):
            ingredient = next((item for item in ingredients if item.name.lower() == ingredient_name.lower()), None)
            if ingredient:
                player.add_to_inventory(ingredient)
        print(f"Bought {quantity} {ingredient_name}(s) for {price}g.")
    else:
        print("Not enough gold.")


# UI Functions
def display_battle_ui(player, monster):
    clear_screen()
    print("#################### BATTLE ####################")
    print(f"Player: {player.name} | Role: {player.role}")
    total_hp = 150 if player.role == 'warrior' else 50 if player.role == 'mage' else 75
    total_mp = 50 if player.role == 'warrior' else 150 if player.role == 'mage' else 75
    total_hp += player.strength
    total_mp += player.intelligence
    print(f"HP: {player.hp}/{total_hp}    MP: {player.mp}/{total_mp}")
    print(f"Strength: {player.strength}  Agility: {player.agility}")
    print(f"Intelligence: {player.intelligence}  Spirit: {player.spirit}")
    print(f"Luck: {player.luck}  Armor: {player.armor}")
    print(f"Defense Buff Turns Remaining: {player.defense_buff_turns}")
    print("------------------------------------------------")
    print(f"Monster: {monster.name}")
    print(f"HP: {monster.hp}    MP: {monster.mp}")
    print(f"Strength: {monster.strength}  Agility: {monster.agility}")
    print(f"Intelligence: {monster.intelligence}  Spirit: {monster.spirit}")
    print(f"Luck: {monster.luck}  Armor: {monster.armor}")
    for effect in monster.status_effects:
        if effect['effect'] == 'stun':
            print(f"{monster.name} is stunned for {effect['turns']} more turns.")
    print("################################################")


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
    print('##############################')
    print('#          - Play -          #')
    print('#          - Load -          #')
    print('#          - Help -          #')
    print('#          - Exit -          #')
    print('# Copyright 2024 Krystian S  #')
    print('##############################')

    title_screen_selection()


def help_menu():
    print('################################################################')
    print('- Move, go, travel, or walk to move around in game')
    print('- Examine, inspect, interact, or look to see whats going on ')
    print('- Map will show display the player as P on the map ')
    print('- Npc will interact with local npcs if they are there')
    print('- Hunt will look for any monsters to battle, be ready')
    print('################################################################')

    title_screen()


def print_location():
    location = my_player.location
    print('\n' + ('#' * (80 + len(location))))
    print('# ' + zonemap[location][DESCRIPTION] + ' #')


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


def prompt():
    print('\n##############################')
    print('# What would you like to do? #')
    action = input('>').lower()
    acceptable_actions = ['move', 'go', 'travel', 'walk', 'examine', 'inspect', 'interact', 'look', 'map', 'npc',
                          'save', 'hunt', 'inventory', 'equip', 'unequip', 'forage', 'buy', 'sell', 'create potion']
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
    elif action == 'inventory':
        my_player.show_inventory()
    elif action == 'equip':
        equip_item()
    elif action == 'unequip':
        unequip_item()
    elif action == 'forage':
        forage()
    elif action == 'buy':
        npc = input("Who would you like to buy from? (Harry/Emily): ").capitalize()
        buy_item(my_player, npc)
    elif action == 'sell':
        npc = input("Who would you like to sell to? (Harry/Emily): ").capitalize()
        sell_item(my_player, npc)
    elif action == 'create potion':
        create_potion(my_player)


def equip_item():
    my_player.show_inventory()
    item_name = input("Which item would you like to equip? ")
    item = my_player.remove_from_inventory(item_name)
    if item:
        my_player.equip(item)
    else:
        print(f"No item named {item_name} found in inventory.")


def unequip_item():
    if my_player.equipped_armor:
        my_player.unequip_armor()
    else:
        print("No armor is currently equipped.")

    if my_player.equipped_weapon:
        my_player.unequip_weapon()
    else:
        print("No weapon is currently equipped.")


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
        display_map()
    else:
        print("You can't go that way!")


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
            while True:
                print(f"\nOptions with {npc.name}:")
                print("1. Buy Items")
                print("2. Sell Items")
                print("3. Get Quests")
                print("4. Hear Rumors")
                print("5. Leave")

                choice = input("Choose an option (1-5): ").strip()

                if choice == '1':
                    buy_item(my_player, npc.name)
                elif choice == '2':
                    sell_item(my_player, npc.name)
                elif choice == '3':
                    npc.offer_quests(my_player)
                    npc.check_quest_completion(my_player)
                elif choice == '4':
                    npc.share_rumors()
                elif choice == '5':
                    print(f"You leave {npc.name}.")
                    break
                else:
                    print("Invalid choice, please select a valid option.")
    else:
        print("There is no one here to talk to.")


def start_game():
    global my_player
    my_player = Player()
    setup_game()
    main_game_loop()


def main_game_loop():
    while not my_player.game_over:
        prompt()


def setup_game():
    clear_screen()

    question1 = 'Hello friend, what is your name?\n'
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

    # Set the initial player location to 'b2'
    my_player.location = 'b2'

    main_game_loop()


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
            print_location()
    else:
        print("No save file found.")


# Main Execution
if __name__ == "__main__":
    my_player = None
    title_screen()
