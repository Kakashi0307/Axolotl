import discord
from discord.ext import commands
import json
import os
import random
import asyncio
from discord.ext.commands.core import command

f = open("rules.txt","r")
rules = f.readlines()

client = commands.Bot(command_prefix=">")
client.remove_command("help")

if os.path.exists(os.getcwd() + "/config.json" ):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": "", "Prefix": ">"}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

#----------------------startup-------------------------
@client.event
async def on_ready(): #startup
    await client.change_presence(activity = discord.Game(name = f"on {len(client.guilds)} servers | >help"))
    print("Bot is ready")
    
@client.event
async def on_command_error(ctx,error): #missing permissions
    if isinstance(error,commands.MissingPermissions):
        em = discord.Embed(title = "Missing Permissions", description = "You don't have enough permissions to perform this action :sweat_smile:")
        await ctx.send(embed = em)
        await ctx.message.delete()
    elif isinstance(error,commands.MissingRequiredArgument): #missing arguments
        em = discord.Embed(title = "Missing Arguments", description = "Please enter all required arguments.Try **>help <command>** to know the syntax")
        await ctx.send(embed = em)
        await ctx.message.delete()
    else:
        raise error

#----------------------moderation-------------------------

@client.command(aliases=['c','clear','p',"Clear","Purge"])
@commands.has_permissions(manage_messages = True)
async def purge(ctx,*,amount=10): #purge
    amount += 1
    await ctx.channel.purge(limit = amount)

@client.command(aliases=['k','Kick','K'])
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason= "No Reason Provided"): #kick
    try:
        await member.send(" You were kicked from " + ctx.guild.name + " **|** " + reason)
    except:
        await ctx.send("The user has his/her dms closed,hence no dm notification was sent")
    
    await ctx.send(member.name + " kicked from the server **|** " + reason)
    await member.kick(reason=reason)

@client.command(aliases=['Ban','b','B'])
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason= "No Reason Provided"): #ban
    try:
        await member.send(" You were banned from " + ctx.guild.name + " **|** " + reason)
    except:
        await ctx.send("The user has his/her dms closed,hence no dm notification was sent")

    await ctx.send(member.name + " has been banned from the server because " + reason)
    await member.ban(reason=reason)

@client.command(aliases=['Unban','ub','Ub'])
@commands.has_permissions(ban_members = True)
async def unban(ctx,*,member): #unban
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split('#')

    for banned_entry in banned_users:
        user = banned_entry.user

        if (user.name, user.discriminator)==(member_name, member_disc):
            await ctx.guild.unban(user)
            await ctx.send(member_name + " has been unbanned")
        else :
            await ctx.send(member + " was not found")

@client.command(aliases=['m','Mute','M'])
@commands.has_permissions(manage_messages = True)
async def mute(ctx,member : discord.Member,*,reason = None): #mute
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")
        
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages = False, read_message_history = True, read_messages = True)
    
    await member.add_roles(mutedRole,reason=reason)
    await ctx.send(f"Muted {member.mention} for reason {reason}")

@client.command(aliases=['Um','Unmute','um'])
@commands.has_permissions(manage_messages = True)
async def unmute(ctx,member : discord.Member,*,reason = None): #Unmute

    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        await ctx.send("User has not been muted")
        return
    
    await member.remove_roles(mutedRole,reason=reason)
    await ctx.send("Unmuted")

#----------------------general-------------------------

@client.command(aliases=['userinfo','Whois','Userinfo'])
async def whois(ctx,member : discord.Member): #whois
    embed = discord.Embed(title = member.name , description = member.mention , color = discord.Colour.green())
    embed.add_field(name = "ID", value = member.id, inline = True)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed = embed)

@client.command(aliases = ['POLL','Poll'])
async def poll(ctx,*,message): #poll
        emb=discord.Embed(title = 'POLL', description = f"{message}")
        msg = await ctx.channel.send(embed =emb)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

