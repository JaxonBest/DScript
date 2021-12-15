# Compiled with the DS Script Compiler.
# -----------------------------------

# Imports
import discord

# From Imports
from discord.ext import commands



class untitled_command(commands.Bot):
    def __init__(self, client):
        self.client = client
    
    @commands.has_permissions(kick_members=True)
    @commands.command(name="untitled_command")
    async def untitled_command(self, ctx, target_user,kicking_reason_):
        
        
        
        
        
        
        
        
        await target_user.kick(reason="$reason")
        
        
        
        success_message='Succesfully kicked ' + target_user.mention
        
        
        
        
        ctx.send(success_message)
        
        executer = ctx.author
        executer.send(success_message)
        

def setup(client):
    client.add_cog(untitled_command(client))
