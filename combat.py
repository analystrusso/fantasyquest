import random
import time
import sys
from spells import spellbook
from character import Player




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
        damage = attacker.attack_power - defender.defense
        result = cls.roll_die(20)
        if result >= defender.armor_class:
            print(f"{attacker.name} hits {defender.name} for {damage} damage!")
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
                Player.level_up(attacker)
                try:
                    current_location.enemies.remove(defender)
                except ValueError:
                    pass
        else:
            print(f"{attacker.name} misses {defender.name}!")

        if defender.health <= 0:
            return
        print(f"{defender.name} attacks {attacker.name}!")
        result = cls.roll_die(20)
        if result >= attacker.armor_class:
            print(f"{defender.name} hits for {damage} damage!")
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
        if not spell:
            print(f"{attacker.name} doesn't know how to cast {spell_name}.")
            return

        if attacker.mana < spell.mana_cost:
            print(f"{attacker.name} doesn't have enough mana to cast {spell_name}.")
            return

        attacker.mana -= spell.mana_cost

        if spell.aoe:
            # AoE logic: target multiple enemies
            targets = current_location.enemies[:spell.max_targets] if spell.max_targets else current_location.enemies
            if not targets:
                print("There are no enemies to target!")
                return
            print(f"{attacker.name} casts {spell.name}, hitting multiple enemies!")
            for target in targets:
                cls.apply_damage(attacker, target, spell, current_location)
        else:
            # Single-target logic
            cls.apply_damage(attacker, defender, spell, current_location)




    @classmethod
    def apply_damage(cls, attacker, defender, spell, current_location):
        damage = spell.damage
        if damage < 0:
            damage = 0
        result = cls.roll_die(20)
        if result >= defender.armor_class:
            print(f"{attacker.name} hits {defender.name} for {damage} damage!")
            defender.health -= damage
            if defender.health <= 0:
                defender.health = 0
                print(f"{defender.name} has been defeated!")
                dropped_item = defender.drop_item(current_location)
                if dropped_item:
                    print(f"{defender.name} dropped {dropped_item.name}.")
                attacker.xp += defender.xp
                current_location.despawn_enemies()
                Player.level_up(attacker)
                try:
                    current_location.enemies.remove(defender)
                except ValueError:
                    pass
        else:
            print(f"{attacker.name} misses {defender.name}!")

        if defender.health <= 0:
            return
        else:
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

