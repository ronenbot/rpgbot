import random
import itertools
import nextcord
import botToken
from nextcord.ext import commands
from room import Room
from monster import Monster
description = "Eplore the Dungeon, fight monsters, find treasure and survive!"
intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
characters = {} #dictionary for character storage

bot = commands.Bot(command_prefix="$", description=description, intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    channel = bot.get_channel(1270832902963466305)
    await channel.send("I'm online!")

def create_character(user_id):
    # Your character creation logic here
    character = {
        'name': f"User {user_id}",
        'health': 100,
        'attack': 10,
        'defense': 5
    }
    return character
async def run():
    print("You ran away to safety!")
@bot.command()
async def create(ctx):
    try:
        user_id = ctx.author.id
        if user_id not in characters:
            character = create_character(user_id)
            characters[user_id] = character
            await ctx.send(f"Character created!\n{character}")
        else:
            await ctx.send("You already have a character!")
    except Exception as e:
        print(f"Error: {e}")
@bot.command(description="For when you wanna settle the score some other way")
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))
async def open_door(ctx, room):
    print("open_door called")
    room.generate()
    await ctx.send(room.description)

    while True:
        await ctx.send("What do you do?\n1. Fight\n2. Interact\n3. Explore\n4. RUN!")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await bot.wait_for('message', check=check)

        if msg.content == '1':
            print(room.template)
            if room.template == "monster":
                monster = Monster("Goblin", 10, 2, 1)
                Monster.spawn()
                await ctx.send(f"You engage in combat with the {monster.name}!")
                # Add combat logic here
            elif room.template == "treasure":
                await ctx.send("There is no monster to fight here.")
            elif room.template == "puzzle":
                await ctx.send("You can't fight a puzzle.")
            elif room.template == "empty":
                await ctx.send("There is nothing to fight here.")
        elif msg.content == '2':
            if room.template == "treasure":
                await ctx.send("You open the chest and find gold and treasure!")
                break
                # Add chest interaction logic here
            elif room.template == "monster":
                await ctx.send("There is no chest to interact with here.")
            elif room.template == "puzzle":
                await ctx.send("You can't interact with a puzzle.")
            elif room.template == "empty":
                await ctx.send("There is nothing to interact with here.")
        elif msg.content == '3':
            if room.template == "monster":
                await ctx.send("You explore the room and find a hidden passage!")
                # Add exploration logic here
            elif room.template == "treasure":
                await ctx.send("You explore the room and find a secret compartment in the chest!")
                # Add exploration logic here
            elif room.template == "puzzle":
                await ctx.send("You explore the room and find a hidden clue to the puzzle!")
                # Add exploration logic here
            elif room.template == "empty":
                await ctx.send("You explore the room, but there's nothing to find.")
        elif msg.content == '4':
            await ctx.send("You ran away to safety!")
            break
        else:
            await ctx.send("Invalid choice. Please try again.")
@bot.command(name='open')
async def open(ctx):
    print("open command called")
    room = Room()
    await open_door(ctx, room)


bot.run(botToken.botToken)