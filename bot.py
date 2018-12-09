import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
import platform
import colorsys
import youtube_dl
import random
import os
import time
import aiohttp
from discord.utils import find
from discord import Game, Embed, Color, Status, ChannelType

#cogs = storage/emulated/0/Android/Azone/Cogs

from discord import opus
OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll',
             'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']
def load_opus_lib(opus_libs=OPUS_LIBS):
    if opus.is_loaded():
        return True

    for opus_lib in opus_libs:
            try:
                opus.load_opus(opus_lib)
                return
            except OSError:
                pass

    raise RuntimeError('Could not load an opus lib. Tried %s' %
                       (', '.join(opus_libs)))
load_opus_lib()

in_voice=[]


players = {}
songs = {}
playing = {}


async def all_false():
    for i in bot.servers:
        playing[i.id]=False


async def checking_voice(ctx):
    await asyncio.sleep(130)
    if playing[ctx.message.server.id]== False:
        try:
            pos = in_voice.index(ctx.message.server.id)
            del in_voice[pos]
            server = ctx.message.server
            voice_client = bot.voice_client_in(server)
            await voice_client.disconnect()
            await bot.say("{} left because there was no audio playing for a while".format(bot.user.name))
        except:
            pass

owner = ["362672438699622403"]
developer = ["362672438699622403"]

BOT_PREFIX = ("axe", "a!", "ax", "366579653395349505", "<@366579653395349505>")

#timestamp=datetime.datetime.utcfromtimestamp(1541415948)

bot = Bot(description="You are not supposed to see this", command_prefix=BOT_PREFIX, pm_help = True)
bot.remove_command('help')

server1 = bot.get_server(472829296940154901)

#----- Extensions
#bot.load_extension('spoiler')

async def status_task():
    while True:
        await bot.change_presence(game=discord.Game(name='for axhelp', type=1))
        await asyncio.sleep(5)
        await bot.change_presence(game=discord.Game(name='with '+str(len(set(bot.get_all_members())))+' users', type=1))
        await asyncio.sleep(3)
        await bot.change_presence(game=discord.Game(name='Begone', type=1))
        await asyncio.sleep(3)
        await bot.change_presence(game=discord.Game(name='Thot', type=1))
        await asyncio.sleep(1)
     
         # ------------ Oofy  
	
@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)
    in_voice.append(ctx.message.server.id)


async def player_in(con):  # After function for music
    try:
        if len(songs[con.message.server.id]) == 0:  # If there is no queue make it False
            playing[con.message.server.id] = False
            bot.loop.create_task(checking_voice(con))
    except:
        pass
    try:
        if len(songs[con.message.server.id]) != 0:  # If queue is not empty
            # if audio is not playing and there is a queue
            songs[con.message.server.id][0].start()  # start it
            await bot.send_message(con.message.channel, 'Now queueed')
            del songs[con.message.server.id][0]  # delete list afterwards
    except:
        pass
        


@bot.command(pass_context=True)
async def play(ctx, *,url):

    opts = {
        'default_search': 'auto',
        'quiet': True,
    }  # youtube_dl options


    if ctx.message.server.id not in in_voice: #auto join voice if not joined
        channel = ctx.message.author.voice.voice_channel
        await bot.join_voice_channel(channel)
        in_voice.append(ctx.message.server.id)

    

    if playing[ctx.message.server.id] == True: #IF THERE IS CURRENT AUDIO PLAYING QUEUE IT
        voice = bot.voice_client_in(ctx.message.server)
        song = await voice.create_ytdl_player(url, ytdl_options=opts, after=lambda: bot.loop.create_task(player_in(ctx)))
        songs[ctx.message.server.id]=[] #make a list 
        songs[ctx.message.server.id].append(song) #add song to queue
        await bot.say("Audio {} is queued".format(song.title))

    if playing[ctx.message.server.id] == False:
        voice = bot.voice_client_in(ctx.message.server)
        player = await voice.create_ytdl_player(url, ytdl_options=opts, after=lambda: bot.loop.create_task(player_in(ctx)))
        players[ctx.message.server.id] = player
        # play_in.append(player)
        if players[ctx.message.server.id].is_live == True:
            await bot.say("Can not play live audio yet.")
        elif players[ctx.message.server.id].is_live == False:
            player.start()
            await bot.say("Now playing audio")
            playing[ctx.message.server.id] = True



