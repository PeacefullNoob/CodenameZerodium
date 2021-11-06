import discord
import subprocess
import requests
import random
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
from datetime import datetime
import sys
from addict import Dict
import json
from profanity import profanity
# import sqlalchemy
import asyncio

load_dotenv()
#client = discord.AutoShardedClient(shard_count=10)
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$')
globalFilterOverride = False
f = open("filterwords.json")
chatFilter = Dict(json.load(f))
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
    if message.author.guild_permissions.manage_messages == False and globalFilterOverride == False:
        role = discord.utils.get(message.guild.roles, name = "On Watch")
        if role in message.author.roles: 
            if "http" in message.content.lower():
                await message.delete()
                channel = client.get_channel(858495313740300318)  #Updated for sex discord
                embed = discord.Embed(
                    title="Global Filter",
                    description="Banned word triggered by `On-Watch link remover`",
                    colour=discord.Colour.from_rgb(255, 0, 242)
                )
                embed.add_field(name="Trigger", value="Link Posted")
                embed.add_field(name="Full Message", value=message.content, inline=False)
                embed.set_author(name=message.author.name+'#'+message.author.discriminator, icon_url=message.author.avatar_url)

                await channel.send(embed=embed)
            await channel.send(embed=embed)
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
                #print(mydict[key])
                return
    for x in message.mentions:
        if(x==client.user):
            await message.delete()
            embed = discord.Embed(
                title="CodenameZerodium#9466",
                description="""Moderation bot developed and maintained by <@852614202014302219> and <@830607392802078791>
                
Currently running **v1.0.0**            
                """
                
            )
            embed.set_footer(text="Message will delete after 20 seconds") # 852614202014302219 = femou, 830607392802078791 = CodenamePhoton
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/752993473350860920/4ecaf6fa0d715727e5e65deff5748759.png")
            await message.channel.send(embed=embed, delete_after=20)
    if message.content.startswith('$banword'):
        text = message.content.replace("$banword ", "", 1)
        if message.author.guild_permissions.administrator == True:
            foxtrot = open("filterwords.json", "r")
            filterList = Dict(json.load(foxtrot))
            filterList['bannedWords'].setdefault(text,)
            chatFilter['bannedWords'].setdefault(text,)
            foxtrot.close()
            jsonFile = open("filterwords.json", "w+")
            json.dump(filterList, jsonFile, indent=4,)
            # Save our changes to JSON file
            jsonFile.close()
            await message.channel.send(str(text)+" has been added to globalfilter")
    if message.content.startswith('$unbanword'):
        text = message.content.replace("$unbanword ", "", 1)
        if message.author.guild_permissions.administrator == True:
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
            await message.delete()
            await message.channel.send("Global filter override: " + str(globalFilterOverride), delete_after=5)
    if message.content.startswith('$globalfilterstatetoggle'):
        if message.author.guild_permissions.administrator == True:
            if  globalFilterOverride == True:
                globalFilterOverride = False
                await message.channel.send("Global Filter Enabled")
            elif globalFilterOverride == False:
                globalFilterOverride = True
                await message.channel.send("Global Filter Disabled")
    if message.content.startswith('$getuserid'):
         for x in message.mentions:
             await message.channel.send("ID FOR: "+x.name+"#"+x.discriminator+" is "+str(x.id))
        
    if message.content.startswith('$mute '):
        if message.author.guild_permissions.administrator == True:
            text = message.content
            text = text.replace("$mute ", "", 1)
            role = discord.utils.get(message.guild.roles, name="Muted")
            user = await message.guild.fetch_member(int(text))
            for x in user.roles:
                if x == role:
                    embed = discord.Embed(
                        description="I can't mute "+user.name+"#"+user.discriminator+", they are already muted"
                    )
                    await message.channel.send(embed=embed)
                    return
        
            await user.add_roles(role)
            embed = discord.Embed(
                description="Muted "+user.name+"#"+user.discriminator
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
                        description="I can't mute "+user.name+"#"+user.discriminator+", they are already muted"
                    )
                    await message.channel.send(embed=embed)
                    return
        
            await user.add_roles(role)
            embed = discord.Embed(
                description="Muted "+user.name+"#"+user.discriminator+" for: "+str(muteTime)+" minutes."
            )
            await message.channel.send(embed=embed)
            channel = client.get_channel(758729070111490109)
            await channel.send(embed=embed)
            await asyncio.sleep(muteTime*60)
            await user.remove_roles(role)
            embed = discord.Embed(
                description="Unmuted "+user.name+"#"+user.discriminator
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
                description="I can't unmute "+user.name+"#"+user.discriminator+", they are already unmuted"
            )
            await message.channel.send(embed=embed)
    
    if message.content.startswith('$ignore'):
        if message.author.id == 852614202014302219:
            text = message.content
            text = text.replace("$ignore ", "", 1)
            data =  {'API_KEY':apiKey,
            'USERID': str(text),
            'REQ_TYPE':"ADD"
            }
            r = requests.post(apiURL+"/user/ignore", json=data)
            if r.status_code == 569:
                await message.channel.send("User already Ignored!")
            elif r.status_code == 200:
                await message.channel.send("User with ID of: "+text+" Ignored!")
                
    if message.content.startswith('$unignore'):
        if message.author.id == 852614202014302219:
            text = message.content
            text = text.replace("$unignore ", "", 1)
            data =  {'API_KEY':apiKey,
            'USERID': str(text),
            'REQ_TYPE':"REMOVE"
            }
            r = requests.post(apiURL+"/user/ignore", json=data)
            if r.status_code == 569:
                await message.channel.send("User was already not ignored!")
            elif r.status_code == 200:
                await message.channel.send("User with ID of: "+text+" No longer ignored!")
    if message.content.startswith('$restart'):
        if message.author.id == 852614202014302219:
            print("argv was",sys.argv)
            print("sys.executable was", sys.executable)
            print("restart now")
            await message.delete()
            await message.channel.send("**Shutting down and Restarting. See you later!**")
            os.execv(sys.executable, ['python3.8'] + sys.argv)
            await message.channel.send("There was an error restarting")

    if message.content.startswith('$ping'):
        elapsed_time = 0
        msgtime = message.created_at
        now = datetime.now()
        #now - msgtime datetime.timedelta(0, 3, 519319)
        diff = now - msgtime
        elapsed_time = (diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000)
        elapsed_time = str(elapsed_time)
        frameworklat = str(client.latency*1000)
        await message.channel.send("Serverside:" + ' ' + elapsed_time + ' ' + "milliseconds \nFramework:" + ' ' + frameworklat + ' ' + 'ms')

    if message.content.startswith('$say'):
        #target = client.get_channel(658251987959152641)
        text = message.content
        text = text.replace("$say ", "", 1)
        await message.delete()
        await message.channel.send(text)
        #await target.send(message.content)
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
            channel = client.get_channel(779398704847126528)
            await channel.send(embed=embed)

    if message.content.startswith('$gensay'):
        if message.author.guild_permissions.administrator == True:
            #target = client.get_channel(658251987959152641)
            text = message.content
            text = text.replace("$gensay ", "", 1)
            await message.delete()
            channel = client.get_channel(739975346513903750)
            await channel.send(text)
    
    if message.content.startswith('$offsay'):
        if message.author.guild_permissions.administrator == True:
            #target = client.get_channel(658251987959152641)
            text = message.content
            text = text.replace("$offsay ", "", 1)
            await message.delete()
            channel = client.get_channel(736432247842013234)
            await channel.send(text)
    if message.content.startswith('$massrepeat'):
        if message.author.id == 852614202014302219:
            #target = client.get_channel(658251987959152641)
            text = message.content
            text = text.replace("$massrepeat ", "", 1)
            await message.delete()
            iterateor = 0
            while iterateor < 11:
                await message.channel.send(text)
                iterateor = iterateor+1
    
    if message.content.startswith('$cmd'):
        if message.author.id == 852614202014302219:
            #target = client.get_channel(658251987959152641)
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
                description="Only the **Bot Owner** may use the Serverside Executor!",
                colour=discord.Colour.red()
            )
            await message.channel.send(embed=embed)


    if message.content.startswith('$message'):
        #target = client.get_channel(658251987959152641)
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

    if message.content.startswith('$kos'):
        #target = client.get_channel(658251987959152641)
        if message.author.guild_permissions.administrator == True:
            text = message.content
            text = text.lstrip("$kos")
            #await message.channel.send(text)
            if text == '':
                embed = discord.Embed(
                title="**Usage Instructions**",
                colour=discord.Colour.orange(),
                description="$kos <username>",
                )
                await message.delete()
                await message.channel.send(embed=embed)
            else:
                await message.delete()
                channel = client.get_channel(741142717463134260)
                await channel.send(text+' '+"is now on NIA KoS!")
            #await target.send(message.content)
        else:
            embed = discord.Embed(
            title="**Invalid Permissions!**",
            colour=discord.Colour.orange(),
            description="You are not allowed to run that command!",
            )
            await message.channel.send(embed=embed)
    if message.content.startswith('$getchannel'):
        if message.author.id == 852614202014302219:
            await message.delete()
            await message.channel.send(message.channel.id, delete_after=1)
    if message.content.startswith('$mypoints') and  (message.author.guild_permissions.administrator == True or  message.channel.id == 736446384252780555):
        #target = client.get_channel(658251987959152641)
        print(apiKey)
        data =  {'API_KEY':apiKey,
        'USERNAME': message.author.nick,
        'req_type':"Singular"
        }
        #headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(apiURL+"/user/viewpoints", json=data)
        print(r.text)
        embed = discord.Embed(
                title="**Points for"+' '+message.author.nick+"**",
                colour=discord.Colour.orange(),
                description=r.text,
                )
        status = r.status_code
        print(status)
        if status == 200:
            await message.channel.send(embed=embed)
        elif status == 569:
            await message.channel.send("User Not Found!")
        else:
            await message.channel.send("An Unknown Error has Occured. Check bot and API logs.")
    
    if message.content.startswith('$viewpoints'):
        if message.author.guild_permissions.administrator == True:
            #target = client.get_channel(658251987959152641)
            text = message.content
            text = text.replace("$viewpoints ", "", 1)
            if text == "||batchlist":
                data = {'API_KEY':apiKey,
                'req_type':"Batch"}
                r = requests.post(apiURL+"/user/viewpoints", json=data)
                jsonData = r.json()
                await message.channel.send(jsonData)
            else:
                print(apiKey)
                data =  {'API_KEY':apiKey,
                'USERNAME': text,
                'req_type':"Singular"
                }
                #headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                r = requests.post(apiURL+"/user/viewpoints", json=data)
                print(r.text)
                embed = discord.Embed(
                    title="**Points for"+' '+text+"**",
                    colour=discord.Colour.orange(),
                    description=r.text,
                    )
                status = r.status_code
                print(status)
                if status == 200:
                    await message.channel.send(embed=embed)
                elif status == 569:
                    await message.channel.send("User Not Found!")
                else:
                    await message.channel.send("An Unknown Error has Occured. Check bot and API logs.")
    
    if message.content.startswith('$addpoints'):
        #target = client.get_channel(658251987959152641)
        text = message.content
        text = text.replace("$addpoints ", "", 1)
        points = text[text.find(';'):]
        points = points.lstrip(';')
        if text.endswith(points):    
            username = text.rstrip(points).rstrip(";")
        print(apiKey)
        data =  {'API_KEY':apiKey,
        'USERNAME': username,
        'POINTS': points
        }
        #headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(apiURL+"/user/addpoints", json=data)
        #print(r.text)
        status = str(r.status_code)
        #embed = discord.Embed(
        #        title="**Points for"+username+"**",
        #        colour=discord.Colour.orange(),
        #        description=r.text,
        #        )
        if r.status_code == 200:
            await message.channel.send("points are set")
            if int(points) < 0:
                intstat = "Deducted"
            elif int(points) > 0:
                intstat = "Added"
            if int(points) == 0:
                intstat = "Unchanged"
            dbupd = client.get_channel(802015191948722216)
            embed = discord.Embed(title="NIA Database Update", description="<@"+str(message.author.id)+"> updated points for"+username)
            embed.add_field(name="Point Modification",value=intstat+" "+str(points)+" points")
            await dbupd.send(embed=embed)
        else:
            print(r.text)
            await message.channel.send("there was an error processing your request")
            await message.channel.send(f"status"+ ' ' + status)
    
    if message.content.startswith('$setpoints'):
        if message.author.guild_permissions.administrator == True:
            #target = client.get_channel(658251987959152641)
            text = message.content
            text = text.replace("$setpoints ", "", 1)
            if text.startswith("$setpoints"):
                embed = discord.Embed(
                title="**Usage Instructions**",
                colour=discord.Colour.red(),
                description="$setpoints <username>;<points:integer>",
                )
                await message.delete()
                await message.channel.send(embed=embed)
            else:
                points = text[text.find(';'):]
                points = points.lstrip(';')
                if text.endswith(points):    
                    username = text.rstrip(points).rstrip(";")
                #username = text.rstrip(';'+points)
                data =  {'API_KEY':apiKey,
                'USERNAME': username,
                'POINTS': points
                }
                print(username)
                #headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                r = requests.post(apiURL+"/user/setpoints", json=data)
                #print(r.text)
                status = str(r.status_code)
                #embed = discord.Embed(
                #        title="**Points for"+username+"**",
                #        colour=discord.Colour.orange(),
                #        description=r.text,
                #        )
                if r.status_code == 200:
                    await message.channel.send("points are set")
                    dbupd = client.get_channel(802015191948722216)
                    embed = discord.Embed(title="NIA Database Update", description="<@"+str(message.author.id)+"> updated points for"+username)
                    embed.add_field(name="Point Modification",value="Set points to "+str(points))
                    await dbupd.send(embed=embed)
                else:
                    print(r.text)
                    await message.channel.send("there was an error processing your request")
                    await message.channel.send(f"status"+ ' ' + status)
        else:
            await message.channel.send("You do not have the required permissions to use that command!")

    if message.content.startswith('$listrules'):
        # Using readline() 
        file1 = open('rules.txt', 'r') 
        count = 0
        
        for line in file1: 
            count += 1
            if ((count % 2) == 0) == False:
                line1 = line
            else:
                line2 = line
                if count == 2:
                    embed = discord.Embed(
                    title="**NIA DISCORD RULES**",
                    colour=discord.Colour.orange(),
                    description="**Welcome to the Neutral Intelligence Agency Discord server! We are an independent group of players in a top secret organization from Pinewood that attends Mayhem Syndicate raids to either join forces with the Pinewood Builders Security Team to defend the core, or with The Mayhem Syndicate to achieve a meltdown/freezedown! As you finish your verification in this server, please take the time to read the general rules and reminders here in this server.**"
                    )
                else:
                    embed = discord.Embed(
                    colour=discord.Colour.orange()
                    )
                embed.add_field(name="\u200b", value=line1, inline=False)
                embed.add_field(name="\u200b", value=line2, inline=False)
                await message.channel.send(embed=embed)        
  


    if message.content.startswith('$schedule'):
        text = message.content
        text = text.replace("$schedule ", "", 1)
        if text == "$schedule":
            if message.author.guild_permissions.administrator == True:
                embed = discord.Embed(
                title="**Usage Instructions**",
                colour=discord.Colour.red(),
                description="""
$schedule - Used to interact with the Schedule:
$schedule next - Displays next event
$schedule events - Displays next 5 events

**HR Commands**

$schedule new;<DateTime> - Date needs to be formatted exactly as follows (MM/DD/YY HH:MM), failiure to do so will break something. Times are supposed to be in UTC, using 24 hour format
$schedule remove;<eventid> - Removes the specified event - use `$schedule next` or `$schedule events` to find event IDs
                """
                )
                await message.delete()
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                title="**Usage Instructions**",
                colour=discord.Colour.red(),
                description="""
$schedule - Used to interact with the Schedule:
$schedule next - Displays next event
$schedule events - Displays next 5 events
                """
                )                
                await message.delete()
                await message.channel.send(embed=embed)
        if text.startswith("next"):
            data =  {'API_KEY':apiKey,
            'req_type':"ViewNext"
            }
            r = requests.post(apiURL+"/schedule", json=data)
            if r.status_code == 569:
                await message.channel.send("No Upcoming Event!")
            elif r.status_code == 200:
                json_data = r.json()
                embed = discord.Embed(
                    title="NIA Event",
                    description=json_data['EVENT_TYPE'],
                    colour=discord.Colour.from_rgb(104,204,237)
                )
                embed.add_field(name="Event Host", value=json_data['EVENT_HOST_NAME'])
                embed.add_field(name="Event Host", value="<@"+str(json_data['EVENT_HOST_ID'])+">")
                embed.add_field(name="Event Date", value=json_data['EVENT_DATE'])
                embed.add_field(name="Event ID", value=json_data['EVENT_ID'])
                await message.channel.send(embed=embed)
            else:
                await message.channel.send("An Unkown Error has Occured")
        if text.startswith("events"):
            text = text.replace("events", "", 1)
            if text == "":
                userAmount = 5
            else:
                userAmount = text[text.find(';'):]
                userAmount = userAmount.lstrip(';')
            data =  {'API_KEY':apiKey,
            'req_type':"Counter"
            }
            r = requests.post(apiURL+"/schedule", json=data)
            amount = int(r.text)
            userAmount = int(userAmount)
            if amount < userAmount:
                endAmount = amount
            else:
                endAmount = userAmount
            iterate = 1
            if endAmount == 0:
                await message.channel.send("No Upcoming Events!")
            else:
                await message.channel.send("Now displaying"+' **'+str(endAmount)+'** '+ "events!")
                while iterate <= endAmount:
                    data =  {'API_KEY':apiKey,
                    'req_type':"ViewNextNum",
                    'EVENT_ID':iterate
                    }
                    r = requests.post(apiURL+"/schedule", json=data)
                    iterate = iterate + 1
                    if r.status_code == 569:
                        if iterate > endAmount:
                            await message.channel.send("No Events Found!")
                    elif r.status_code == 200:
                        json_data = r.json()
                        embed = discord.Embed(
                        title="NIA Event",
                        description=json_data['EVENT_TYPE'],
                        colour=discord.Colour.from_rgb(104,204,237)
                        )
                        embed.add_field(name="Event Host", value=json_data['EVENT_HOST_NAME'])
                        embed.add_field(name="Event Host", value="<@"+str(json_data['EVENT_HOST_ID'])+">")
                        embed.add_field(name="Event Date", value=json_data['EVENT_DATE'])
                        embed.add_field(name="Event ID", value=json_data['EVENT_ID'])
                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.send("An Unkown Error has Occured")
                
        if text.startswith("new"):
            if message.author.guild_permissions.administrator == True:
                if message.author.nick is None:
                    username = message.author.name
                else:
                    username = message.author.nick
                date = text[text.find(';'):]
                date = date.lstrip(';')
                data =  {'API_KEY':apiKey,
                'EVENT_HOST_NAME': username,
                'EVENT_HOST_ID': message.author.id,
                'EVENT_TYPE': "Training",
                'EVENT_DATE': date,
                'req_type': "New"
                }
                #headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                r = requests.post(apiURL+"/schedule", json=data)
                #print(r.text)
                status = str(r.status_code)
                #embed = discord.Embed(
                #        title="**Points for"+username+"**",
                #        colour=discord.Colour.orange(),
                #        description=r.text,
                #        )
                if r.status_code == 200:
                    await message.channel.send("Event has been Scheduled!")
                        #await message.channel.send(r.text)
                elif r.status_code == 568:
                    await message.channel.send("Event already exists during the selected time slot!")
                else:
                    print(r.text)
                    await message.channel.send("there was an error processing your request")
                    await message.channel.send(f"status"+ ' ' + status)
            else:
                embed = discord.Embed(
                title="**Invalid Permissions!**",
                colour=discord.Colour.red(),
                description="You are not allowed to run that command!",
                )
                await message.channel.send(embed=embed)

        if text.startswith("remove"):
            if message.author.guild_permissions.administrator == True:
                selectedID = text[text.find(';'):]
                selectedID = selectedID.lstrip(';')
                data =  {'API_KEY':apiKey,
                'req_type':"Remove",
                'EVENT_ID':selectedID
                }
                r = requests.post(apiURL+"/schedule", json=data)
                if r.status_code == 200:
                    json_data = r.json()
                    embed = discord.Embed(
                    title="NIA Event Removed",
                    description=str(json_data['EVENT_TYPE']),
                    colour=discord.Colour.from_rgb(255,0,0)
                    )
                    embed.add_field(name="Event Host", value=json_data['EVENT_HOST_NAME'])
                    embed.add_field(name="Event Host", value="<@"+str(json_data['EVENT_HOST_ID'])+">")
                    embed.add_field(name="Event Date", value=json_data['EVENT_DATE'])
                    await message.channel.send(embed=embed)
                elif r.status_code == 569:
                    await message.channel.send("No events with selected ID found!")
                else:
                    embed = discord.Embed(
                    title="**Invalid Permissions!**",
                    colour=discord.Colour.red(),
                    description="You are not allowed to run that command!",
                    )
                    await message.channel.send(embed=embed)


    if message.content.startswith('$relcycle'):
        if message.author.id == 852614202014302219:
            await message.delete()
            embed = discord.Embed(
                title="CodenameZerodium#9466",
                description="""
A bot for the Neutrals Intelligence Agency, developed and maintained by <@852614202014302219>
                
    Currently running **NIA-Bot v1.0.4**
                
    **A new update has been issued!**

    *What's New:*
        - Batch Point Logging

    You can now use `$help` for help information!!!

Bot source code can be viewed here: [GitHub](https://github.com/HYPERDRIVE-Motivator/NIA-Bot)
                """
            )
            embed.set_footer(text="This is an automated message that displays on Bot Updates")
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/752993473350860920/4ecaf6fa0d715727e5e65deff5748759.png")
            channel = client.get_channel(735875610479558760)
            await channel.send(embed=embed)
    if message.content.startswith('$flirt'):
        #if message.author.id == 599040744334032912 and roriflirtmode == True:
        #    file = "flirts.txt"
        #    line = random.choice(open(file).readlines())
        #    await message.channel.send("<@"+str(message.author.id)+"> " + line )
        if message.author.guild_permissions.administrator == True:
            await message.delete()
            slice(message.content)
            file = "flirts.txt"
            line = random.choice(open(file).readlines())
            id = message.mentions[0].id 
            # print(line)
            #target = client.get_channel(658251987959152641)
            await message.channel.send("<@"+str(id)+"> " + line )
            #   print("<@"+str(id)+"> " + line)
        else:
            await message.delete()
            embed = discord.Embed(
                title="Unauthorised",
                description="Only **Server Admins** are allowed to use that command!",
                colour=discord.Colour.red()
            )
            embed.set_footer(text="This message will delete in 5 seconds")
            await message.channel.send(embed=embed, delete_after=5)
        
    
        #file1.close() 
    if message.content.startswith('$help'):
        await message.delete()
        if message.author.guild_permissions.administrator == True:
            embed = discord.Embed(
                title="Help Info",
                description="""
Commands:

$help - Displays this message
$ping - View bot latency
$mypoints - Displays your own points

**Schedule Commands - ALL TIMES ARE TO BE IN UTC**

$schedule - Used to interact with the Schedule:
$schedule next - Displays next event
$schedule events - Displays next 5 events

**HR Commands**

$schedule new;<DateTime> - Date needs to be formatted exactly as follows (MM/DD/YY HH:MM), failiure to do so will break something. Times are supposed to be in UTC, using 24 hour format
$schedule remove;<eventid> - Removes the specified event - use `$schedule next` or `$schedule events` to find event IDs

$viewpoints <username> - Username must be the ***DISCORD NICKNAME*** - Not Roblox username
$setpoints <username>;<number> - Username must be the ***DISCORD NICKNAME*** - Not Roblox username
$addpoints <username>;<number> - Username must be the ***DISCORD NICKNAME*** - Not Roblox username

$mute <User ***ID***> - User IDs not Usernames or mentions.
$tempmute <User ***ID***> <Minutes> - User IDs not Usernames or mentions.
$purge <# of messages> - Purges messages in the current channel.
$globalfilterstateget - Returns the state of the GlobalFilter *Override*
                """,
                colour=discord.Colour.from_rgb(104, 204, 237)

            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/752993473350860920/4ecaf6fa0d715727e5e65deff5748759.png")
            embed.set_author(name="CodenameZerodium#9466",icon_url="https://cdn.discordapp.com/avatars/752993473350860920/4ecaf6fa0d715727e5e65deff5748759.png")
            await message.channel.send(embed=embed)

        if message.author.guild_permissions.administrator == False:
            embed = discord.Embed(
                title="Help Info",
                description="""
Commands:

$help - Displays this message
$ping - View bot latency
$mypoints - Displays your own points

**Schedule Commands - ALL TIMES ARE TO BE IN UTC**

$schedule - Used to interact with the Schedule:
$schedule next - Displays next event
$schedule events - Displays next 5 events
                """,
                colour=discord.Colour.from_rgb(104, 204, 237)

            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/752993473350860920/4ecaf6fa0d715727e5e65deff5748759.png")
            embed.set_author(name="CodenameZerodium#9466",icon_url="https://cdn.discordapp.com/avatars/752993473350860920/4ecaf6fa0d715727e5e65deff5748759.png")
            await message.channel.send(embed=embed)


    if message.content.startswith('$batchlog'):
        if message.author.guild_permissions.administrator == True:
            text = message.content
            text = text.replace("$batchlog ", "", 1)
            if text.startswith('$batchlog'):
                text = text.replace("$batchlog", "", 1)
            if text.startswith("$batchlog"):
                await message.channel.send("an error has occured")
                return
            text = text.split()
            stagingList = []
            for x in text:
                if ';' in x:
                    stagingList.append(x)
                else:
                    await message.channel.send("an error has occured, please check your formattings")
                    return
            #await message.channel.send(stagingList)
            #print(stagingList)
            embed = discord.Embed(title="NIA Point Log", description="Batch Logging (Adding these points) \n Please say 'Approve' or 'Reject'")
            for x in stagingList:
                operate = str(x)
                points = operate[operate.find(";"):]
                points = points.lstrip(";")
                if operate.endswith(points):    
                    username = operate.rstrip(points).rstrip(";")
                    memberList = message.guild.members
                    #print(memberList)
                    userid = None
                    for member in memberList:
                        if member.nick == username:
                            userid = member.id
                    if userid is None:
                        await message.channel.send("The user: "+username+" was not found in this server. Please try running $batchlog again with the correct spellings.")
                        return
                    embed.add_field(name=username,value="Points for <@"+str(userid)+"> will be modified by " +str(points))
            try:
                await message.channel.send(embed=embed)
                msg = await client.wait_for("message",timeout=30) # 30 seconds to reply
            except asyncio.TimeoutError:
                await message.channel.send("Sorry, you didn't reply in time!")
                return
            if 'approve' in msg.content.lower():
                for x in stagingList:
                    operate = str(x)
                    points = operate[operate.find(";"):]
                    points = points.lstrip(";")
                    if operate.endswith(points):    
                        username = operate.rstrip(points).rstrip(";")
                        data =  {'API_KEY':apiKey,
                        'USERNAME': username,
                        'POINTS': points
                        }
                        r = requests.post(apiURL+"/user/addpoints", json=data)
                        status = str(r.status_code)
                        if r.status_code == 200:
                            await message.channel.send("points are logged for: "+username)
                            dbupd = client.get_channel(802015191948722216)
                            embed = discord.Embed(title="NIA Database Update", description="<@"+str(message.author.id)+"> updated points for: "+username)
                            embed.add_field(name="Point Modification",value="Modified points to "+str(r.text))
                            embed.add_field(name="Point Modification",value="Modified points by "+str(points))
                            await dbupd.send(embed=embed)
                        else:
                            print(r.text)
                            await message.channel.send("there was an error processing points for:"+username)
                            await message.channel.send(f"status"+ ' ' + status)
                clicker = await message.channel.send("Send DB Update message? [Y/n]")
                try:
                    msg = await client.wait_for("message", timeout=30)
                except asyncio.TimeoutError:
                    await message.channel.send("No Database update notification sent. - User timeout",delete_after=5)
                    return
                if "n" in msg.content.lower():
                    await clicker.delete()
                    await message.channel.send("No Database update notification sent.",delete_after=5)
                    return
                elif "y" in msg.content.lower():
                    await clicker.delete()
                    msg.delete()
                    clicker2 = await message.channel.send("Please input Database Update Notification Message")
                    try:
                        msg = await client.wait_for("message",timeout=30)
                    except asyncio.TimeoutError:
                        await message.channel.send("No Database update sent notification. - User timeout",delete_after=5)
                        return
                    targMsg = msg.content
                    targChannel = client.get_channel(753076693379317983)
                    embed = discord.Embed(title="NIA Database Update Notification",description=str(targMsg))
                    embed.set_author(name="CodenameZerodium#9466",icon_url="https://cdn.discordapp.com/avatars/752993473350860920/4ecaf6fa0d715727e5e65deff5748759.png")
                    embed.set_footer(text=msg.author.nick,icon_url=msg.author.avatar_url)
                    await targChannel.send(embed=embed)
                    await msg.delete()
                    await clicker2.delete()
                    return
                        

                
            elif 'reject' in msg.content.lower():
                await message.channel.send("Point log Rejected.")
            else:
                embed = discord.Embed(title="Invalid Command Flow!",description="Please say 'Approve' or 'Reject' (not case sensitive), Please start log process over.",colour=discord.Colour.red)
                errormsg = await message.channel.send(embed=embed)
                time.asyncio.sleep(60)

                return

    #if message.content.startswith('$testcmd'):
     
        

                
                


    if message.content.startswith('$DEMOTE'):
        text = message.content
        text = text.replace("$DEMOTE ", "", 1)
        embed = discord.Embed(title="NIA Demotion",description="Demotion set for: <@"+str(text)+">!")
        embed.set_footer(name="Message will auto delete in 30 seconds")
        await message.channel.send(embed=embed,delete_after=30)



#async def userCheck(message):
#      if message.author != "HYPERٴٴٴٴٴٴٴٴٴٴٴٴٴٴٴٴٴٴٴٴٴٴDRIVE#0001":
#          await message.channel.send("You're not allowed to use that command!")
      



client.run(os.getenv("BOT_TOKEN"))

@bot.command(name="aaaa")
async def aaaa(ctx, arg):
    await ctx.send(arg)


