# This example requires the 'members' privileged intents
import random
import itertools
import sqlite3
from bdb import Breakpoint
from room import Room
from character import Character
from monster import Monster
import nextcord
import botToken
from nextcord.ext import commands

description = """An example bot to showcase the nextcord.ext.commands extension
module.

There are a number of utility commands being showcased here."""

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="$", description=description, intents=intents)

# when the bot signs in
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    channel = bot.get_channel(1270832902963466305)
    await channel.send("I'm online!")
@bot.command()
async def add(ctx, left: int, right: int): #ex: $add 1 1 will add 1 and 1
    """Adds two numbers together."""
    await ctx.send(left + right)
@bot.command()
async def sum(ctx, *numbers: int): 
    """Adds multiple numbers together."""
    total = list(itertools.accumulate(numbers))
    try:
        await ctx.send(f"The sum is: {total[-1]}")
    except:
        await ctx.send("Nope")
@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split("d"))
    except ValueError:
        await ctx.send("Format has to be in NdN!") #ex: 1d20 rolls 1 d20
        return

    result = ", ".join(str(random.randint(1, limit)) for _ in range(rolls))
    await ctx.send(result)
@bot.command(description="For when you wanna settle the score some other way")
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))
@bot.command()
async def joined(ctx, member: nextcord.Member):
    """Says when a member joined."""
    await ctx.send(f"{member.name} joined in {member.joined_at}")
@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f"No, {ctx.subcommand_passed} is not cool")
@cool.command(name="Ronen")
async def _Ronen(ctx):
    """Is Ronen cool?"""
    await ctx.send("Yes, Ronen is cool.")

def run():
    # Run away from an attack
    print("You ran away to safety!")

    # premade monsters
goblin = Monster("Goblin", 10, 2, 1)
orc = Monster("Orc", 15, 3, 2)
skeleton = Monster("Skeleton", 5, 1, 0)


def generate(self):
    # Randomly select a room template
    self.template = "monster"
    # self.template = random.choice(["empty", "treasure", "monster", "puzzle"])

    if self.template == "empty":
        self.description = "You find yourself in an empty room."
    elif self.template == "treasure":
        self.description = "You find a chest filled with treasure!"
        self.objects.append("chest")
    elif self.template == "monster":
        self.description = "You find a fearsome monster waiting for you!"
        self.creatures.append("goblin")
    elif self.template == "puzzle":
        self.description = "You find a mysterious puzzle that needs to be solved."
        self.features.append("puzzle")


async def open_door(self, ctx):
    self.generate()@bot.command(name='open')
async def open(ctx, self=None):
    await open_door.generate()
    await ctx.send(self.description)

    while True:
        await ctx.send("What do you do?\n1. Fight\n2. Interact\n3. Explore\n4. RUN!")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await bot.wait_for('message', check=check)

        if msg.content == '1':
            print(self.template)
            if self.template == "monster":
                monster = Monster("Goblin", 10, 2, 1)
                Monster.spawn()
                await ctx.send(f"You engage in combat with the {monster.name}!")
                # Add combat logic here
            elif self.template == "treasure":
                await ctx.send("There is no monster to fight here.")
            elif self.template == "puzzle":
                await ctx.send("You can't fight a puzzle.")
            elif self.template == "empty":
                await ctx.send("There is nothing to fight here.")
        elif msg.content == '2':
            if self.template == "treasure":
                await ctx.send("You open the chest and find gold and treasure!")
                # Add chest interaction logic here
            elif self.template == "monster":
                await ctx.send("There is no chest to interact with here.")
            elif self.template == "puzzle":
                await ctx.send("You can't interact with a puzzle.")
            elif self.template == "empty":
                await ctx.send("There is nothing to interact with here.")
        elif msg.content == '3':
            if self.template == "monster":
                await ctx.send("You explore the room and find a hidden passage!")
                # Add exploration logic here
            elif self.template == "treasure":
                await ctx.send("You explore the room and find a secret compartment in the chest!")
                # Add exploration logic here
            elif self.template == "puzzle":
                await ctx.send("You explore the room and find a hidden clue to the puzzle!")
                # Add exploration logic here
            elif self.template == "empty":
                await ctx.send("You explore the room, but there's nothing to find.")
        elif msg.content == '4':
            await ctx.send("You ran away to safety!")
            break
        else:
            await ctx.send("Invalid choice. Please try again.")


@bot.command(name='open')
async def open(ctx):
    room = Room()
    await room.open_door(ctx)

bot.run(botToken.botToken)