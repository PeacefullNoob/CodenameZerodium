import discord
import subprocess
import random
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
from datetime import datetime
import sys
from addict import Dict
import json
import asyncio

load_dotenv()
intents = discord.Intents.default()
intents = discord.Intents(messages=True, guilds=True)
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$')
globalFilterOverride = False
f = open("filterwords.json")
r = open("riley.json")
chatFilter = Dict(json.load(f))
rileyweird = Dict(json.load(r))
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Pinewood Computer Core'))
    print('Successfully logged in as {0.user}.'.format(client))
    globalFilterOverride = False

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global globalFilterOverride
    
    if message.author.id != "852614202014302219" or message.author.id != "830607392802078791" or message.author.guild_permissions.administrator == False and globalFilterOverride == False:
        for key in chatFilter['bannedWords']:
            text = message.content.lower()
            if key in text.split():
                await message.delete()
                channel = client.get_channel(858495313740300318) #Updated for sex discord
                embed = discord.Embed(
                    title="Global Filter",
                    description="Banned word triggered by `Wildcard`",
                    colour=discord.Colour.from_rgb(255, 0, 242)
                )
                embed.add_field(name="Banned Word", value=key)
                embed.add_field(name="Full Message", value=message.content, inline=False)
                embed.set_author(name=message.author.name+'#'+message.author.discriminator, icon_url=message.author.avatar_url)

                await channel.send(embed=embed)
                return
        if message.author.id == "566118564717658114":
            for key in chatFilter['rileyweirdwords']:
                text = message.content.lower()
                if key in text.split():
                    await message.delete()
                    channel = client.get_channel(858495313740300318)
                    embed = discord.Embed(
                        title="Riley Filter",
                        description="Filtered word from Riley",
                        colour=discord.Colour.from_rgb(255, 0, 242)
                    )
                    embed.add_field(name="Filtered Word", value=key)
                    embed.add_field(name="Full Message", value=message.content, inline=False)
                    embed.set_author(name=message.author.name+'#'+message.author.discriminator, icon_url=message.author.avatar_url)
                    await channel.send(embed=embed)
    for x in message.mentions:
        if(x==client.user):
            embed = discord.Embed(
                title="CodenameZerodium#6429",
                description="""Moderation bot developed and maintained by <@852614202014302219> and <@830607392802078791>
                
Currently running **v1.4.1*            
                """
                
            )
            embed.set_footer(text="Message will delete after 20 seconds") # 852614202014302219 = femou, 830607392802078791 = CodenamePhoton
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/906552943103311934/deaece333de290f421adea71041f0535.png?size=2048")
            await message.channel.send(embed=embed, delete_after=20)

    if message.content.startswith('$info'):
        embed = discord.Embed(
            title="CodenameZerodium#6429",
            description="""Moderation bot developed and maintained by <@852614202014302219> and <@830607392802078791>
                
Currently running **v1.4.1**            
            """
                
            )
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/906552943103311934/deaece333de290f421adea71041f0535.png?size=2048")
        await message.channel.send(embed=embed)

    
    if message.content.startswith('$rileybanword'): ##fucking riley
        text = message.content.replace("$rileybanword ", "", 1)
        if message.author.id == "852614202014302219" or message.author.id == "830607392802078791" or message.author.id == "599040744334032912":
            if text == "$rileybanword":
                await message.channel.send("Error.")
                return
            foxtrot = open("riley.json", "r")
            filterList = Dict(json.load(foxtrot))
            filterList['rileyweirdwords'].setdefault(text,)
            chatFilter['rileyweirdwords'].setdefault(text,)
            foxtrot.close()
            jsonFile = open("riley.json", "w+")
            json.dump(filterList, jsonFile, indent=4,)
            jsonFile.close()
            await message.channel.send(str(text)+" has been added to Riley's filter.")
        else:
            embed = discord.Embed(
                description="User <@"+str(message.user.id)+"> tried adding to the Riley filter.",
                colour=discord.Colour.red()
            )
            channel = client.get_channel(906564812048314438)
            await channel.send(embed=embed)


    if message.content.startswith('$banword'):
        text = message.content.replace("$banword ", "", 1)
        if message.author.guild_permissions.administrator == True:
            if text == "$banword":
                await message.channel.send("Error.")
                return 
            foxtrot = open("filterwords.json", "r")
            filterList = Dict(json.load(foxtrot))
            filterList['bannedWords'].setdefault(text,)
            chatFilter['bannedWords'].setdefault(text,)
            foxtrot.close()
            jsonFile = open("filterwords.json", "w+")
            json.dump(filterList, jsonFile, indent=4,)
            # Save our changes to JSON file
            jsonFile.close()
            await message.channel.send(str(text)+" has been added to globalfilter.")
    if message.content.startswith('$unbanword'):
        text = message.content.replace("$unbanword ", "", 1)
        if message.author.guild_permissions.administrator == True:
            if text == "$unbanword":
                await message.channel.send("Error.")
                return 
            foxtrot = open("filterwords.json", "r")
            filterList = Dict(json.load(foxtrot))
            foxtrot.close()
            if text in filterList['bannedWords']:
                filterList['bannedWords'].pop(text)
                chatFilter['bannedWords'].pop(text)
                jsonFile = open("filterwords.json", "w+")
                json.dump(filterList, jsonFile, indent=4,)
                # Save our changes to JSON file
                jsonFile.close()
                await message.channel.send(str(text)+" has been removed from the globalfilter")
            else:
                await message.channel.send(str(text)+" was already unfiltered!") 

    if message.content.startswith('$globalfilterstateget'):
        if message.author.guild_permissions.administrator == True:
            await message.channel.send("Global filter override: " + str(globalFilterOverride))
    if message.content.startswith('$globalfilterstatetoggle'):
        if message.author.guild_permissions.administrator == True:
            if  globalFilterOverride == True:
                globalFilterOverride = False
                await message.channel.send("Global Filter Enabled")
            elif globalFilterOverride == False:
                globalFilterOverride = True
                await message.channel.send("Global Filter Disabled")
        
    if message.content.startswith('$mute '):
        if message.author.guild_permissions.administrator == True:
            text = message.content
            text = text.replace("$mute ", "", 1)
            role = discord.utils.get(message.guild.roles, name="Muted")
            user = await message.guild.fetch_member(int(text))
            for x in user.roles:
                if x == role:
                    embed = discord.Embed(
                        description="User "+user.name+"#"+user.discriminator+" is already muted."
                    )
                    await message.channel.send(embed=embed)
                    return
        
            await user.add_roles(role)
            embed = discord.Embed(
                description="Muted "+user.name+"#"+user.discriminator+"."
            )
            await message.channel.send(embed=embed)
    if message.content.startswith('$tempmute '):
        if message.author.guild_permissions.administrator == True:
            text = message.content
            text = text.replace("$tempmute ", "", 1)
            text = text.split()
            userid = text[0]
            muteTime = int(text[1])
            role = discord.utils.get(message.guild.roles, name="Muted")
            user = await message.guild.fetch_member(int(userid))
            embed = discord.Embed(
                    title="Temp Mute",
                    description="""Usage:
$tempmute <userID> <Minutes>
                    """,
                    colour=discord.Colour.red()
                )
            if text[1] is None:
                await message.channel.send(embed=embed)
            for x in user.roles:
                if x == role:
                    embed = discord.Embed(
                        description="User "+user.name+"#"+user.discriminator+" is already muted."
                    )
                    await message.channel.send(embed=embed)
                    return
        
            await user.add_roles(role)
            embed = discord.Embed(
                description="Muted "+user.name+"#"+user.discriminator+" for: "+str(muteTime)+" minutes."
            )
            await message.channel.send(embed=embed)
            channel = client.get_channel(858410240541851668)
            await channel.send(embed=embed)
            await asyncio.sleep(muteTime*60)
            await user.remove_roles(role)
            embed = discord.Embed(
                description="Unmuted "+user.name+"#"+user.discriminator+"."
            )
            await channel.send(embed=embed)

    if message.content.startswith('$unmute '):
        if message.author.guild_permissions.manage_messages == True:
            text = message.content
            text = text.replace("$unmute ", "", 1)
            role = discord.utils.get(message.guild.roles, name="Muted")
            user = await message.guild.fetch_member(int(text))
            for x in user.roles:
                if x == role:
                    await user.remove_roles(role)
                    embed = discord.Embed(
                        description="Unmuted "+user.name+"#"+user.discriminator
                    )
                    await message.channel.send(embed=embed)
                    return

            embed = discord.Embed(
                description="User "+user.name+"#"+user.discriminator+" != muted."
            )
            await message.channel.send(embed=embed)

    if message.content.startswith('$restart'):
        if message.author.id == 852614202014302219 or 830607392802078791:
            print("argv was",sys.argv)
            print("sys.executable was", sys.executable)
            print("restart now")
            await message.channel.send("**Shutting down and Restarting. See you later!**")
            os.execv(sys.executable, ['python3.8'] + sys.argv)
            await message.channel.send("There was an error restarting")
        else: 
            await message.channel.send("Invalid permissions.")
            embed = discord.Embed(
                description="User <@"+message.author.id+"> tried using $restart in <#"+message.channel.id+">"
            )
            channel = client.get_channel(906564812048314438)
            await channel.send(embed=embed)

    if message.content.startswith('$ping'):
        frameworklat = str(client.latency*1000)
        await message.channel.send("Ping:" + ' ' + frameworklat + ' ' + 'ms')

    if message.content.startswith('$say'):
        text = message.content
        text = text.replace("$say ", "", 1)
        await message.delete()
        await message.channel.send(text)
        embed = discord.Embed(
            description=message.content+"""
            
            """+"<@"+message.author.id+">"
        )
        client.get_channel('906564812048314438')
        await channel.send(embed=embed)
    if message.content.startswith('$purge'):
        if message.author.guild_permissions.administrator == True:
            text = message.content
            text = text.replace("$purge ", "", 1)
            await message.delete()
            await message.channel.purge(limit=int(text))
            embed = discord.Embed(
                title="Purge",
                description=text+" Messages deleted in <#"+str(message.channel.id)+">"
            )
            embed.set_author(name=message.author.name+"#"+message.author.discriminator, icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed)

    if message.content.startswith('$offsay'):
        if message.author.guild_permissions.administrator == True:
            text = message.content
            text = text.replace("$offsay ", "", 1)
            await message.delete()
            embed = discord.Embed(
                description=str(message.content)+"""
                
                """+"<@"+str(message.author.id)+">"
            )
            channel = client.get_channel(858406792468234244)
            await channel.send(text)
            channel = client.get_channel(906564812048314438)
            await channel.send(embed=embed)

    if message.content.startswith('$cmd'):
        if message.author.id == 852614202014302219 or 830607392802078791:
            #target = client.get_channel(906564812048314438)
            text = message.content
            target = await message.channel.send("Processing <a:loading:796555559004012544>")
            text = text.replace("$cmd ", "", 1)
            try:
                result = subprocess.check_output(text, shell=True)
            except:
                await target.edit(content="Process Failiure")
                return
            result = result.decode("utf-8")
            string_length = len(result)
            if string_length > 1998:                
                chunklength = 1998
                chunks = [result[i:i+chunklength ] for i in range(0, len(result), chunklength )]
                starter = 1
                for chunk in chunks:
                    if starter == 1:
                        await target.edit(content="```"+chunk+"```")
                        starter = 2
                    else:
                        await message.channel.send("```"+chunk+"```")
            else:

                await target.edit(content="```"+result+"```")
        else:
            embed = discord.Embed(
                title="Invalid Permissions!",
                description="Only the Bot Owners may use the Serverside Executor.",
                colour=discord.Colour.red()
            )
            await message.channel.send(embed=embed)
            embed = discord.Embed(
                description=str(message.content)
            )
            embed.set_footer("User <@"+str(message.user.id)+"> tried using $cmd")
            channel = client.get_channel('906564812048314438')
            await channel.send(embed=embed)


    if message.content.startswith('$message'):
        #target = client.get_channel(906564812048314438)
        text = message.content
        text = text.lstrip("$message")
        #await message.channel.send(text)
        if text == '':
            embed = discord.Embed(
            title="**Usage Instructions**",
            colour=discord.Colour.orange(),
            description="$message <message> \n Ex: $message hello world",
            )
            await message.delete()
            await message.channel.send(embed=embed)
        else:
            await message.delete()
            if message.author.nick is None:
                usersName = message.author.name
            else:
                usersName = message.author.nick
            embed = discord.Embed(
            title="**Message from" + ' ' + usersName +"**",
            colour=discord.Colour.blue(),
            description=text,

            )
            await message.channel.send(embed=embed)
            #await target.send(message.content)
    
        #file1.close() 
    if message.content.startswith('$help'):
        if message.author.guild_permissions.administrator == True:
            embed = discord.Embed(
                title="Help Info",
                description="""
Commands:

$help - Displays this message
$ping - View bot latency
$info - Shows bot information

**HR Commands**

$mute <User ***ID***> - User IDs not Usernames or mentions.
$tempmute <User ***ID***> <Minutes> - User IDs not Usernames or mentions.
$purge <# of messages> - Purges messages in the current channel.
$globalfilterstateget - Returns the state of the GlobalFilter *Override*
$globalfilter
$banword - Adds words to the ban list
$unbanword - Unban words from the ban list

**Owner/User specifc commands**

$[REDACTED] - Adds to the [REDACTED] filter
$[REDACTED] - Removes from the [REDACTED] filter (Does not work, manually remove it from the file if needed or make a request to <@852614202014302219> or <@830607392802078791>)
                """,
                colour=discord.Colour.from_rgb(104, 204, 237)

            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/906552943103311934/deaece333de290f421adea71041f0535.png?size=2048")
            embed.set_author(name="CodenameZerodium#6429",icon_url="https://cdn.discordapp.com/avatars/906552943103311934/deaece333de290f421adea71041f0535.png?size=2048")
            await message.channel.send(embed=embed)

        if message.author.guild_permissions.administrator == False:
            embed = discord.Embed(
                title="Help Info",
                description="""
Commands:

$help - Displays this message
$ping - View bot latency
$info - Shows bot information
                """,
                colour=discord.Colour.from_rgb(104, 204, 237)

            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/906552943103311934/deaece333de290f421adea71041f0535.png?size=2048")
            embed.set_author(name="CodenameZerodium#6429",icon_url="https://cdn.discordapp.com/avatars/906552943103311934/deaece333de290f421adea71041f0535.png?size=2048")
            await message.channel.send(embed=embed)




client.run(os.getenv("BOT_TOKEN"))

@bot.command(name="aaaa")
async def aaaa(ctx, arg):
    await ctx.send(arg)