@bot.command(pass_context=True)
async def queue(con):
    await bot.say("There are currently {} audios in queue".format(len(songs)))

@bot.command(pass_context=True)
async def pause(ctx):
    players[ctx.message.server.id].pause()

@bot.command(pass_context=True)
async def resume(ctx):
    players[ctx.message.server.id].resume()
          
@bot.command(pass_context=True)
async def volume(ctx, vol:float):
    volu = float(vol)
    players[ctx.message.server.id].volume=volu


@bot.command(pass_context=True)
async def skip(con): #skipping songs?
  songs[con.message.server.id]
    
    
    
@bot.command(pass_context=True)
async def stop(con):
    players[con.message.server.id].stop()
    songs.clear()

@bot.command(pass_context=True)
async def leave(ctx):
    pos=in_voice.index(ctx.message.server.id)
    del in_voice[pos]
    server=ctx.message.server
    voice_client=bot.voice_client_in(server)
    await voice_client.disconnect()
    songs.clear()

#@bot.command(pass_context=True)
#async def send1(ctx): #--- Not Working Because: This bot isn't hosted with my phone.
#    area=ctx.message.channel
#    await bot.send_file(area, r"/storage/emulated/0/Android/Azone/BotPic/zone.png",filename="zone.png",content="")
    
#@bot.command(pass_context=True)
#async def send2(ctx): #--- Not Working Because: This bot isn't hosted with my phone.
#    area=ctx.message.channel
#    await bot.send_file(area, r"/storage/emulated/0/Android/Azone/BotPic/zone1.png",filename="zone.png",content="")
               

