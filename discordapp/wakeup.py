import discord
import asyncio
from discordapp.queries import format_data

client = discord.Client()

@client.event
async def on_ready():
    print('logged in as')
    print(client.user.name)

@client.event
async def on_message(msg):
    first_word = msg.content.split()[0].lower()
    channel = msg.channel

    if first_word == 'pingme':
        # try:
        data = format_data(msg.content, metric_name='dark', player_name='adi', player_tag='#8292J8QV8')
        # except Exception as e:
        #     data = 'An Error Occurred. The Minions are on it.'
        #     raise(e)

        await channel.send(data)


client.run('NTkwMzI1MjMyODUwNTY3MTY4.XQgmzA.cUNwAMqPdPmwP6cWpqsne8hMZh0')