# Discord for utilizing discord's api, time for waiting related functions, asyncpraw to access reddit posts
# os to access secret variables, random to create a sense of suspense, and importing commands from discord.ext to create
# a bot.
import asyncprawcore
from discord import * 
import datetime
import time
import asyncpraw
import random
import json
import secret_variables as secret_variables
from discord.ext import commands, tasks


#######################################################
#                                                     #
#    DEV MODE OF BOT, DOESN'T HAVE LIST FUNCTIONS     #
#    ONLY USE WHEN CREATING NEW FUNCTIONS             #
#                                                     #
#                                                     #
#                                                     #
#                                                     # 
#######################################################

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

fileWithIDs = 'user_ids.txt'

# Accessing Reddit's API, this stuff is supposed to be secret.
reddit = asyncpraw.Reddit(
    client_id=(secret_variables.client_ID),
    client_secret=(secret_variables.client_secret),
    user_agent=(secret_variables.user_agent)
)

# This is for the list of individuals in the list to receive kitty images.
listWithUserIDs = []

# List of subreddits to choose from
listOfSubreddits = ['IllegallySmolCats', 'cats', 'Blep', 'kitten_gifs']

# Counter to prevent people from spamming amogus command.
amogus_counter = 0

# SomethingRandom's ID.

owner_id = 265596926857183252

# Bot's main function is here.

def createEmbed(submission):
     redditLink = "https://www.reddit.com/" + submission.permalink
     messageEmbed = discord.Embed(colour=3447003, title="Here's a cat, just for you! ^-^")
     messageEmbed.add_field(name='Post Information', value=f"This post was created by reddit user {submission.author} which can be found [here]({redditLink})")
     messageEmbed.set_footer(text="If the image/gif/video fails, feel free to click the blue link to see what would've been posted :D")
     messageEmbed.set_image(url=submission.url)
     return messageEmbed


# BOT COMMANDS start here

@bot.command()
# This command is used to obtain a single kitten gif or image by utilizing PRAW to retrieve a url.
async def getsinglekitty(ctx):
    # Chooses a random subreddit from listWithSubreddits, uses createEmbed and then sends it to the individual who asked for it.
    randomSubreddit = random.choice(listOfSubreddits)
    chosenSubreddit = await reddit.subreddit(randomSubreddit)
    submission = await chosenSubreddit.random()	
    single_kitty_embed = createEmbed(submission)
    await ctx.channel.send(embed=single_kitty_embed)



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
        multiple_kitty_embed = createEmbed(submission)
        await ctx.channel.send(embed=multiple_kitty_embed)

@bot.command()
# Sends a giant kitty.
async def sendbigkitty(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/837418361696288828/837433194055598110/image0.jpg')


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
async def leaveserver(ctx, server_id):
    # Removes kitten bot from the server id given
    if ctx.author.id == owner_id:
        server_to_leave = bot.get_guild(int(server_id))
        await server_to_leave.leave()
        owner = await bot.fetch_user(owner_id)
        await owner.send(f"Kitten Bot has left from {server_to_leave.name} (ID: {server_to_leave.id} )")
    else:
        await ctx.send("You do not have access to this command.")

@bot.command()
async def listservers(ctx):
    # Lists the names of servers that Kitten Bot is in.
    if ctx.author.id == 265596926857183252:
        server_list = ' '
        for server in bot.guilds:
            server_list += f"+ {server.name} (ID: {server.id}) \n"
        await ctx.channel.send(server_list)
    else:
        await ctx.channel.send("You do not have access to this command.")

                    
# Bot events start here

@bot.event
# Saying kitten bot will doom you to a breakfast with cookies and milk.
async def on_message(message):
    if "kitten bot" in message.content.lower():
        game = discord.Game(f"I see you, {message.author}")
        await bot.change_presence(status=discord.Status.do_not_disturb, activity=game)
        with open('victims.txt', 'a') as file_object:
            file_object.write(f"{message.author} incurred the wrath of Kitten Bot at {datetime.datetime.now()}\n")
        time.sleep(1)
        game = discord.Game("with a ball of yarn, mew!")
        await bot.change_presence(status=discord.Status.online, activity=game)
    await bot.process_commands(message)

@bot.event
async def on_ready():
    """What the bot will do here is read over user_ids.txt and then append each id
    into listWithUserIDs so as to keep the list filled with whatever was inside it before.
    It'll then set playing status and start the loop of giving cats every 45 minutes."""

    print("Dev Mode is on")
    game = discord.Game("with a ball of yarn, mew!")
    await bot.change_presence(status=discord.Status.idle, activity=game)

bot.run(secret_variables.discord_token)