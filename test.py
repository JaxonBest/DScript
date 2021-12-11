# Compiled with the DS Script Compiler.

import discord
from discord.ext import commands

welcome = None
variable_name_storing_author = ctx.author
welcome = f"Hello, {variable_name_storing_author}"
if "Hello," in welcome:
    print("Hey!")
ctx.send(welcome) # Sending a message to the same channel the message was sent in.
