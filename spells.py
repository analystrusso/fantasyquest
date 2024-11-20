# Spells and Magic
class Spell:
    def __init__(self, name, mana_cost, damage):
        self.name = name
        self.mana_cost = mana_cost
        self.damage = damage
        self.description = ""


spellbook = {
    "Firebolt": Spell("Firebolt", 20, 25),
    "Spark": Spell("Spark", 25, 30),
    "Heal": Spell("Heal", 15, 20)
}
