

# Discord for utilizing discord's api, time for waiting related functions, asyncpraw to access reddit posts,  random to create a sense of suspense, and importing commands from discord.ext to create
# a bot.
import discord
import time
import asyncpraw
import random
import datetime
import json
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


# Accessing Reddit's API, this stuff is supposed to be secret.
reddit = asyncpraw.Reddit(client_id='IVJMP4juDRfx-w',
client_secret='2q_P6io3kdE1YMd1m6NMOXfBaj0HjA', 
user_agent='Kitten Bot by SomethingRandom0768')

# This is for the list of individuals in the list to receive kitty images.
listWithUserIDs = []

# List of subreddits to choose from
listOfSubreddits = ['kittengifs', 'Kitten_gifs']

# Counter to prevent people from spamming amogus command.
amogus_counter = 0 

@bot.command()
async def devMode(ctx):
    """Only the dev version of the bot will respond to this command."""
    await ctx.send("Yes, this is a DEV version of the bot.")

@bot.command()
# This command is used to obtain a single kitten gif or image by utilizing PRAW to retrieve a url.
async def getsinglekitty(ctx):
    # Chooses a random subreddit from listWithSubreddits
    randomSubreddit = random.choice(listOfSubreddits)
    chosenSubreddit = await reddit.subreddit(randomSubreddit)

    chosenSubreddit_post = await chosenSubreddit.random()
    redditLink = "https://www.reddit.com/" + chosenSubreddit_post.permalink

    if chosenSubreddit == await reddit.subreddit('Kitten_Gifs') or chosenSubreddit == await reddit.subreddit('kittengifs'):
        await ctx.channel.send(f"This gif was posted by redditor " + chosenSubreddit_post.author.name)
    else:
        while 'v.redd.it' in chosenSubreddit_post.url or 'gallery' in chosenSubreddit_post.url or 'youtu.be' in chosenSubreddit_post.url or 'youtube' in chosenSubreddit_post.url:
            print(chosenSubreddit_post.url)
            chosenSubreddit_post = await chosenSubreddit.random()
        else:
            print(chosenSubreddit_post.url)
            messageEmbed = discord.Embed(author='Kitten Bot(!)#4954', colour=3447003, title="Here's a cat, just for you! ^-^")
            messageEmbed.add_field(name='Post Information', value=f"This post was created by reddit user {chosenSubreddit_post.author} which can be found [here]({redditLink})")
            messageEmbed.set_footer(text="If the image/gif/video fails, feel free to click the blue link to see what would've been posted :D")
            messageEmbed.set_image(url=chosenSubreddit_post.url)
            await ctx.channel.send(embed=messageEmbed)

@bot.command() 
async def sendbigkitty(ctx):
     # Sends a giant kitty.
     await ctx.send('https://cdn.discordapp.com/attachments/837418361696288828/837433194055598110/image0.jpg')

@bot.command()
# Command to ask for multiple cats, limit is 15
async def getmultiplekitties(ctx, number):
    if int(number) > 15:
        await ctx.send("That's too many! Please do fewer than 16 :( it makes me tired.")
    else:
        number = int(number)
    for i in range(0, number):
        subreddit = await reddit.subreddit(random.choice(listOfSubreddits))
        submission = await subreddit.random()

        while 'v.redd.it' in submission.url or 'gallery' in submission.url or 'youtu.be' in submission.url or 'youtube' in submission.url:
            print(submission.url)
            submission = await subreddit.random()
            time.sleep(1)
        else:
            redditLink = "https://www.reddit.com/" + submission.permalink
            messageEmbed = discord.Embed(author='Kitten Bot(!)#4954', colour=3447003, title=f"Here's a cat, just for you! ^-^ ({i+1} of {number})")
            messageEmbed.add_field(name='Post Information', value=f"This post was created by reddit user {submission.author} which can be found [here]({redditLink})")
            messageEmbed.set_footer(text="If the image/gif/video fails, feel free to click the blue link to see what would've been posted :D")
            messageEmbed.set_image(url=submission.url)
            await ctx.channel.send(embed=messageEmbed)


