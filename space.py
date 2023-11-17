
class Bubble:
    def __init__(self, id: str):
        self.id = id
        self.celestial_bodies = dict()

    def attach_celestial_body(self, celestial_body: 'CelestialBody') -> 'CelestialBody':
        if celestial_body.id not in self.celestial_bodies:
            self.celestial_bodies[celestial_body.id] = celestial_body
            celestial_body.bubble = self
            return celestial_body
        else:
            print(f"Celestial Body '{celestial_body.id}' already exists in '{self.id}'")

    def find_character(self, character_id: str) -> 'CelestialBody':
        for celestial_body in self.celestial_bodies.values():
            if character_id in list(map(celestial_body.characters, lambda character: character.id)):
                return celestial_body

    def get_hierarchy(self) -> str:
        hierarchy = f"Bubble: {self.id}\n"
        for celestial_body in self.celestial_bodies.values():
            hierarchy += celestial_body.get_hierarchy(indent_level=1)
        return hierarchy

class CelestialBody:
    def __init__(self, id: str, description: str):
        self.id = id
        self.description = description
        self.locations = dict()
        self.bubble = None

    def attach_location(self, location: 'Location') -> 'Location':
        if location.id not in self.locations:
            self.locations[location.id] = location
            location.celestial_body = self
            return location
        else:
            print(f"Location '{location.id}' already exists in '{self.id}'")

    def find_character(self, character_id: str) -> 'Location':
        for location in self.locations.values():
            if character_id in list(map(location.characters, lambda character: character.id)):
                return location

    def get_hierarchy(self, indent_level: int = 0) -> str:
        indent = "  " * indent_level
        hierarchy = f"{indent}Celestial Body: {self.id} - {self.description}\n"
        for location in self.locations.values():
            hierarchy += location.get_hierarchy(indent_level + 1)
        return hierarchy


class Location:
    def __init__(self, id: str, description: str):
        self.id = id
        self.description = description
        self.rooms = []
        self.celestial_body = None

    def attach_room(self, room: 'Room') -> 'Room':
        if room not in self.rooms:
            self.rooms.append(room)
            room.location = self
            return room
        else:
            print(f"Room '{room.id}' already exists in '{self.id}'")

    def find_character(self, character_id: str) -> 'Room':
        for room in self.rooms:
            if character_id in list(map(room.characters, lambda character: character.id)):
                return room
            
    def get_path(self, from_room, to_room) -> list:
        if (from_room in self.rooms) and (to_room in self.rooms):
            # TODO: Implement pathfinding algorithm
            return [from_room, to_room]

    def get_hierarchy(self, indent_level: int = 0) -> str:
        indent = "  " * indent_level
        hierarchy = f"{indent}Location: {self.id} - {self.description}\n"
        for room in self.rooms:
            hierarchy += room.get_hierarchy(indent_level + 1)
        return hierarchy


class Room:
    def __init__(self, id: str, description: str):
        self.id = id
        self.description = description
        self.players = list()
        self.objects = list()
        self.connected_rooms = dict()
        self.location = None

    def connect_room(self, room: 'Room', bidirectional: bool = True, attached: bool = True, *args, **kwargs) -> None:
        if room not in self.connected_rooms:
            connection = f"{room.id}" # + "".join([f"|{arg}" for arg in args]) + "".join([f"|{key}:{value}" for key, value in kwargs.items()])
            self.connected_rooms[connection] = room
            print(self.connected_rooms)
            if bidirectional:
                room.connect_room(self, bidirectional=False, attached=False, *args, **kwargs)
            if attached:
                self.location.attach_room(room)
            
            return connection
        else:
            print(f"Room '{room.id}' already connected to '{self.id}'")

    def get_hierarchy(self, indent_level: int = 0) -> str:
        return "  " * indent_level + f"Room: {self.id} - {self.description}\n"


if __name__ == '__main__':
    universe = Bubble("universe_a")
    earth = universe.attach_celestial_body(CelestialBody("earth", "The planet we live on"))
    johns_house = earth.attach_location(Location("johns_house", "The house John lives in"))

    bedroom = Room("bedroom", "The room John sleeps in")
    hallway = Room("hallway", "The hallway outside John's bedroom")
    study = Room("study", "The study")
    balcony = Room("balcony", "The balcony")


    johns_house.attach_room(bedroom)
    johns_house.attach_room(hallway)
    johns_house.attach_room(study)
    johns_house.attach_room(balcony)

    bedroom.connect_room(hallway)
    hallway.connect_room(study)
    hallway.connect_room(balcony)


    print(johns_house.get_path(bedroom, balcony))
    print(universe.get_hierarchy())