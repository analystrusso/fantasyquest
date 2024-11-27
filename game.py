from character import create_character, Mage
from npc_enemy import Npc
from world import World, Directions
from items import Weapon, Armor
from combat import Combat
from spells import spellbook



class Game:
    def __init__(self):
        self.player = create_character()
        self.world = World.create_world()
        self.current_location = self.world.starting_location



    def display_location(self, location):
        if not location.visited:
            print(location.description)
            print("-------------------------------")
            for direction, connection in location.connected_locations.items():
                print(f"You can go {direction.name.lower()}.")
                location.visited = True
            print("-------------------------------")

        for enemy in location.enemies:
            print(f"You see a {enemy.name} here.")

        for npc in location.npcs:
            print(f"You see a {npc.name} here.")



    def run(self):
        command_handlers = {
            'move': self.handle_move_command,
            'attack': self.handle_attack_command,
            'cast': self.handle_cast_command,
            'spells': self.handle_spells_command,
            'pickup': self.handle_pickup_command,
            'inventory': self.handle_inventory_command,
            'look': self.handle_look_command,
            'status': self.handle_status_command,
            'connections': self.handle_connections_command,
            'talk': self.handle_talk_command,
            'buy': self.handle_buy_command
        }

        while True:
            self.display_location(self.current_location)
            command = input("> ").lower()
            if command == "quit":
                break
            parts = command.split()
            if not parts:
                continue
            if parts[0] in command_handlers:
                command_handlers[parts[0]](command)
            else:
                print("Invalid command. Try again.")

        print("Thanks for playing!")



    def handle_move_command(self, command):
        try:
            direction = Directions.from_str(command.split(' ', 1)[1])
            if direction in self.current_location.connected_locations:
                self.current_location = self.current_location.connected_locations[direction]
            else:
                print(f"you can't move {direction} from here.")
        except IndexError:
            print("Invalid command. Try 'move <direction>'.")



    def handle_attack_command(self, command):
        try:
            enemy_name = command.split(' ', 1)[1]
            enemy = next((e for e in self.current_location.enemies if e.name.lower() == enemy_name.lower()), None)
            if enemy:
                Combat.attack(self.player, enemy, self.current_location)
            else:
                print(f"there is no {enemy_name} here.")
        except IndexError:
            print("Invalid command. Try 'attack <enemy>'.")

    def handle_cast_command(self, command):
        if not isinstance(self.player.char_class, Mage):
            print("You are not a mage. You cannot cast spells.")
            return

        try:
            parts = command.split(' ')
            if len(parts) == 4 and parts[2].lower() == 'on':
                enemy_name = parts[3]
                enemy = next((e for e in self.current_location.enemies if e.name.casefold() == enemy_name.casefold()),
                             None)
                if enemy:
                    Combat.cast(self.player, enemy, parts[1], self.current_location)
                else:
                    print(f"there is no {enemy_name} here.")
            elif len(parts) == 3 and parts[2].lower() == 'self':
                Combat.cast(self.player, self.player, parts[1], self.current_location)
            else:
                print("Invalid command. Try 'cast <spell> on <enemy>' or 'cast <spell> self'.")
        except IndexError:
            print("Invalid command. Try 'cast <spell> on <enemy>' or 'cast <spell> self'.")



    def handle_spells_command(self, command):
        if not isinstance(self.player.char_class, Mage):
            print("You are not a mage. You cannot cast spells.")
            return

        print("Your spells:")
        for spell in spellbook.values():
            print(spell.name)
        print("-------------------------------")


    def update_player_stats(self, item):
        if isinstance(item, Weapon):
            if self.player.equipped_weapon:
                self.player.attack_power -= self.player.equipped_weapon.damage
                self.player.inventory.remove(self.player.equipped_weapon)
            self.player.equipped_weapon = item
            self.player.attack_power += self.player.equipped_weapon.damage

        elif isinstance(item, Armor):
            if self.player.equipped_armor:
                self.player.defense -= self.player.equipped_armor.defense_bonus
                self.player.inventory.remove(self.player.equipped_armor)
            self.player.equipped_armor = item
            self.player.defense += self.player.equipped_armor.defense_bonus



    def handle_pickup_command(self, command):
        parts = command.split()
        if len(parts) < 2 or parts[0].lower() != 'pickup':
            print("Invalid command. Try 'pickup <item>'")
            return
        item_name = ' '.join(parts[1:]).casefold()
        if item_name == 'all':
            for item in self.current_location.items[:]:
                self.player.inventory.append(item)
                self.current_location.items.remove(item)
                self.update_player_stats(item)
            print("You picked up everything.")
        else:
            item = next((i for i in self.current_location.items if i.name.casefold() == item_name), None)
            if item:
                self.player.inventory.append(item)
                self.current_location.items.remove(item)
                print(f"You picked up the {item.name}.")
                self.update_player_stats(item)
            else:
                print(f"There is no {item_name} here.")



    def handle_inventory_command(self, command):
        if command.lower() == "inventory":
            if self.player.inventory:
                print("Inventory:")
                for item in self.player.inventory:
                    print(f"- {item.name}")
            else:
                print("Your inventory is empty.")



    def handle_look_command(self, command):
        if command.lower() == "look":
            print(self.current_location.description)
        else:
            print("Invalid command. Try 'look'.")



    def handle_connections_command(self, command):
        if command.lower() == "connections":
            for direction, location in self.current_location.connected_locations.items():
                print(f"You can go {direction.name.lower()}.")



    def handle_talk_command(self, command):
        parts = command.split()
        if len(parts) < 3 or parts[0].lower() != "talk" or parts[1].lower() != "to":
            print("Invalid command. Try 'talk to' <npc>'")
            return
        else:
            npc_name = ' '.join(parts[2:]).casefold()
            npc = next((n for n in self.current_location.npcs if n.name.casefold() == npc_name), None)
            if npc.name == "Shopkeeper":
                print("------------------------------\nWelcome to my shop, traveller.\nRest a while and take a look at my wares....\n------------------------------")
                for item in npc.shopkeeper_inventory():
                    print(f"- {item.name} | {item.description} | {item.value} gold")
            else:
                print(f"There is no {npc_name} here.")



    def handle_buy_command(self, command):
        parts = command.split()
        if len(parts) < 4 or parts[0].lower() != "buy" or parts[-2].lower() != "from":
            print("Invalid command. Try 'buy <item> from' <npc>'")
            return
        else:
            item_name = ' '.join(parts[1:-2]).casefold()
            npc_name = parts[-1].casefold()
            npc = next((n for n in self.current_location.npcs if n.name.casefold() == npc_name), None)
            if npc:
                item = next((i for i in npc.shopkeeper_inventory() if i.name.casefold() == item_name), None)
                if item:
                    if self.player.gold >= item.value:
                        self.player.gold -= item.value
                        self.player.inventory.append(item)
                        self.update_player_stats(item)
                        npc.shopkeeper_inventory().remove(item)
                        print(f"You bought the {item.name}.")
                    else:
                        print("You don't have enough gold.")
                else:
                    print(f"There is no {item_name} for sale.")
            else:
                print(f"There is no {npc_name} here.")



    def handle_status_command(self, command):
        if command.lower() == "status":
            print(f"Name: {self.player.name}")
            print(f"Race: {self.player.race.__class__.__name__}")
            print(f"Class: {self.player.char_class.__class__.__name__}")
            print(f"Level: {self.player.level}")
            print(f"Health: {self.player.health}")
            print(f"Mana: {self.player.mana}")
            print(f"Attack Power: {self.player.attack_power}")
            print(f"Defense: {self.player.defense}")
            print(f"Armor Class: {self.player.armor_class}")
            print(f"XP: {self.player.xp}")
            print(f"Gold: {self.player.gold}")
