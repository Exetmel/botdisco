import discord
from discord.ext import tasks

TOKEN = 'BOT TOKEN HERE'
GUILD = 'GUILD NAME HERE'

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@tasks.loop(seconds=10)
async def auto_send(channel : discord.TextChannel):
    await channel.send('Test message')

@client.event
async def on_ready():

    if not auto_send.is_running():
        channel = await client.fetch_channel('channel id (as int)')
        auto_send.start(channel)

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} has successfully connected to the following guild(s):\n'
        f'{guild.name}(id: {guild.id})'
    )

    await client.change_presence(
        activity=discord.Activity(name='anything', type=discord.ActivityType.playing)
    )

client.run(TOKEN)