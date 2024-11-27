from character import Player
from items import *




class Npc:
    def __init__(self, name, health, attack_power, defense, armor_class, xp, inventory=None):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.armor_class = armor_class
        self.xp = xp
        self.inventory = []




    @classmethod
    def shopkeeper(cls, inventory):
        shopkeeper = cls("Shopkeeper", 50, 10, 5, 5, 10)
        shopkeeper.inventory = inventory
        return shopkeeper



    def shopkeeper_inventory(self):
        return self.inventory



    def purchase_item(self, item):
        if item in self.inventory and Player.gold >= item.price:
            self.inventory.remove(item)
            return item
        else:
            return None

shopkeeper_inventory = [iron_sword, steel_sword, great_sword]
shopkeeper = Npc.shopkeeper(shopkeeper_inventory)




class Enemy:
    def __init__(self, name, health, attack_power, defense, armor_class, xp, item):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.armor_class = armor_class
        self.xp = xp
        self.item = item



    def drop_item(self, current_location):
        if self.health <= 0:
            current_location.items.append(self.item)
            return self.item
        else:
            return None



    @classmethod
    def goblin(cls):
        return cls("Goblin", 50, 10, 5, 5, 10, iron_sword)



    @classmethod
    def orc(cls):
        return cls("Orc", 100, 15, 10, 10, 20, steel_sword)



    @classmethod
    def troll(cls):
        return cls("Troll", 200, 20, 15, 15, 40, great_sword)

