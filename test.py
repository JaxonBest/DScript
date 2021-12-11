# Compiled with the DS Script Compiler.
# -----------------------------------

# Imports
import discord

# From Imports
from discord.ext import commands

# Get and send a message to the channel.
# Hi Hi!
my_channel = discord.utils.get(ctx.guild.channels, id=int("1010101010"))
my_channel.send("'Hello'")
