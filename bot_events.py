import discord
import dotenv
import os

MAIN_GUILD_ID = '1173108848127643688'
HUMANS_CATEGORY_ID = '1173151578031656990'

MASTER_TERMINAL = '1173126604684267541'


class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.players = []
        self.objects = []
        self.exits = []  # List of Room objects that this room is connected to. This is a directed graph.

    def add_object(self, obj):
        self.objects.append(obj)

    def add_player(self, player):
        self.players.append(player)
        return self


class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.rooms = dict()

    def add_room(self, room):
        self.rooms[room.name] = room

    def get_room(self, player):
        return self.rooms[player.current_room]

class House(Location):
    # A house contains rooms, and must contain one "bedroom" room.
    def __init__(self, name, description):
        super().__init__(name, description)
        self.rooms = {"bedroom": Room("bedroom", "A bedroom")}


class Bubble:  # A bubble is a named category which contains a list of channels for different characters.
    def __init__(self, name):
        self.name = name
        self.channels = {}  # A list of channels in the bubble. "John" would be a channel in the bubble "Earth"
        self.locations = {}  # A list of locations in the bubble. "John's house" would be a location in the bubble "Earth"

    def add_location(self, location: Location):
        self.locations[location.name] = location
        return location

    def add_channel(self, channel):
        self.channels[channel] = CharacterChannel(channel)
        return self.channels[channel]


class Hero:
    def __init__(self, name, home_universe: Bubble):
        self.name = name
        self.inventory = []
        self.current_bubble = home_universe
        self.hero_channel = CharacterChannel(self)

        self.current_location = home_universe.add_location(House(f"{name}'s house", "A house"))
        self.current_room = self.current_location.rooms["bedroom"].add_player(self)

    def get_bubble(self):
        return self.current_bubble



class CharacterChannel:  # A channel represents a main character within a location that can be interacted with.
    def __init__(self, character: Hero):
        self.character = character
        self.channel = None

    def command_handler(self, command, args):
        if command == "inspect":
            return self.character.current_room.description

    async def create_channel(self):
        self.channel = await self.character.current_bubble.create_text_channel(self.character.name)

    async def assign_character(self, character):
        self.character = character
        await self._create_discord_channel(character.name, self.current_bubble)

    @staticmethod
    async def _create_discord_channel(name, category):
        return await category.create_text_channel(name)




humans = {}


class MyView(discord.ui.View):  # Create a class called MyView that subclasses discord.ui.View

    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary,
                       emoji="😎")  # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Button clicked!")  # Sends a message to the user who clicked the button


class BotEvents(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_member_join(self, member):
        print(f'{member} has joined the server!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if str(message.channel.id) == MASTER_TERMINAL:
            if message.content.startswith('!'):
                command, args = message.content[1:].split(" ", 1)
                if command == "create_human":
                    human = Human(args[0])
                    humans[args[0]] = human


            return

        if message.channel.category_id == HUMANS_CATEGORY_ID:
            human_name = message.channel.name
            if human_name not in humans:
                humans[human_name] = Human(human_name)
            humans[human_name].inventory.append(message.content)

        if message.content.startswith('!'):
            command, args = message.content[1:].split(" ", 1)
            await message.channel.send(command)
            await message.channel.send(args)

    async def on_message_delete(self, message):
        print('Message deleted from {0.author}: {0.content}'.format(message))


class GameManager:
    def __init__(self):
        self.heroes = {}
        self.bubbles = {}

    def add_hero(self, hero, bubble=None):
        self.heroes[hero.name] = hero
        if bubble:
            self.bubbles[bubble.name].add_channel(hero.name)

    def add_bubble(self, bubble):
        self.bubbles[bubble.name] = bubble


if __name__ == '__main__':
    dotenv.load_dotenv()
    intents = discord.Intents.all()
    bot = BotEvents(intents=intents)
    bot.run(os.getenv("DISCORD_TOKEN"))
