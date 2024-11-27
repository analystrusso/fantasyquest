class Items:
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value




class Weapon(Items):
    def __init__(self, name, description, value, damage):
        super().__init__(name, description, value)
        self.damage = damage

iron_sword = Weapon("Iron Sword", "An old, rusted sword.", 10, 5)
steel_sword = Weapon("Steel Sword", "A sturdy steel sword.", 20, 10)
great_sword = Weapon("Greatsword", "A powerful two-handed sword.", 30, 15)




class Armor(Items):
    def __init__(self, name, description, value, defense_bonus):
        super().__init__(name, description, value)
        self.defense_bonus = defense_bonus

leather_armor = Armor("Leather Armor", "Light leather armor.", 10, 1)
chainmail_armor = Armor("Chainmail Armor", "Sturdy chainmail armor.", 20, 2)
plate_armor = Armor("Plate Armor", "Heavy plate armor.", 30, 3)
