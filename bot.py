#bot.py
import os
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
from twitterAccount import TwitterAccount

# collects environment variables / secrets & constants
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD = os.getenv('DISCORD_GUILD')
SPORTS_CHANNEL = os.getenv('SPORTS_CHANNEL')
secondsInMin = 60

# discord bot setup
intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.watching, name="Headlines")
bot = commands.Bot(command_prefix='!', intents=intents, activity=activity, status=discord.Status.idle)

# accounts list to store all TwitterAccount objects
accounts = []

# List Twitter Accounts to be tracked below internally
# accounts.append(TwitterAccount('adamschefter', 5))
# accounts.append(TwitterAccount('wojespn', 5))

# function that pings all twitter accounts
async def ping_headline():
    # waits until bot is ready
    await bot.wait_until_ready()
    counter = 0
    channel = bot.get_channel(int(SPORTS_CHANNEL))
    while not bot.is_closed():
        # for debugging purposes, counter to keep track of loop iterations
        counter += 1
        # appends all account tweets to a tweets list
        tweets = []
        for account in accounts:
            tweets.append(account.getTweets())
        # sends all tweets in the tweets list to the appropriate discord channel
        for accountTweets in tweets:
            for tweet in accountTweets:
                await channel.send(tweet)
        # for debugging purposes, below line prints the value of the counter variable
        # print(counter)
        await asyncio.sleep(5*secondsInMin) 

@bot.event
async def on_ready():
    # checks bot connectivity
    for guild in bot.guilds:
        if guild.name == DISCORD_GUILD:
            break
    print(
        f'{bot.user} has conected to Discord!'
        f'{guild.name} (id:{guild.id}) \n'
    )
    
    # prints connection in sports channel
    channel = bot.get_channel(int(SPORTS_CHANNEL))
    await channel.send('HeadlinerBot has connected!')

    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('----------')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members: \n - {members}')

    # pings twitter headlines indefinitely
    bot.loop.create_task(ping_headline())

# called by !accounts; prints a list of all twitter accounts currently being tracked
@bot.command(name='accounts', help='Lists All Accounts to Ping. ')
async def test(ctx):
    # prevents recursive calls
    if ctx.message.author == bot.user:
        return
    # appends all account names to a list
    response = []
    for account in accounts:
        response.append(account.username)
    # prints account names list in the appropriate channel
    await ctx.message.channel.send(response)

# called by !shutdown;  shuts the bot down
@bot.command(name='shutdown', help='Shuts Down HeadlinerBot :(')
@commands.has_permissions(administrator=True)
async def close(ctx):
    await ctx.message.channel.send('HeadlinerBot shutdown!')
    await bot.close()
    print("Bot closed")

@bot.command(name='addAccount', help='Adds an Account to Ping.')
async def add(ctx, accountName: str, freq: int):
    # prevents recursive calls
    if ctx.message.author == bot.user:
        return
    accounts.append(TwitterAccount(accountName, freq))
    response = accountName + ' sucessfully added!'
    await ctx.message.channel.send(response)  


@bot.command(name='deleteAccount', help='Deletes an Account.')
async def add(ctx, accountName: str):
    # prevents recursive calls
    if ctx.message.author == bot.user:
        return

    accountFound = False
    for account in accounts:
        if account.username == accountName:   
            accountFound = True  
            accounts.remove(account)
            response = accountName + ' sucessfully deleted!'
    if not accountFound:
        response = accountName + ' does not exist in system. '
    await ctx.message.channel.send(response)  

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("That command wasn't found! Sorry :(")
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.send("That command has missing arguments! Sorry :(")

bot.run(DISCORD_TOKEN)

