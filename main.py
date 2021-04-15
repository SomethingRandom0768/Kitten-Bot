# Discord for utilizing discord's api, time for waiting related functions, asyncpraw to access reddit posts,  random to create a sense of suspense, and importing commands from discord.ext to create
# a bot.
import discord
import time
import asyncpraw
import random
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

fileWithIDs = 'user_ids.txt'

# Accessing Reddit's API, this stuff is supposed to be secret.
reddit = asyncpraw.Reddit(client_id=(#INSERTCLIENTID,
client_secret=(#INSERTCLIENTSECRET, 
user_agent=#INSERTUSERAGENT

# This is for the list of individuals in the list to receive kitty images.
listWithUserIDs = []

list_of_commands = {
    'announcement': "[Command reserved for SomethingRandom] If SomethingRandom finds something worthy to send all of the people in the list, he'll send it using this command!",
    'getmultiplekitties [insert number]':"One kitty isn't enough? You can ask for more!",   
	'getsinglekitty':'returns a kitty pic or gif!',
    'help': 'Just sends a giant list of all the commands if you need to read them without their descriptions!',
    'joinlist':"allows you to join the folks who'll get a kitty every 45 minutes!",
    'joinlistmultiple [insert IDs with spaces in between]': "allows you to add multiple folks into the list provided you know their user IDs",
    'leavelist':"allows you to leave the list on your own",
    'petbot':"Feel like petting the bot? Do so with this command!",
    'pokeyourself':"Was originally a test function, now is just used to poke yourself if you feel like it",
    'postcommands': "You used this command to read this! Lists out all of kitten bot's commands with a description",
    'postlist':"posts the people in the list of people, use it to make sure you're in it!",
    'resetlist':"[Command reserved for SomethingRandom] Used to reset the list for testing purposes.",
    'say': "If you'd like to speak as the kitten bot, this the command to do it with (Note: You have to delete your own message using this command for full effect",
    "sendkittenstochina": "Joke command to send all of Kitten Bot's siblings to China"  
}


@bot.command()
# This command is used to obtain a single kitten gif or image by utilizing PRAW to retrieve a url.
# r/kittengifs and r/kittens are privated at the moment
async def getsinglekitty(ctx):
    randomNumber = random.randint(1, 4)
    if randomNumber == 1:
        subreddit = await reddit.subreddit("IllegallySmolCats")
#    elif randomNumber == 2:
#        subreddit = await reddit.subreddit("kittengifs")
    elif randomNumber == 2:
        subreddit = await reddit.subreddit("Blep")
    elif randomNumber == 3:
        subreddit = await reddit.subreddit('cats')
#    else:
#        subreddit = await reddit.subreddit("kittens")

    submission = await subreddit.random()
    await ctx.channel.send("Obtaining submission")
	
    while 'v.redd.it' in submission.url or 'gallery' in submission.url:
        print(submission.url)
        await ctx.channel.send("This URL doesn't work right :( trying again",
                               delete_after=2)
        submission = await subreddit.random()
        time.sleep(2)
    else:
        await ctx.channel.send(submission.url)


@bot.command()
# Command to ask for multiple cats, limit is 15
async def getmultiplekitties(ctx, number):
    if int(number) > 15:
        await ctx.send("That's too many! Please do fewer than 16 :( it makes me tired.")
    else:
        number = int(number)

    for i in range(0, number):
        randomNumber = random.randint(1, 3)

        if randomNumber == 1:
            subreddit = await reddit.subreddit("IllegallySmolCats")
#        elif randomNumber == 2:
#            subreddit = await reddit.subreddit("kittengifs")
        elif randomNumber == 2:
            subreddit = await reddit.subreddit("Blep")
        elif randomNumber == 3:
            subreddit = await reddit.subreddit('cats')
        
           # subreddit = await reddit.subreddit("kittens")

        submission = await subreddit.random()
        await ctx.channel.send(f"Obtaining submission ({i+1} of {number})")
        time.sleep(2)

        while 'v.redd.it' in submission.url or 'gallery' in submission.url or 'youtu.be' in submission.url:
            print(submission.url)
            await ctx.channel.send(
                "This URL doesn't work right :( trying again", delete_after=2)
            submission = await subreddit.random()
        else:
            await ctx.channel.send(submission.url)

    await ctx.channel.send(f"I'm ready again! ^-^")


@bot.command()
# Command to join the list for kittens
async def joinlist(ctx): # A guy named indra in the python discord is the reason this command works. Adds the command user to listWithUserIDs
    if ctx.author.id in listWithUserIDs:
        await ctx.channel.send("Wait a minute! You're already in the list :O")
    else:
        with open(fileWithIDs, 'a') as file_object: # Add to the txt file
                file_object.write( f"{ ctx.author.id }\n")
        listWithUserIDs.append(ctx.author.id)

        await ctx.channel.send(f"{ctx.author.name}, you have been added to the list! :D (NOTE: Make sure your privacy settings allow DMs from both the bot and the server you use this command in otherwise the bot will break!") 
        # Sends a message to let them know they've been added.


@bot.command()
 # Command to add in multiple user IDs with a tuple
async def joinlistmultiple(ctx, *user_ids_to_enter):
    for id in user_ids_to_enter: # This for loop just adds them.
        user = await bot.fetch_user(int(id))
        if int(id) in listWithUserIDs:
            await user.send(f"{user.display_name} is already in the list! .-. ")
            print(user_ids_to_enter)
        else:
            try:
                await user.send(f"This is to let you know you've been added into the list! :D If you would like to leave, be sure to use !leavelist")
                listWithUserIDs.append(int(id)) # Adds the ID to the list
                with open(fileWithIDs, 'a') as file_object: # Appends to the txt file
                    file_object.write( f"{ id }\n")
            except discord.Forbidden:
                await ctx.channel.send(f"Either they don't share a server with me, or I'm blocked by them :( I can't add {user.display_name}")
        


@bot.command()
async def leavelist(ctx):
    # Removes the command user from both the list and user_ids.txt, works by removing the user from the list, empties the entire txt file, then appends whoever is left in the 
    if ctx.author.id in listWithUserIDs:
        listWithUserIDs.remove(ctx.author.id)
        await ctx.author.send(f"This is to let you know you've been removed from the list! :D Hope you enjoyed the kitties and I hope to see you again soon! ^_^ ")

        with open('user_ids.txt', 'w') as file_object: # Resets the file
            file_object.write('')

        for id in listWithUserIDs:
            with open(fileWithIDs, 'a') as file_object: # Adds everyone else who is still in the file.
                file_object.write( f"{ id }\n")
    else:
        await ctx.send(f" {await bot.fetch_user(ctx.author.id)} isn't in the list!")

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
    command_list = ''
    for command_name, command_desc in list_of_commands.items():
        command_list += command_name + " : " + command_desc + "\n"
    await ctx.channel.send(command_list)


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
    else:
        await ctx.channel.send(messagetosend)
        await ctx.message.delete()

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
async def resetlist(ctx):
# Completely erases the entire user_ids.txt
    if ctx.author.id == 265596926857183252:      
        with open('user_ids.txt', 'w') as file_object:
            file_object.write('')
    else:
        await ctx.channel.send("You do not have access to this command.")

@bot.command()
async def listservers(ctx):
    # Lists the names of servers that Kitten Bot is in.
    if ctx.author.id == 265596926857183252:      
        server_list = ' '
        for server in bot.guilds:
            server_list += f"+ {server.name}\n"  
        await ctx.channel.send(server_list)
    else:
        await ctx.channel.send("You do not have access to this command.")	

# Tasks
@tasks.loop(minutes=60)
async def randomkittens(): # This task gives folks in the list a random kitten image every 60 minutes.
    for user_id in listWithUserIDs: 
        user = await bot.fetch_user(user_id)

        randomNumber = random.randint(1, 3)
        if randomNumber == 1:
            subreddit = await reddit.subreddit("IllegallySmolCats")
#        elif randomNumber == 2:
#            subreddit = await reddit.subreddit("kittengifs")
        elif randomNumber == 2:
            subreddit = await reddit.subreddit("Blep")
        elif randomNumber == 3:
            subreddit = await reddit.subreddit('cats')
       # else:
           # subreddit = await reddit.subreddit("kittens")


        submission = await subreddit.random()

        while 'v.redd.it' in submission.url or 'gallery' in submission.url or 'youtu.be' in submission.url or 'comments' in submission.url:
            submission = await subreddit.random()
        else:
            try:
                await user.send("Because you've been patient and a good person, have a kitty! ^-^")
                await user.send(submission.url)
                print(f"{user.display_name} has been sent a picture.")
	
            except discord.Forbidden:
                owner = await bot.fetch_user(265596926857183252)	
                await owner.send(f"{user.display_name} has errored. Removing from the list.")
	
                if user.id in listWithUserIDs:
                    listWithUserIDs.remove(user.id)
                    with open('user_ids.txt', 'w') as file_object: # Resets the file
                            file_object.write('')
                    
                    for id in listWithUserIDs:
                        with open(fileWithIDs, 'a') as file_object: # Add to the txt file
                            file_object.write( f"{ id }\n")

@bot.event
# Saying kitten bot will doom you to a breakfast with cookies and milk.
async def on_message(message):
    if "kitten bot" in message.content.lower():
        game = discord.Game(f"I see you, {message.author}")
        await bot.change_presence(status = discord.Status.do_not_disturb, activity=game)
        with open('victims.txt', 'a') as file_object:
            file_object.write(f"{message.author} incurred the wrath of Kitten Bot at {datetime.datetime.now()}\n")
        time.sleep(1)
        game = discord.Game("with Doggo Bot")
        await bot.change_presence(status = discord.Status.online, activity=game)
        
    await bot.process_commands(message)


@bot.event
async def on_ready():
    """What the bot will do here is read over user_ids.txt and then append each id
    into listWithUserIDs so as to keep the list filled with whatever was inside it before.
    It'll then set playing status and start the loop of giving cats every 45 minutes."""

    with open('user_ids.txt') as file_object:
        lines = file_object.readlines()

    joining_users = ''
    for line in lines:
        listWithUserIDs.append(int(line))
        user = await bot.fetch_user( int(line) )
        joining_users += f"{user.display_name}'s ID has been pulled from the txt file.\n"
    print(joining_users)

    print("Loaded IDs")
    game = discord.Game("with Doggo Bot")
    await bot.change_presence(status=discord.Status.online,activity=game)
    await randomkittens.start()

bot.run(#INSERTDISCORDTOKEN)
