class Bubble:
    def __init__(self, id: str):
        self.id = id
        self.celestial_bodies = {}

    def attach_celestial_body(self, celestial_body):
        if celestial_body.id not in self.celestial_bodies:
            self.celestial_bodies[celestial_body.id] = celestial_body
            celestial_body.bubble = self
            return self
        else:
            print(f"Celestial Body '{celestial_body.id}' already exists in '{self.id}'")

    def get_hierarchy(self):
        hierarchy = f"Bubble: {self.id}\n"
        for celestial_body in self.celestial_bodies.values():
            hierarchy += celestial_body.get_hierarchy(indent_level=1)
        return hierarchy


class HomePlanetBubble(Bubble):
    pass  # Specific methods or properties for the home planet


class IncipisphereBubble(Bubble):
    pass  # Specific methods or properties for the Incipisphere


class CelestialBody:
    def __init__(self, id: str, description: str, bubble=None):
        self.id = id
        self.description = description
        self.locations = {}  # Locations on the celestial body
        self.bubble = bubble.attach_celestial_body(self) if bubble else None

    def attach_location(self, location):
        if location.id not in self.locations:
            self.locations[location.id] = location
            location.celestial_body = self
            return self
        else:
            print(f"Location '{location.id}' already exists in '{self.id}'")

    def attach_to_bubble(self, bubble):
        bubble.attach_celestial_body(self)
        return self

    def get_hierarchy(self, indent_level=0):
        indent = "  " * indent_level
        hierarchy = f"{indent}Celestial Body: {self.id} - {self.description}\n"
        for location in self.locations.values():
            hierarchy += location.get_hierarchy(indent_level + 1)
        return hierarchy


class Location:
    def __init__(self, id: str, description: str, celestial_body=None):
        self.id = id
        self.description = description
        self.rooms = {}
        self.celestial_body = celestial_body.attach_location(self) if celestial_body else None
    
    def attach_room(self, room):
        if room.id not in self.rooms:
            self.rooms[room.id] = room
            room.set_location(self)
            return self
        else:
            print(f"Room '{room.id}' already exists in '{self.id}'")

    def attach_to_celestial_body(self, celestial_body):
        celestial_body.attach_location(self)
        return self

    def get_hierarchy(self, indent_level=0):
        indent = "  " * indent_level
        hierarchy = f"{indent}Location: {self.id} - {self.description}\n"
        for room in self.rooms.values():
            hierarchy += room.get_hierarchy(indent_level + 1)
        return hierarchy

# class House(Location):
#     def __init__(self, id: str, description: str):
#         super().__init__(id, description)
#         self.rooms = {}
        
#         self.attach_room(Room("Living Room", "A room for living"))


class Room:
    def __init__(self, id: str, description: str, location=None):
        self.id = id
        self.description = description
        self.characters = []  # Characters in the room
        self.objects = []  # Objects in the room
        self.location = location.attach_room(self) if location else None

        self.connected_rooms = {}  # Adjacency list for connected rooms, the string id can potentially contain metadata about the connection. For example, "hallway|locked|key:1234" could indicate a locked door that can be unlocked with the key 1234
    
    def set_location(self, location):
        self.location = location.attach_room(self)
        return self

    def connect_room(self, room, bidirectional=True, attached=True, *args, **kwargs):
        if room not in self.connected_rooms.values():
            connection = f"{room.id}" + "".join([f"|{arg}" for arg in args]) + "".join([f"|{key}:{value}" for key, value in kwargs.items()])
            self.connected_rooms[connection] = room

            if bidirectional:
                room.connect_room(self, bidirectional=False, attached=False)
            if attached:
                self.location.attach_room(room)  # Attach the room to the same location as the current room

                
            return room
        else:
            print(f"Room '{room.id}' already connected to '{self.id}'")

    
    def disconnect(self):
        for connection, connected_room in list(self.connected_rooms.items()):
            self.disconnect_room(connected_room)
            connected_room.disconnect_room(self)
        return self

    def disconnect_room(self, room):
        for connection, connected_room in list(self.connected_rooms.items()):
            if connected_room == room:
                del self.connected_rooms[connection]
        return self

    def add_character(self, character):
        self.characters.append(character)
        return self

    def add_object(self, item):
        self.objects.append(item)
        return self

    def get_hierarchy(self, indent_level=0):
        indent = "  " * indent_level
        return f"{indent}Room: {self.id} - {self.description}\n"

if __name__ == '__main__':
    universe = Bubble("universe_a")
    earth = CelestialBody("earth", "The planet we live on", universe)
    johns_house = Location("john_house", "The house John lives in", earth)


    bedroom = Room("bedroom", "The room John sleeps in", johns_house)

    hallway = Room("hallway", "The hallway outside John's bedroom", johns_house)
    bedroom.connect_room(hallway)


    print(universe.get_hierarchy())
    