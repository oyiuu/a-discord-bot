import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
import config

bot = commands.Bot(
    command_prefix="?",
    help_command=None)

@bot.event
async def on_ready():
    print("I'm ready!")
    status = discord.Game("Prefix: ?")
    await bot.change_presence(activity=status)

"""@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")"""

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Prefix: ,", description="A list of all available commands", color=discord.Color.purple)
    member = ctx.message.author
    embed.set_author(name="Help", icon_url="{}".format(member.avatar_url))
    embed.add_field(name="Prune (num)", inline=False)
    embed.add_field(name="Kick", inline=False)
    embed.add_field(name="Ban", inline=False)
    embed.add_field(name="Avatar (id/ping)", inline=False)
    embed.add_field(name="Info", inline=False)
    embed.set_footer(text="More commands to come.")
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx, member: discord.Member):
    embed=discord.Embed(color=discord.Color.purple())
    if not member:
        member = ctx.message.author
    embed.set_author(name=f"{member}", icon_url=member.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="ID", value=f"{member.id}")
    embed.add_field(name="Nickname", value=f"{member.nick}", inline=True)
    embed.add_field(name="Account Created", value=f"{member.created_at:%A, %B %dth %Y @ %H:%M:%S %p}", inline=False)
    embed.add_field(name="Join Date", value=f"{member.joined_at:%A, %B %dth %Y @ %H:%M:%S %p}", inline=False)
    not_everyone = lambda r: r.position != 0
    if roles := [r.mention for r in filter(not_everyone, member.roles)]:
        embed.add_field(name="Roles", value=" | ".join(reversed(roles)), inline=False)
    await ctx.send(embed=embed)

@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member):
    await ctx.send(f"{member} was kicked!")
    await member.kick()
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, CheckFailure):
        await ctx.send("You aren't powerful enough.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Target is not here.")
    else:
        await ctx.send("Invalid ID/tag")

@bot.command()
@has_permissions(ban_members=True)  
async def ban(ctx, member:discord.Member): 
    await ctx.send(f'{member} was banned!')
    await member.ban()
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, CheckFailure):
        await ctx.send("You aren't powerful enough.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Target is not here.")
    else:
        await ctx.send("Invalid ID/tag")

@bot.command()
async def avatar(ctx, member: discord.Member):
    if not member:
        member = ctx.message.author
    show_avatar = discord.Embed(title=" ", color=discord.Color.purple())
    show_avatar.set_image(url=member.avatar_url)
    show_avatar.set_author(name=f"{member}")
    await ctx.send(embed=show_avatar)

@bot.command()
@has_permissions(manage_messages=True)
async def prune(ctx, amount : int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"Deleted {amount} message(s)!", delete_after=5)
@prune.error
async def prune_error(ctx, error):
    if isinstance(error, CheckFailure):
        await ctx.send("You aren't powerful enough.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify an amount.")

    
@bot.event
async def on_message(message):         
    if message.author == bot.user: 
        return 
    message_lower = message.content.lower()    
    if message_lower == "hello":   
        await message.channel.send("Hi!")

    await bot.process_commands(message)  #on_message blocks commands

bot.run(config.TOKEN) 
