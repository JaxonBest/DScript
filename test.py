# Compiled with the DS Script Compiler.
# -----------------------------------

# Imports
import discord
# From Imports
from discord.ext import commands
class ping(commands.Bot):
    def __init__(self, client):
        self.client = client
    @commands.command(name="ping")
    async def ping(self, ctx ):
        ctx.send("Pong!")
def setup(client):
    client.add_cog(ping(client))