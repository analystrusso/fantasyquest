# Create the player character
def create_character():
    print("Welcome to the Text-Based Adventure Game!")
    name = input("Enter your character's name: ")

    race_dict = {
        '1': Human, 'human': Human,
        '2': Elf, 'elf': Elf,
        '3': Dwarf, 'dwarf': Dwarf
    }
    class_dict = {'1': Warrior, '2': Mage, '3': Archer}

    print("Choose your race:")
    print("1. Human\n2. Elf\n3. Dwarf\n> ")
    race_choice = input("> ")
    race = race_dict.get(race_choice)

    print("Choose your class:")
    print("1. Warrior\n2. Mage\n3. Archer\n> ")
    class_choice = input("> ")
    char_class = class_dict.get(class_choice)  # Default to Warrior if input is invalid

    return Character(name, race(), char_class(), xp=0)


# Character class
class Character:
    def __init__(self, name, race, char_class, xp):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.xp = xp
        self.max_health = 100 + self.race.health_bonus + self.char_class.health_bonus
        self.health = self.max_health
        self.attack_power = 10 + self.race.attack_bonus + self.char_class.attack_bonus
        self.defense = 5 + self.race.defense_bonus + self.char_class.defense_bonus
        self.armor_class = 10
        self.mana = 100
        self.inventory = []
        self.level = 1
        self.equipped_weapon = None
        self.equipped_armor = None

        # Leveling

    def level_up(self):
        if self.xp >= 50 and self.level < 10:
            self.level += 1
            self.max_health += 10
            self.health = self.max_health
            self.mana += 2
            self.attack_power += 2
            self.defense += 1
            print(f"Level up! You are now level {self.level}.")

    def add_item(self, item, quantity=1):
        # Check if the item already exists in the inventory
        for inventory_item in self.inventory:
            if inventory_item['item'].name == item.name:
                inventory_item['quantity'] += quantity
                return
        # If the item is not found, add it to the inventory
        self.inventory.append({'item': item, 'quantity': quantity})

    def remove_item(self, item_name, quantity=1):
        for inventory_item in self.inventory:
            if inventory_item['item'].name == item_name:
                inventory_item['quantity'] -= quantity
                return


    def is_alive(self):
        return self.health > 0


# Races
class Race:
    def __init__(self, health_bonus, attack_bonus, defense_bonus):
        self.health_bonus = health_bonus
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus


class Human(Race):
    def __init__(self):
        super().__init__(10, 2, 2)


class Elf(Race):
    def __init__(self):
        super().__init__(0, 4, 0)


class Dwarf(Race):
    def __init__(self):
        super().__init__(20, 0, 2)


# Classes
class Class:
    def __init__(self, health_bonus, attack_bonus, defense_bonus):
        self.health_bonus = health_bonus
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus


class Warrior(Class):
    def __init__(self):
        super().__init__(10, 6, 6)


class Mage(Class):
    def __init__(self):
        super().__init__(-10, 10, -2)


class Archer(Class):
    def __init__(self):
        super().__init__(10, 8, 4)