@bot.command()
# Posts the dictionary of commands instantiated at the beginning of this file.
async def postcommands(ctx):
    with open('commands_list.json') as commands_file:
        cmds = json.load(commands_file)
        commands_embed = discord.Embed.from_dict(cmds)

    await ctx.channel.send(embed=commands_embed)


@bot.command()
# If you want to pet the kitten bot
async def petbot(ctx):
    await ctx.channel.send(f"Mew! {ctx.message.author}, thank you for petting me! ^-^")


@bot.command()
# joke command, not meant to be anything serious
async def sendkittenstochina(ctx):
    await ctx.channel.send(f"Mew mew mew!!!! Sending my brothers and sisters to China! ^-^")

@bot.command()
async def say(ctx, *message):
# Allows users to speak as the kitten bot, although they will need to delete their own message as quickly as possible.
    messagetosend = ""
    for word in message:
            messagetosend += " " + word
    if '@everyone' in message:
        await ctx.channel.send(f"{ctx.author} has used an everyone ping!")
    elif 'sus' in message:
        await ctx.channel.send("You do not have those privileges. LOOOOOOL")
        await ctx.message.delete()
    else:
        try:
            await ctx.channel.send(messagetosend)
            await ctx.message.delete()
        except discord.errors.HTTPException:
            await ctx.channel.send("Cannot send an empty message.")



@bot.command()
async def pokeyourself(ctx):
# Why not poke yourself? Sometimes, it might be all that you need.
    await ctx.author.send("You have poked yourself! ^_^")


@bot.command()
async def listservers(ctx):
    # Lists the names of servers that Kitten Bot is in and their IDs.
    if ctx.author.id == 265596926857183252:
        server_list = ' '
        for server in bot.guilds:
            server_list += f"+ {server.name} (ID: {server.id}) \n"
        await ctx.channel.send(server_list)
    else:
        await ctx.channel.send("You do not have access to this command.")	

@bot.command()
async def leaveserver(ctx, server_id):
    # Removes kitten bot from the server id given
    if ctx.author.id == 265596926857183252:
        server_to_leave = bot.get_guild(int(server_id))
        await server_to_leave.leave()
        owner = await bot.fetch_user(265596926857183252)
        await owner.send(f"Kitten Bot has left from {server_to_leave.name} (ID: {server_to_leave.id} )")
    else:
        await ctx.send("You do not have access to this command.")


@bot.event
# Saying kitten bot will doom you to a breakfast with cookies and milk.
async def on_message(message):
    if "kitten bot" in message.content.lower():
        game = discord.Game(f"I see you, {message.author}")
        await bot.change_presence(status = discord.Status.do_not_disturb, activity=game)
        time.sleep(1)
        game = discord.Game("with Doggo Bot")
        await bot.change_presence(status = discord.Status.online, activity=game)
        
    await bot.process_commands(message)


@tasks.loop(seconds=1)
async def checkTime():
    current_time = datetime.datetime.now()
    if current_time.day == 7 and current_time.hour == 22 and current_time.minute == 0 and current_time.second == 0:
        print(f"The time is {current_time} and the day is Saturday")
        friday_event_guild = await bot.fetch_guild(837209189281038347) # Gets the guild
        event_role = friday_event_guild.get_role(840805963622645761) # Gets the role
        ping_message = event_role.mention # Fetches the ping string that the bot can send.
        event_channel = bot.get_channel(840812002497658911)
        await event_channel.send(f"The Friday Event has been started! {ping_message}")



@bot.event
async def on_ready():
    """What the bot will do here is read over user_ids.txt and then append each id
    into listWithUserIDs so as to keep the list filled with whatever was inside it before.
    It'll then set playing status and start the loop of giving cats every 45 minutes."""

    game = discord.Game("with a ball of yarn")
    await bot.change_presence(status=discord.Status.online,activity=game)

    print("You are running a DEV version of the bot. This bot has no list related commands.")
    checkTime.start()

bot.run('ODAyNjEyNjIxODQ5MDAyMDEy.YAxxQA.VN0TONoU53MQjYL1Purm9rmMNlw')
