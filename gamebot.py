import random
import itertools
import nextcord
import botToken
from nextcord.ext import commands

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
    await ctx.send("What do you do?\n1. Fight\n2. Interact\n3. Explore\n4. RUN!")
@bot.command(name='open')
async def open(ctx):
    print("open command called")
    room = Room()
    await open_door(ctx, room)


bot.run(botToken.botToken)