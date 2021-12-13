# Discord for utilizing discord's api, time for waiting related functions, asyncpraw to access reddit posts
# os to access secret variables, random to create a sense of suspense, and importing commands from discord.ext to create
# a bot.

import asyncprawcore
import discord
import datetime
import time
import asyncpraw
import random
import json
import dev.secret_variables as secret_variables
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

fileWithIDs = 'dev/user_ids.txt'

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

# BOT COMMANDS start here

@bot.command()
# This command is used to obtain a single kitten gif or image by utilizing PRAW to retrieve a url.
async def getsinglekitty(ctx):
    # Chooses a random subreddit from listWithSubreddits
    randomSubreddit = random.choice(listOfSubreddits)
    chosenSubreddit = await reddit.subreddit(randomSubreddit)

    submission = await chosenSubreddit.random()
    await ctx.channel.send("Obtaining submission")
	
    while 'v.redd.it' in submission.url or 'gallery' in submission.url or 'youtu.be' in submission.url or 'youtube' in submission.url:
        print(submission.url)
        await ctx.channel.send("This URL doesn't work right :( trying again", delete_after=2)
        submission = await chosenSubreddit.random()
        time.sleep(2)
    else:
        print(submission.url)
        redditLink = "https://www.reddit.com/" + submission.permalink
        messageEmbed = discord.Embed(colour=3447003, title="Here's a cat, just for you! ^-^")
        messageEmbed.add_field(name='Post Information', value=f"This post was created by reddit user {submission.author} which can be found [here]({redditLink})")
        messageEmbed.set_footer(text="If the image/gif/video fails, feel free to click the blue link to see what would've been posted :D")
        messageEmbed.set_image(url=submission.url)
        await ctx.channel.send(embed=messageEmbed)


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
            messageEmbed = discord.Embed(colour=3447003, title=f"Here's a cat, just for you! ^-^ ({i+1} of {number})", footer="If the image/gif/video fails, feel free to click the blue link to see what would've been posted :D")
            messageEmbed.add_field(name='Post Information', value=f"This post was created by reddit user {submission.author} which can be found [here]({redditLink})")
            messageEmbed.set_footer(text="If the image/gif/video fails, feel free to click the blue link to see what would've been posted :D")
            messageEmbed.set_image(url=submission.url)
            await ctx.channel.send(embed=messageEmbed)
            time.sleep(1)