#@bot.command(pass_context=True)
#async def send(ctx): #--- Not Working Because: This bot isn't hosted with my phone.
#    area=ctx.message.channel
#    await bot.send_file(area, r"/storage/emulated/0/Android/Azone/BotPic/friendzone.png",filename="™.png",content="")
# ---
@bot.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def rules(ctx):
	embed = discord.Embed(colour = discord.Colour.orange())
	embed.set_author(name="Rules")
	#embed.set_thumbnail(url=ctx.message.author.avatar_url)
	embed.set_footer(text='{}'.format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
	embed.add_field(name="1. Don't spam in any channels.", value='You will be muted immediately.')
	embed.add_field(name='2. No NSFW.', value='Posting an NSFW image/link at any time and your image permissions will be removed forever. Expect in NSFW channels.')
	embed.add_field(name='3. No advertising.', value='Do not post Discord server links, social media links, or any nsfw website without permission. That also includes DM advertising. The only links we will allow you to post are screenshot links or a link relevant to the current discussion.')
	embed.add_field(name='4. Only have conversations in #general.', value='Keep up with the theme in every channel. Do not talk in #memes, #selfies, or any of the channels in the fun category.')
	embed.add_field(name='5. Do not bully people.', value='Do not target and harass people')
	embed.add_field(name='6. Do not spam bot commands outside of #bots.', value='Doing it outside that channel will get you muted.')
	embed.add_field(name='7. Try your best to include new members in your conversations.', value='Make them feel welcome. Please try not to ignore new members. Remember, you were new once too. Try to make everyone feel included')
	embed.add_field(name='8. Please dont ask to be a mod.', value='That just annoys the Owner and reduces your chances to become one.')
	embed.add_field(name='9. Dont expect to get your roles back when leaving the server.', value='If you leave, you are consenting to losing all of your roles.')
	embed.add_field(name='10. Dont fragment your messages to boost your level', value='Fragmenting is defined as intentionally shortening your messages to increase your level. For example, sending 1 word per message')
	embed.add_field(name='11. Dont be racist or derogatory.', value='Racism in a derogatory manner wont be tolerated')
	await bot.say(embed=embed)
	await asyncio.sleep(1)
	await bot.delete_nessage(ctx.message)

@bot.command(pass_context = True)
@commands.has_permissions(administrator=True) 
async def test123(ctx):
	embed = discord.Embed(title=" ")
	embed.set_author(name="Commands", icon_url=ctx.message.author.avatar_url)
	embed.add_field(name="General", value="`avatar`, `userinfo`, `serverinfo`, `poll`, `info`", inline=False)
	embed.add_field(name="Moderation", value="`kick`, `ban`, `mute`, `unmute`", inline=False)
	embed.set_footer(text="{}".format(ctx.message.server), icon_url=ctx.message.author.avatar_url)
	await bot.say(embed=embed)
	


# ---
 
@bot.command(pass_context=True)
async def partners(ctx):
	embed=discord.Embed(
	colour = discord.Colour.orange()
    )
	embed.set_author(name="Partnerships", icon_url='https://cdn.discordapp.com/attachments/511228031008768002/511435194100613122/zone.png')
	embed.add_field(name="Owners:", value="`Barry#0828` & `Nick#4671`", inline=False)
	embed.add_field(name="FriendZone", value="<:friendhappy:511813270437494794> | [Join here](https://discord.gg/wtqV67x)", inline=True)
	embed.add_field(name="Zone", value="⊳ [Join here](https://discord.gg/ZFzHHDb)", inline=True)
	embed.add_field(name="Add the bot", value="<:bottag:511826577139433473> [Click here!](https://discordapp.com/oauth2/authorize?client_id=366579653395349505&scope=bot&permissions=8)", inline=True)
	embed.set_footer(text="Requested by {}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
# ---------------------------	
#[Coming Soon!](https://www.google.com)
#embed.set_author(name='Help', icon_url='https://cdn.discordapp.com/attachments/366584787902922752/506896480984891402/PingReeeGif.gif')
# ---------------------------
@bot.event
async def on_ready():
    print('Logged in as '+bot.user.name+' (ID:'+bot.user.id+') | Connected to '+str(len(bot.servers))+' servers | Connected to '+str(len(set(bot.get_all_members())))+' users')
    print('--------') # -
    print('--------') # --
    print('🕵 Succesfull') # ---
    print('load') # ----
    print('--------') # -----
    print('--------') # ------
    print('Invite link: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id)) # -------
    bot.loop.create_task(status_task())

def is_owner(ctx):
    return ctx.message.author.id == "362672438699622403, 282998342315933707"
    
@bot.command(pass_context=True)
async def help(ctx):
	author = ctx.message.author
	message = ctx.message
	embed = discord.Embed(colour = discord.Colour.orange())
	embed.set_author(name='Help Menu', icon_url='https://cdn.discordapp.com/attachments/366584787902922752/508926666622369805/8471_PepeHalloween.gif')
	embed.add_field(name='cmhelp', value='for moderation commands', inline=False)
	embed.add_field(name='cghelp', value='for general commands', inline=False)
	embed.set_footer(text ='Prefix: c', icon_url=bot.user.avatar_url)
	await bot.send_message(author, embed=embed)
	await bot.delete_message(ctx.message)
	
#@bot.command(pass_context=True)
#async def mhelp(ctx):
#	embed=discord.Embed(colour = discord.Colour.red())
#	embed.set_author(text="Moderation",url="https://discordapp.com/api/oauth2/authorize?client_id=366579653395349505&permissions=2146827511&scope=bot", icon_url=bot.user.avatar_url)
#	embed.set_thumbnail(url=bot.user.avatar_url)
#	embed.add_field(name="Moderation", value="`kick`, `ban`", inline=True)
#	embed.add_field(name="Misc", value="`userinfo`, `serverinfo`", inline=True)
#	embed.set_footer(text="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
#	await bot.say(embed=embed)

@bot.command(pass_context=True)
async def ghelp(ctx):
	embed=discord.Embed(title="  ")
	embed.set_author(name="Help", icon_url=bot.user.avatar_url)
	embed.add_field(name="General", value="`avatar`, `poll`", inline=True)
	embed.add_field(name="Bot", value="`info`", inline=True)
	embed.add_field(name="Owner", value="`setname`, `setgame`, `setavatar`", inline=True)
	embed.set_footer(text="Charlie | Requested by {}".format(ctx.message.author), icon_url=bot.user.avatar_url)
	await bot.say(embed=embed)
	
@bot.command(pass_context=True)
async def mhelp(ctx):
	embed=discord.Embed(title="  ")
	embed.set_author(name="Moderation", icon_url=bot.user.avatar_url)
	embed.add_field(name="Moderation", value="`kick`, `ban`", inline=True)
	embed.add_field(name="Misc", value="`userinfo`, `serverinfo`", inline=True)
	embed.set_footer(text="Charlie | Requested by {}".format(ctx.message.author), icon_url=bot.user.avatar_url)
	await bot.say(embed=embed)

#@bot.command(pass_context=True)
#async def ghelp(ctx):
#	user = discord.Member
#	embed=discord.Embed(title="Add Charlie", url="https://discordapp.com/api/oauth2/authorize?client_id=366579653395349505&permissions=2146827511&scope=bot", color=544F4F)
#	embed.set_author(name="Help", url="http://example.com", icon_url=bot.user.avatar_url)
#	embed.set_thumbnail(url=bot.user.avatar_url)
#	embed.add_field(name="General", value="`avatar`, `poll`", inline=True)
#	embed.add_field(name="Bot", value="`info`", inline=True)
#	embed.add_field(name="Owner", value="`setname`, `setgame`, `setavatar`", inline=True)
#	embed.set_footer(text="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
#	await bot.say(embed=embed)

@bot.command(pass_context=True)
async def info(ctx):
    author = ctx.message.author
    message = ctx.message
    
    embed = discord.Embed(
    colour = discord.Colour.orange()
    ) #-------------- Zone
    embed.set_author(name="{}'s Info".format(bot.user.name), icon_url=bot.user.avatar_url)
    message = ctx.message
    embed.add_field(name='Owners:', value='Barry`#0828` & Nick`#4671`', inline=False)
    embed.add_field(name='Library:', value='<:py:511826873374736414> discord.py', inline=False)
    embed.add_field(name='Servers:', value='{}'.format(len(bot.servers)), inline=True)
    embed.add_field(name='Users:', value='{}'.format((len(set(bot.get_all_members())))), inline= True)
    embed.add_field(name='Server:', value='[Click here!](https://discord.gg/wtqV67x)', inline=True)
    embed.add_field(name='Website:', value='[Coming Soon!](https://www.google.com)', inline=True)
    embed.set_footer(text ='{}'.format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
    await bot.say(embed=embed)
    await bot.add_reaction(message, emoji="🙈")
    await asyncio.sleep(2)
    await bot.delete_message(ctx.message)

#[Click here!](http://tripl3dogdare.com

#(len(set(bot.get_all_members())))
#----- OWNER

@bot.command(pass_context=True, hidden=True)
async def setavatar(ctx, url):
	if ctx.message.author.id not in owner:
		return
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as r:
			data = await r.read()
	await bot.edit_profile(avatar=data)
	await bot.say("I changed my avatar.", delete_after=6)
	await bot.delete_message(ctx.message)



  	
@bot.command(pass_context=True, hidden=True)
async def setgame(ctx, *, game):
    if ctx.message.author.id not in owner:
        return
    game = game.strip()
    if game != "":
        try:
            await bot.change_presence(game=discord.Game(name=game))
        except:
            await bot.say("Failed to change game")
        else:
            await bot.say("Successfuly changed game to {}".format(game))
    else:
        await bot.send_cmd_help(ctx)

@bot.command(pass_context=True, hidden=True)
async def setname(ctx, *, name):
    if ctx.message.author.id not in owner:
        return
    name = name.strip()
    if name != "":
        try:
            await bot.edit_profile(username=name)
        except:
           await bot.say("Failed to change name")
        else:
            await bot.say("Successfuly changed name to {}".format(name))
    else:
        await bot.send_cmd_help(ctx)
        await bot.delete_message(ctx.message)


 #---- MODERATION
@bot.command(pass_context = True)
async def ban(ctx, member: discord.Member):
     if ctx.message.author.server_permissions.ban_members or ctx.message.author.id == '362672438699622403':
        role = discord.utils.get(member.server.roles, name='Muted')
        await bot.add_roles(member, role)
        embed=discord.Embed(title="User Banned!", description="**{0}** was banned by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await bot.say(embed=embed)
        await bot.ban(member)
     else:
        embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        await bot.say(embed=embed)
        await bot.delete_message(ctx.message)

@bot.command(pass_context = True)
@commands.has_permissions(manage_roles=True)     
async def role(ctx, user: discord.Member, *, role: discord.Role = None):
        if role is None:
            return await bot.say("You haven't specified a role! ")

        if role not in user.roles:
            await bot.add_roles(user, role)
            return await bot.say("{} role has been added to {}.".format(role, user))

        if role in user.roles:
            await bot.remove_roles(user, role)
            return await bot.say("{} role has been removed from {}.".format(role, user))

@bot.command(pass_context = True)
async def kick(ctx, member: discord.Member):
     if ctx.message.author.server_permissions.kick_members or ctx.message.author.id == '362672438699622403':
        role = discord.utils.get(member.server.roles, name='Muted')
        await bot.add_roles(member, role)
        embed=discord.Embed(title="User Kicked!", description="**{0}** was kicked by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await bot.say(embed=embed)
        await bot.kick(member)
        await bot.delete_message(ctx.message)
     else:
        embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        await bot.say(embed=embed)
        await bot.delete_message(ctx.message)
 
@bot.command(pass_context = True)
async def purge(ctx, number):
    if ctx.message.author.server_permissions.kick_members or ctx.message.author.id == '362672438699622403':    
        mgs = [] #Empty list to put all the messages in the log
        number = int(number) #Converting the amount of messages to delete to an integer
        async for x in bot.logs_from(ctx.message.channel, limit = number):
            mgs.append(x)
        await bot.delete_messages(mgs)
        await bot.say('**Messages cleared**', delete_after=5)
    else:
        await bot.say("No Perms!")
 
 
@bot.command(pass_context = True)
@commands.has_permissions(administrator=True)     
async def makemod(ctx, user: discord.Member):
    nickname = '[🕵] ' + user.name
    await bot.change_nickname(user, nickname=nickname)
    role = discord.utils.get(ctx.message.server.roles, name='Moderator')
    await bot.add_roles(user, role)
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='Congratulations Message')
    embed.add_field(name = '__Congratulations__',value ='**<@{}> has been promoted to Moderator!**'.format(user.id),inline = False)
    embed.set_image(url = 'https://preview.ibb.co/i1izTz/ezgif_5_e20b665628.gif')
    await bot.send_message(user,embed=embed)
    await bot.delete_message(ctx.message)
 
 #if not msg: await bot.say("Please specify a user to warn")
 #   else:
 
@bot.command(pass_context = True)
@commands.has_permissions(manage_nicknames=True)     
async def setnick(ctx, user: discord.Member, *, nickname):
    await bot.change_nickname(user, nickname)
    await bot.delete_message(ctx.message)
 
 #----- server
@bot.command(pass_context = True)    
async def userinfo(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_thumbnail(url = user.avatar);
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)
 
@bot.command(pass_context=True)  
@commands.has_permissions(kick_members=True)     

async def serverinfo(ctx):
    '''Displays Info About The Server!'''

    server = ctx.message.server
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50: #Just in case there are too many roles...
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles'%len(roles))

    roles = ', '.join(roles);
    channelz = len(server.channels);
    time = str(server.created_at); time = time.split(' '); time= time[0];
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    join = discord.Embed(description= '%s '%(str(server)),title = 'Server Name', color = discord.Color((r << 16) + (g << 8) + b));
    join.set_thumbnail(url = server.icon_url);
    join.add_field(name = 'Owner', value = str(server.owner) + '\n' + server.owner.id);
    join.add_field(name = 'ID', value = str(server.id))
    join.add_field(name = 'Member Count', value = str(server.member_count));
    join.add_field(name = 'Text/Voice Channels', value = str(channelz));
    join.add_field(name = 'Roles (%s)'%str(role_length), value = roles);
    join.set_footer(text ='Created: %s'%time);

    return await bot.say(embed = join);
 
 
 #---- Misc
	
@bot.command(pass_context=True)
async def avatar(ctx, member: discord.Member):
	embed = discord.Embed(title="{}'s avatar".format(member.name), url=member.avatar_url)
	embed.set_image(url=member.avatar_url)
	embed.set_footer(text='{}'.format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
	await bot.delete_message(ctx.message)
	await bot.say(embed=embed) # ----------------------------------- EMBED ONE
 
#@bot.command(pass_context=True, no_pm=True)
#async def avatar(ctx, member: discord.Member):
#    """User Avatar"""
#    await bot.reply("{}".format(member.avatar_url))
#    await bot.delete_message(ctx.message)
 
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def embed(ctx, *args):
    """
    Sending embeded messages with color (and maby later title, footer and fields)
    """
    argstr = " ".join(args)
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    text = argstr
    color = discord.Color((r << 16) + (g << 8) + b)
    await bot.send_message(ctx.message.channel, embed=Embed(color = color, description=text))
    await bot.delete_message(ctx.message)

 
@bot.command()
async def invite():
  	await bot.say("**Check your DMs.**")
  	await bot.whisper("**Add me with this link** {}".format(discord.utils.oauth_url(bot.user.id)))
  	
@bot.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def say(ctx, *, msg = None):
    await bot.delete_message(ctx.message)
    if not msg: await bot.say("Please specify a message to send")
    else: await bot.say(msg)
    return
  	
@bot.command(pass_context=True)
async def poll(ctx, question, *options: str):
        if len(options) <= 1:
            await bot.say('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await bot.say('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['👍', '👎']
        else:
            reactions = ['1\u20e3', '2\u20e3', '3\u20e3', '4\u20e3', '5\u20e3', '6\u20e3', '7\u20e3', '8\u20e3', '9\u20e3', '\U0001f51f']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title='question', description=''.join(description), color = discord.Color((r << 16) + (g << 8) + b))
        react_message = await bot.say(embed=embed)
        for reaction in reactions[:len(options)]:
            await bot.add_reaction(react_message, reaction)
        embed.set_footer(text='Poll ID: **{}**'.format(react_message.id))
        await bot.edit_message(react_message, embed=embed)



#--- HELP Commands
#@bot.command(pass_context = True)
#async def modhelp(ctx):
 #   author = ctx.message.author
 #   message = ctx.message
 #   embed = discord.Embed(
 #   colour = discord.Colour.orange()
  #  )
 #   embed.set_author(name='Moderation', icon_url='https://cdn.discordapp.com/attachments/366584787902922752/508926667146919946/5311_BlobKnight_2.gif')
 #   embed.add_field(name = 'd!kick',value ='Use it like ``d!kick (user)``',inline = False)
  #  embed.add_field(name = 'd!ban',value ='Use it like ``d!ban (user)``',inline = False)
#    embed.add_field(name = 'd!userinfo',value ='Use it like ``d!userinfo (user)``',inline = False)
  #  embed.add_field(name = 'd!makemod',value ='Use it like ``d!makemod (user)``(Assigns Moderator role)',inline = False)
 #   embed.add_field(name = 'd!setnick',value ='Use it like ``d!setnick (user) (new name)``',inline = False)
 #   embed.set_footer(text ='{}'.format(message.timestamp))
 #   await bot.send_message(author,embed=embed)
 #   await bot.say('<:enveloping:511846521478840320> Check DMs For Information', delete_after=5)
 #   await bot.delete_message(ctx.message)
   
#@bot.command(pass_context = True)
#async def ownerhelp(ctx):
 #   author = ctx.message.author
#    message = ctx.message
 #   r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
#    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
#    embed.set_author(name='Owner', icon_url='https://cdn.discordapp.com/attachments/366584787902922752/508926667146919946/5311_BlobKnight_2.gif')
#    embed.add_field(name = 'd!setname',value ='Use it like ``d!setname (name)``',inline = False)
 #   embed.add_field(name = 'd!setgame',value ='Use it like ``d!setgame (game)``',inline = False)
#    embed.add_field(name = 'd!setavatar',value ='Use it like ``d!setavatar (url)``',inline = False)
#    embed.set_footer(text ='{}'.format(message.timestamp))
#    await bot.send_message(author,embed=embed)
#    await bot.say('<:enveloping:511846521478840320> Check DMs For Information', delete_after=5)
#    await bot.delete_message(ctx.message)
  
#
#@bot.command(pass_context = True)
#async def generalhelp(ctx):
#    author = ctx.message.author
#    message = ctx.message
#    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
#    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
#    embed.set_author(name='General', icon_url='https://cdn.discordapp.com/attachments/366584787902922752/508927292542550016/2284_PepoSalute.gif')
#    embed.add_field(name = 'd!info',value ='Use it like ``d!info``',inline = False)
#    embed.add_field(name = 'd!avatar',value ='Use it like ``d!avatar (user)``',inline = False)
#    embed.add_field(name = 'd!partners',value ='Use it like ``d!partners``',inline = False)
#    embed.add_field(name = 'd!poll',value ='Use it like ``d!poll "Question" "Option1" "Option2" ..... "Option9"``',inline = False)
#    embed.set_footer(text ='{}'.format(message.timestamp))
#    await bot.send_message(author,embed=embed)
#    await bot.say('<:enveloping:511846521478840320> Check DMs For Information', delete_after=5)
#    await bot.delete_message(ctx.message)


#oofoofoofoofoofoofoofoof
bot.run(os.getenv('Token')) #--- Tokens
