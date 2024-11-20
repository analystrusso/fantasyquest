import random
import time
import sys
from spells import spellbook
from character import Character


# Combat class
class Combat:
    def __init__(self):
        pass

    def roll_die(self, sides=20):
        result = random.randint(1, sides)
        print(result)
        if result in range(18, 21):
            print("Critical hit!")
        elif result == 1:
            print("Critical miss!")
        return result

    @classmethod
    def attack(cls, attacker, defender, current_location):
        result = cls.roll_die(20)
        if result >= defender.armor_class:
            print(f"{attacker.name} hits!")
            damage = attacker.attack_power - defender.defense
            if damage < 0:
                damage = 0
            if result in range(18, 21):
                damage *= 2
            defender.health -= damage
            if defender.health < 0:
                defender.health = 0
                print(f"{defender.name} has been defeated!")
                dropped_item = defender.drop_item(current_location)
                if dropped_item:
                    print(f"{defender.name} dropped {dropped_item.name}.")
                attacker.xp += defender.xp
                current_location.despawn_enemies()
                Character.level_up(attacker)
                try:
                    current_location.enemies.remove(defender)
                except ValueError:
                    pass
        else:
            print(f"{attacker.name} misses {defender.name}!")

        print(f"{defender.name} attacks {attacker.name}!")
        result = cls.roll_die(20)
        if result >= attacker.armor_class:
            print(f"{defender.name} hits!")
            damage = defender.attack_power - attacker.defense
            if damage < 0:
                damage = 0
            if result in range(18, 21):
                damage *= 2
            attacker.health -= damage
            if attacker.health < 0:
                attacker.health = 0
                print(f"{attacker.name} has been defeated!\nGame Over!")
                time.sleep(10)
                sys.exit()

    @classmethod
    def cast(cls, attacker, defender, spell_name, current_location):
        spell = next((v for k, v in spellbook.items() if k.casefold() == spell_name.casefold()), None)
        if spell:
            if attacker.mana >= spell.mana_cost:
                attacker.mana -= spell.mana_cost
                if spell.name == "Heal":
                    if attacker.health < attacker.max_health:
                        heal_amount = min(spell.damage, attacker.max_health - attacker.health)
                        attacker.health += heal_amount
                        print(f"{attacker.name} heals for {heal_amount} health!")
                        return
                damage = spell.damage
                if damage < 0:
                    damage = 0
                result = cls.roll_die(20)
                if result >= defender.armor_class:
                    print(f"{attacker.name} hits!")
                    defender.health -= damage
                    if defender.health < 0:
                        defender.health = 0
                        print(f"{defender.name} has been defeated!")
                        attacker.xp += defender.xp
                        current_location.despawn_enemies()

                        Character.level_up(attacker)
                        try:
                            current_location.enemies.remove(defender)
                        except ValueError:
                            pass
                else:
                    print(f"{attacker.name} misses {defender.name}!")
            else:
                print(f"{attacker.name} doesn't have enough mana to cast {spell_name}.")
        else:
            print(f"{attacker.name} doesn't know how to cast {spell_name}.")

        print(f"{defender.name} attacks {attacker.name}!")
        result = cls.roll_die(20)
        if result >= attacker.armor_class:
            print(f"{defender.name} hits!")
            damage = defender.attack_power - attacker.defense
            if damage < 0:
                damage = 0
            if result in range(18, 21):
                damage *= 2
            attacker.health -= damage
            if attacker.health < 0:
                attacker.health = 0
                print(f"{attacker.name} has been defeated!\nGame Over!")
                time.sleep(10)
                sys.exit()