@client.command(aliases=['rules','r'])
async def rule (ctx,*,number): #rules
    await ctx.send(rules[int(number)-1])

@client.command(aliases = ['av','Avatar','Av'])
async def avatar(ctx, *, member:discord.Member=None): #avatar
    if not member:
        member = ctx.message.author
    userAvatar = member.avatar_url

    embed = discord.Embed(colour=member.colour, timestamp=ctx.message.created_at)
    embed.set_author(name = f"Avatar of {member}")
    embed.set_image(url=member.avatar_url)
    embed.set_footer(text = f"Requwsted by {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)

@client.command(aliases=['Fortune'])
async def fortune(ctx, *, question):
    responses = [
        'Hell no',
        'Idk',
        'Probably',
        'Probably not',
        'It is certain.',
        'Without a Doubt.',
        'Yes - Definitaly.',
        'Uhh- Even I am not sure',
        'You may rely on it.',
        'As i see it, Yes.',
        'Most Likely.',
        'Yes!',
        'No!',
        'Signs a point to Yes!',
        'Reply Hazy, Try again.',
        'IDK but u should follow "Kakashi0307" on anilist and send "Kakashi | ℓινє fℓαмє🔥#1968" friend request on discord',
        'Better not tell you know.',
        'Cannot predict now.',
        'Concentrate and ask again.',
        'My reply is No.',
        'My sources say No.',
        'My sources say Yes.',
        'Very Doubtful'
        '~~Oh Yeah~~ Or maybe not']
    
    em = discord.Embed(title = "**Question**", description = f"**{question}**", colour = ctx.author.colour)
    em.add_field(name = "**Answer**", value = f"**{random.choice(responses)}**")
    em.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    
    await ctx.send(embed = em)


#----------------------giveaways-------------------------

@client.command(aliases = ['Gcreate','GCREATE']) #giveaways
async def gcreate(ctx, time = None, * , prize = None):
    if time == None:
        return await ctx.send('Please include TIME!')
    elif prize == None:
        return await ctx.send('Please include Prize!')
    embed = discord.Embed(title = 'New Giveaway!', description = f'{ctx.author.mention} is giving away **{prize}**')
    time_convert = {"s":1, "m":60, "h":3600, "d":86400}
    gawtime = (int)(time[0]) * time_convert[time[-1]]
    embed.set_footer(text = f'Giveaway ends in {time}')
    gaw_msg = await ctx.send(embed = embed)

    await gaw_msg.add_reaction("🎉")
    await asyncio.sleep(gawtime)

    new_gaw_msg = await ctx.channel.fetch_message(gaw_msg.id)

    users = await new_gaw_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await ctx.send(f"Yey!! {winner.mention} has won {prize} gg :)")

@client.command
async def greroll(ctx,* , msg):
    new_gaw_msg = await ctx.channel.fetch_message(gaw_msg.id)

    users = await new_gaw_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await ctx.send(f"Yey!! {winner.mention} is the new WINNER gg :)")

#----------------------help-------------------------

@client.group(invoke_without_command = True)
async def help(ctx): #help main
    em = discord.Embed(title = "Help", description = f"Use **>help <category>** to know more about commands in that category and type **>help <command>** to know more about that command. Note that **round parentheisis ()** shows that the argument is mandatory while **square parentheisis []** shows that the argument is optional**", colour = ctx.author.colour)
    
    em.add_field (name="**Moderation**", value = "** **")
    em.add_field (name = "General", value = "** **")
    em.add_field (name= "Giveaways", value = "** **")

    await ctx.send(embed=em)

@help.command()
async def moderation(ctx): #help moderation
    em = discord.Embed(title = "Category - **MODERATION**", description = "use **>help <command>** to know more about that command.", colour = ctx.author.colour)
    em.add_field (name = "**Commands**", value = "```mute```, ```unmute```, ```kick```, ```ban```, ```unban```, ```purge```")
    await ctx.send(embed = em)

@help.command()
async def general(ctx): #help uncategorised
    em = discord.Embed(title = "Category - **GENERAL**", description = "use **>help <command>** to know more about that command.", colour = ctx.author.colour)
    em.add_field (name = "**Commands**", value = "```rules```, ```avatar```, ```whois```, ```poll```")
    await ctx.send(embed = em)

@help.command()
async def giveaways(ctx): #help giveaways
    em = discord.Embed(title = "Category - **GIVEAWAY**", description = "use **>help <command>** to know more about that command.", colour = ctx.author.colour)
    em.add_field (name = "**Commands**", value = "```gcreate```, ```greroll```")
    await ctx.send(embed = em)

@help.command()
async def kick(ctx): #help kick
    em = discord.Embed(title = "**Kick**", description = "Kick a member from the server (one can join back if he/she has invite)", colour = ctx.author.colour)
    em.add_field (name = "**Syntax**", value = "kick (member) [reason]")
    em.add_field (name = "**Alternatives**", value = "k")

    await ctx.send(embed = em)

@help.command()
async def ban(ctx): #help ban
    em = discord.Embed(title = "**Ban**", description = "Ban a member from the server once banned one cannot join back until he/she is unbanned", colour = ctx.author.colour)
    em.add_field (name = "**Syntax**", value = "Ban (member) [reason]")
    em.add_field (name = "**Alternatives**", value = "B")

    await ctx.send(embed = em)

@help.command()
async def mute(ctx): #help mute
    em = discord.Embed(title = "**Mute**", description = "Once muted member cannot type in any channel", colour = ctx.author.colour)
    em.add_field (name = "**Syntax**", value = "mute (member) [reason]")
    em.add_field (name = "**Alternatives**", value = "m")

    await ctx.send(embed = em)

@help.command()
async def unmute(ctx): #help unmute
    em = discord.Embed(title = "**Unmute**", description = "Unmutes a muted member", colour = ctx.author.colour)
    em.add_field (name = "**Syntax**", value = "unmute (member) [reason]")
    em.add_field (name = "**Alternatives**", value = "um")

    await ctx.send(embed = em)

@help.command()
async def unban(ctx): #help unban
    em = discord.Embed(title = "**Unban**", description = "Unbans a banned member", colour = ctx.author.colour)
    em.add_field (name = "**Syntax**", value = "unban member(#4-digit code)")
    em.add_field (name = "**Alternatives**", value = "ub")

    await ctx.send(embed = em)

@help.command()
async def purge(ctx): #help purge
    em = discord.Embed(title = "**Purge**", description = "Deletes a certain number of messages. If no value is entered last **10 messages** are deleted", colour = ctx.author.colour)
    em.add_field (name = "**Syntax**", value = "purge (number of messages to be purged]")
    em.add_field (name = "**Alternatives**", value = "p,c,clear")

    await ctx.send(embed = em)

@help.command()
async def avatar(ctx): #help avatar
    em = discord.Embed(title = "**Avatar**", description = "Shows avatar of the mentioned member If noone is mentioned avatar of the one who sent message is shown", colour = ctx.author.colour)
    em.add_field (name = "**Syntax**", value = "avatar [mention user]")
    em.add_field (name = "**Alternatives**", value = "av")

    await ctx.send(embed = em)

@help.command()
async def userinfo(ctx): #help whois
    em = discord.Embed(title = "**userinfo**", description = "Gives info about a user", colour = ctx.author.colour)
    em.add_field (name = "**Syntax**", value = "userinfo (mention the user)")
    em.add_field (name = "**Alternatives**", value = "whois")

    await ctx.send(embed = em)

@help.command()
async def poll(ctx): #help poll
    em = discord.Embed(title = "**Poll**", description = "Creates a poll", colour = ctx.author.colour)
    em.add_field (name = "**Syntax**", value = "poll (question)")
    em.add_field (name = "**Alternatives**", value = "No alternatives")

    await ctx.send(embed = em)

token = configData["Token"]
prefix = configData["Prefix"]
client.run(token)