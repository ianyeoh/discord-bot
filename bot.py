import os
import discord
import asyncio
from discord.ext import commands 
from dotenv import load_dotenv

# Initialise bot and Discord intents gateways
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    await bot.process_commands(message)

### BOT COMMANDS

@bot.command()
# If a "purge-immune" role is configured in the server the command is called, kicks all
# members in the server WITHOUT the role.
async def purge(ctx):
    # Find purge immune role
    purge_immune = None
    for role in ctx.guild.roles:
        if role.name == "purge immune":
            purge_immune = role

    # If role not present
    if purge_immune == None:
        await ctx.channel.send(f"No \"purge immune\" role configured.")
        return

    # Create a list of members who do not have the purge immune role, and are not the bot
    # or the command caller.
    kicked_members = []
    for member in ctx.guild.members:
        if purge_immune not in member.roles and member != ctx.author and member != bot.user:
            kicked_members.append(member)

    # Kick all members in list
    if len(kicked_members) == 0:
        await ctx.channel.send("No members purged.")
    else:
        await ctx.channel.send(f"Executing Order 66. Purged: ")
        for member in kicked_members:
            await member.kick(reason="Purged. See you next time!")
            await ctx.channel.send(f"{member}")

@bot.command()
# Runs an asyncio thread to kick the calling user after the given amount of 
# time from the voice channel they are in, if applicable
async def kickmeafter(ctx, time, units):
    units = str(units)
    time = float(time)
    
    if time <= 0 or (units != "secs" and units != "hrs" and units != "mins"):
        await ctx.channel.send("Usage: $kickmeafter [time] [units: secs/mins/hrs]")
        return
        
    if units == "hrs":
        time = time * 60 * 60
    
    if units == "mins":
        time = time * 60
    
    await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
    await asyncio.sleep(time)
    await ctx.message.author.move_to(None)

@kickmeafter.error
async def kickmeafter_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("Usage: $kickmeafter [time] [units: secs/mins/hrs]")

@bot.command()
# Test command to check bot is listening
async def test(ctx):
    await ctx.channel.send("Hello!")

# Run bot
load_dotenv()
bot.run(os.getenv("TOKEN"))
