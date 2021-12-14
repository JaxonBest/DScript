# Compiled with the DS Script Compiler.
# -----------------------------------

# Imports
import discord

# From Imports
from discord.ext import commands
from datetime import datetime


class untitled_command(commands.Bot):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="untitled_command")
    async def untitled_command(self, ctx ):
        # Importing the modules we need.
        
        current_time=datetime.now()
        current_time = "The current time is " + current_time; 
        ctx.send(current_time)
        

def setup(client):
    client.add_cog(untitled_command(client))
