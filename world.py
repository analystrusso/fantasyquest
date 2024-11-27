from enum import Enum, auto
from npc_enemy import Npc, Enemy, shopkeeper_inventory




class Directions(str, Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()
    UP = auto()
    DOWN = auto()




    @classmethod
    def from_str(cls, value: str) -> 'Directions':
        mapping = {
            'n': cls.NORTH,
            's': cls.SOUTH,
            'e': cls.EAST,
            'w': cls.WEST,
            'u': cls.UP,
            'd': cls.DOWN
        }
        return mapping.get(value.lower())



class Location:
    def __init__(self, name, description):
        self.description = description
        self.name = name
        self.connected_locations = {}
        self.npcs = []
        self.enemies = []
        self.visited = False
        self.items = []



    def add_connection(self, direction, location):
        self.connected_locations[direction] = location



    def spawn_npcs(self):
        if self.description == "You are standing in the town square. There are people around, and the air smells of fresh bread.":
            self.npcs.append(Npc.shopkeeper(shopkeeper_inventory))



    def get_npcs(self):
        return self.npcs



    enemy_spawns = {
        "town_square": [],
        "forest": [Enemy.goblin, Enemy.goblin, Enemy.goblin],
        "outside_cave": [Enemy.orc],
        "inside_cave": [Enemy.troll]}



    def spawn_enemies(self):
        for enemy in self.enemy_spawns.get(self.name, []):
            self.enemies.append(enemy())



    def despawn_enemies(self):
        for enemy in self.enemies[:]:
            if enemy.health <= 0:
                self.enemies.remove(enemy)



    def get_enemies(self):
        return self.enemies



class World:
    def __init__(self, locations, starting_location):
        self.locations = locations
        self.starting_location = starting_location




    @classmethod
    def create_world(cls):
        locations = {
            "town_square": Location("town_square", "You are standing in the town square. There are people around, and the air smells of fresh bread."),
            "forest": Location("forest", "You are in a dense forest. It's quiet, and the trees tower above you."),
            "secluded_clearing": Location("secluded_clearing", "You are in a secluded clearing. It's peaceful and serene."),
            "outside_cave": Location("outside_cave", "You are outside a dark cave. Strange noises echo from within."),
            "inside_cave": Location("inside_cave", "You walk into the dark cave, stooping to fit in the cramped space.")
        }

        locations["town_square"].add_connection(Directions.EAST, locations["forest"])
        locations["forest"].add_connection(Directions.WEST, locations["town_square"])
        locations["forest"].add_connection(Directions.NORTH, locations["outside_cave"])
        locations["forest"].add_connection(Directions.EAST, locations["secluded_clearing"])
        locations["secluded_clearing"].add_connection(Directions.WEST, locations["forest"])
        locations["outside_cave"].add_connection(Directions.SOUTH, locations["forest"])
        locations["outside_cave"].add_connection(Directions.DOWN, locations["inside_cave"])
        locations["inside_cave"].add_connection(Directions.UP, locations["outside_cave"])

        for location in locations.values():
            location.spawn_enemies()
            location.spawn_npcs()

        return cls(locations, locations["town_square"])
