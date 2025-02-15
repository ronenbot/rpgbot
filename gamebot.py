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
# Global variables
user_attack = 10
user_defense = 5
user_health = 100

# Monster variables
monster_attack = 15
monster_defense = 10
monster_health = 50
# Combat logic
async def combat_logic(ctx):
    global user_health, monster_health
    # User attacks monster
    monster_damage = max(0, user_attack - monster_defense)
    monster_health -= monster_damage

    # Monster attacks back
    if monster_health > 0:
        user_damage = max(0, monster_attack - user_defense)
        user_health -= user_damage
        await ctx.send("The monster dealt", user_damage, "damage to you!")

    # Check if user or monster is dead
    if user_health <= 0:
        await ctx.send("You died!")
    elif monster_health <= 0:
        await ctx.send("You killed the monster!")

@bot.command()
async def run(ctx):
    await ctx.send("You ran away to safety!")
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
@bot.command()
async def roll(ctx, dice: str = "1d100"):
    """Rolls a dice in NdN format. Defaults to 1d100 if no argument is provided."""
    try:
        if dice == "1d100":
            result = random.randint(1, 100)
        else:
            rolls, limit = map(int, dice.split("d"))
            result = [random.randint(1, limit)]
            result = result[-1]  # Return the last roll result
    except ValueError:
        await ctx.send("Format has to be in NdN!") #ex: 1d20 rolls 1 d20
        return

    await ctx.send(str(result)) # Send the roll result to the channel
    return result
async def open_door(ctx, room):
    print("open_door called")
    room.generate()
    await ctx.send(room.description)

    while True:
        await ctx.send("What do you do?\n1. Fight\n2. Loot\n3. Explore\n4. RUN!")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await bot.wait_for('message', check=check)

        if room.template == "monster":
            monster = Monster("Goblin", 10, 2, 1)
            Monster.spawn()
            if msg.content == '1':
                await ctx.send(f"You engage in combat with the {monster.name}!")
                await combat_logic(ctx)
            elif msg.content == '2':
                roll_result = await roll(ctx)  # Roll a 1d100
                if roll_result >= 90:
                    await ctx.send("Looting successful! You found some treasure!")
                else:
                    await ctx.send("Looting failed!")
            elif msg.content == '3':
                await ctx.send("You explore the room and find a hidden passage!")
                break
            elif msg.content == '4':
                await ctx.invoke(bot.get_command('run'))
                break
            else:
                await ctx.send("Invalid choice. Please try again.")
        elif room.template == "treasure":
            if msg.content == '1':
                await ctx.send("You destroy the treasure.")
                break
            elif msg.content == '2':
                await ctx.send("You open the chest and find gold and treasure!")
            elif msg.content == '3':
                await ctx.send("You explore the room and find a secret compartment in the chest!")
            elif msg.content == '4':
                await ctx.invoke(bot.get_command('run'))
                break
            else:
                await ctx.send("Invalid choice. Please try again.")
        elif room.template == "puzzle":
            if msg.content == '1':
                await ctx.send("You destroy the puzzle.")
                break
            elif msg.content == '2':
                await ctx.send("You try to solve the puzzle, but fail.")
            elif msg.content == '3':
                await ctx.send("You explore the room and find a hidden clue to the puzzle!")
            elif msg.content == '4':
                await ctx.invoke(bot.get_command('run'))
                break
            else:
                await ctx.send("Invalid choice. Please try again.")
        elif room.template == "empty":
            if msg.content == '1':
                await ctx.send("There is nothing to fight here.")
            elif msg.content == '2':
                await ctx.send("There is nothing to interact with here.")
            elif msg.content == '3':
                await ctx.send("You explore the room, but there's nothing to find.")
            elif msg.content == '4':
                await ctx.invoke(bot.get_command('run'))
                break
            else:
                await ctx.send("Invalid choice. Please try again.")

@bot.command(name='open')
async def open(ctx):
    print("open command called")
    room = Room()
    await open_door(ctx, room)


bot.run(botToken.botToken)