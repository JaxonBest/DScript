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
    async def untitled_command(self, ctx ):
        hello="Hello, World -> "
        print(""+str(hello)+" true")
def setup(client):
    client.add_cog(untitled_command(client))