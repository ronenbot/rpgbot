# This example requires the 'members' privileged intents
import random
import itertools
import sqlite3
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
async def poop(ctx, times: int, content="poopping..."):
    """Repeats a message multiple times."""
    for _ in range(times):
        await ctx.send(content)


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


bot.run(botToken.botToken)