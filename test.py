# Compiled with the DS Script Compiler.
# -----------------------------------

# Imports
import discord

# From Imports
from discord.ext import commands


class untitled_command(commands.Bot):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="untitled_command")
    async def untitled_command(ctx,  one,two,three):
		# -> My first command.
		
		
		
		ctx.send(one) # Sending a message to the same channel the message was sent in.
		ctx.send(two) # Sending a message to the same channel the message was sent in.
		ctx.send(three) # Sending a message to the same channel the message was sent in.
        

def setup(client):
    client.add_cog(untitled_command(client))
