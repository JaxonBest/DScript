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
        # Make sure the user has permission the kick members.
        
        # Create the arguments that will be intaked.
        
        #  ^^^^^^ ^^^^ <= will get translated to 'target_user'
        
        #  ^^^^^^^ ^^^^^^ <= will get translated to 'kicking_reason'
        # Kick the target user stored under the variable 'target_user'.
        await target_user.kick(reason="$reason")
        # Create a variable holding the success message.
        # You can write it directly inside of the send command. 
        # But for this sake I will create a variable.
        success_message='Succesfully kicked ' + target_user.mention
        #                                            ^ <= No '$' symbol because when creating variables
        #                                                 It's executed as pure Python. (For flexibility). 
        #                                                 Be careful because the compiler doesn't check pure Python..
        # Send the message to the channel.
        ctx.send(success_message)
        # Optionally you can also send a message to the user like this.
        executer = ctx.author
        executer.send(success_message)
        

def setup(client):
    client.add_cog(untitled_command(client))
