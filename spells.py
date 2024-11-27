class Spell:
    def __init__(self, name, mana_cost, damage, aoe, max_targets):
        self.name = name
        self.mana_cost = mana_cost
        self.damage = damage
        self.description = ""
        self.aoe = aoe
        self.max_targets = max_targets


spellbook = {

    "Fireball": Spell("Fireball", 30, 50, aoe=True, max_targets=3),
    "Firebolt": Spell("Firebolt", 20, 25, aoe=False, max_targets=1),
    "Spark": Spell("Spark", 25, 30, aoe=False, max_targets=1),
    "Heal": Spell("Heal", 15, 20, aoe=False, max_targets=1),
    "Greater Heal": Spell("Greater Heal", 30, 50, aoe=False, max_targets=1),
}