@bot.command()
# Sends a giant kitty.
async def sendbigkitty(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/837418361696288828/837433194055598110/image0.jpg')

@bot.command()
# Command to join the list for kittens
async def joinlist(ctx):  # A guy named indra in the python discord is the reason this command works. Adds the command user to listWithUserIDs
    if ctx.author.id in listWithUserIDs:
        await ctx.channel.send("Wait a minute! You're already in the list :O")
    else:
        with open(fileWithIDs, 'a') as file_object:  # Add to the txt file
            file_object.write(f"{ ctx.author.id }\n")
        listWithUserIDs.append(ctx.author.id)
        await ctx.channel.send(f"{ctx.author.name}, you have been added to the list! :D")
        print(f"{ctx.author.name} has been added to the list")

@bot.command()
# Command to add in multiple user IDs with a tuple
async def joinlistmultiple(ctx, *user_ids_to_enter):
    
    for id in user_ids_to_enter:  # This for loop just adds them.
        user = await bot.fetch_user(int(id))
        if int(id) in listWithUserIDs:
            await user.send(f"{user.display_name} is already in the list! .-. ")
            print(user_ids_to_enter)
        else:
            try:
                await user.send(f"This is to let you know you've been added into the list! :D If you would like to leave, be sure to use !leavelist")
                listWithUserIDs.append(int(id))  # Adds the ID to the list
                with open(fileWithIDs,'a') as file_object:  # Appends to the txt file
                    file_object.write(f"{ id }\n")
            except discord.Forbidden:
                await ctx.channel.send(f"Either they don't share a server with me, or I'm blocked by them :( I can't add {user.display_name}")


@bot.command()
async def leavelist(ctx):
    # Removes the command user from both the list and user_ids.txt, works by removing the user from the list, empties the entire txt file, then appends whoever is left in the
    if ctx.author.id in listWithUserIDs:
        listWithUserIDs.remove(ctx.author.id)
        await ctx.author.send(f"This is to let you know you've been removed from the list! :D Hope you enjoyed the kitties and I hope to see you again soon! ^_^ ")

        with open(fileWithIDs, 'w') as file_object:  # Resets the file
            file_object.write('')

        for id in listWithUserIDs:
            with open(fileWithIDs, 'a') as file_object:  # Adds everyone else who is still in the file.
                file_object.write(f"{ id }\n")
    else:
        await ctx.send(f"{await bot.fetch_user(ctx.author.id)} isn't in the list!")


@bot.command()
# Posts the list of people who have subscribed to getting random kitten images/gifs at random times.
async def postlist(ctx):
    posting_list = ' '
    if len(listWithUserIDs) > 0:
        for individual in listWithUserIDs:
            user = await bot.fetch_user(individual)
            posting_list += "+ " + user.display_name + "\n"
        await ctx.channel.send(posting_list)
    else:
        await ctx.channel.send(f"I don't have a list of people to send kittens to :( I'm sad now.")


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
    await ctx.channel.send(
        f"Mew! {ctx.message.author}, thank you for petting me! ^-^")

@bot.command()
# joke command, not meant to be anything serious
async def sendkittenstochina(ctx):
    await ctx.channel.send(
        f"Mew mew mew!!!! Sending my brothers and sisters to China! ^-^")


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
async def announcement(ctx, *message):
    # Command usable by SomethingRandom (or you if you decide to change it) to send a message to everyone that is currently subscribed to the list
    if ctx.message.author.id == 265596926857183252:
        for user_id in listWithUserIDs:
            user = await bot.fetch_user(user_id)
            messagetosend = "BOT ANNOUNCEMENT:"
            for word in message:
                messagetosend += " " + word
            await user.send(messagetosend)
            print(f"Message sent to {user}")
    else:
        await ctx.channel.send("You do not have access to this command.")


@bot.command()
async def pokeyourself(ctx):
    # Why not poke yourself? Sometimes, it might be all that you need.
    await ctx.author.send("You have poked yourself! ^_^")

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


@bot.command()
async def resetlist(ctx):
    # Completely erases the entire user_ids.txt
    if ctx.author.id == 265596926857183252:
        with open(fileWithIDs, 'w') as file_object:
            file_object.write('')
        listWithUserIDs.clear()
        print("The list has been reset!")
        await ctx.channel.send("The list has been reset!")
    else:
        await ctx.channel.send("You do not have access to this command.")


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

@tasks.loop(seconds=1)
async def checkTime():
    current_time = datetime.datetime.now()
    if (current_time.minute == 0 and current_time.second == 0) or (current_time.minute == 30 and current_time.second ==0):
        for user_id in listWithUserIDs:
            user = await bot.fetch_user(user_id)
            subreddit = await reddit.subreddit(random.choice(listOfSubreddits))
            
            try:
                submission = await subreddit.random()
            except asyncprawcore.exceptions.Forbidden as error:
                with open('crash_log.txt', 'w') as file_object: # Write to the crash log if this is the case.
                    file_object.write(f"{error} + \nSubreddit crashing name: {subreddit.display_name}")
                    print("Encountered a Forbidden error!")
                    owner = await bot.fetch_user(owner_id)
                    await owner.send( f"{subreddit.display_name} has crashed!")
                        
            try:
                redditLink = "https://www.reddit.com/" + submission.permalink
                messageEmbed = discord.Embed(colour=3447003, title=f"Here's your kitty!")
                messageEmbed.add_field(name='Post Information', value=f"This post was created by reddit user {submission.author} which can be found [here]({redditLink})")
                messageEmbed.set_footer(text="If the image/gif/video fails, feel free to click the blue link to see what would've been posted :D")
                messageEmbed.set_image(url=submission.url)
                
                await user.send(embed=messageEmbed)

                print(f"{user.display_name} has been sent a picture.")

            except discord.Forbidden:
                owner = await bot.fetch_user(265596926857183252)
                await owner.send(f"{user.display_name} has errored. Removing from the list.")

                if user.id in listWithUserIDs:
                    listWithUserIDs.remove(user.id)
                    with open(fileWithIDs,'w') as file_object:  # Resets the file
                        file_object.write('')

                    for id in listWithUserIDs:
                        with open(fileWithIDs,'a') as file_object:  # Add everyone left in the list to the txt file
                            file_object.write(f"{ id }\n")
                    
# Bot events start here

@bot.event
# Saying kitten bot will doom you to a breakfast with cookies and milk.
async def on_message(message):
    if "kitten bot" in message.content.lower():
        game = discord.Game(f"I see you, {message.author}")
        await bot.change_presence(status=discord.Status.do_not_disturb, activity=game)
        with open('dev/victims.txt', 'a') as file_object:
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

    with open(fileWithIDs) as file_object:
        lines = file_object.readlines()

    joining_users = ''
    for line in lines:
        listWithUserIDs.append(int(line))
        user = await bot.fetch_user( int(line) )
        joining_users += f"{user.display_name}'s ID has been pulled from the txt file.\n"
    print(joining_users)

    print("Loaded all IDs")

    game = discord.Game("with a ball of yarn, mew!")
    await bot.change_presence(status=discord.Status.online, activity=game)

    await checkTime.start()

bot.run(secret_variables.discord_token)