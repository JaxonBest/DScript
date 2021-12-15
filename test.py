# Compiled with the DS Script Compiler.
# -----------------------------------

# Imports
import discord
# From Imports
from discord.ext import commands
class untitled_command(commands.Bot):
    def __init__(self, client):
        self.client = client
    @commands.has_permissions(ban_members=True)
    @commands.command(name="untitled_command")
    async def untitled_command(self, ctx, target,reason):
        await target.ban(reason=str(reason))
        ban_success_message="{} was successfully banned!".format(target.discriminator)
        ctx.send(ban_success_message)
def setup(client):
    client.add_cog(untitled_command(client))