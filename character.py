import heart
import space


class Character:
    def __init__(self, name, starting_room: space.Room):
        self.name = name
        self.inventory = []
        self.heart = heart.Heart()  # The heart of the character, which is a growing interpretation of the character.
        self.current_room = starting_room.add_character(self)


    def change_room(self, new_room: space.Room):
        if self.current_room is not None:
            self.current_room.characters.remove(self)
        self.current_room = new_room.add_character(self)

    def command_handler(self, command, args):
        if command == "inspect":
            return self.current_room.description
        elif command == "move":
            if args[0] in self.current_room.exits.keys():
                self.move_to(self.current_room.exits[args[0]])
            else:
                print(f"Cannot move {args[0]} from the current room.")
        elif command == "location":
            return self.current_location()
        elif command == "search":
            return self.current_room.get_items()
        else:
            return f"Command {command} not recognized."

    def move_to(self, new_room):
        if new_room in self.current_room.exits.values():
            self.change_room(new_room)
            print(f"{self.name} moved to the {self.current_room.name}")
        else:
            print(f"Cannot move to {new_room.name}. It's not connected to the current room.")

    def current_location(self):
        return f"{self.name} is currently in the {self.current_room.name}"


if __name__ == '__main__':
    universe_a = space.Bubble("UniverseA")
    earth = space.CelestialBody("Earth", "A planet").attach_to_bubble(universe_a)
    johns_house = space.Location("John's house", "A house").attach_to_celestial_body(earth)

    from space import Room

    bedroom = Room("Bedroom", "A cozy bedroom").attach_to_location(johns_house)
    hallway = Room("Hallway", "A long hallway").attach_to_location(johns_house)
    study = Room("Study", "A quiet study").attach_to_location(johns_house)
    balcony = Room("Balcony", "A sunny balcony").attach_to_location(johns_house)

    # Connect rooms
    bedroom.connect_room(hallway, "Hallway")
    hallway.connect_room(study, "Study")
    hallway.connect_room(balcony, "Balcony")

    bedroom.add_object("computer")

    john = Character("John", bedroom)

    print(john.command_handler("location", []))
    print(john.command_handler("search", []))
    print(universe_a.get_hierarchy())
