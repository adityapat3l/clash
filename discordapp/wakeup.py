import discord
from discordapp.message_parser import read_message
import os

client = discord.Client()

@client.event
async def on_ready():
    print('logged in as')
    print(client.user.name)

@client.event
async def on_message(msg):
    first_word = msg.content.split()[0].lower()
    channel = msg.channel

    # print(first_word)

    if first_word == 'cb!':
        # try:
        data = read_message(msg.content)
        # except Exception as e:
        #     data = 'An Error Occurred. The Minions are on it.'
        #     raise(e)

        await channel.send(data)


if __name__ == '__main__':
    # import argparse
    # parser = argparse.ArgumentParser()
    # # There's no data in redshift before 2010-09-01 so don't bother trying to backfill.
    # parser.add_argument('--start-date', type=command.parse_datetime, default=datetime.datetime(2016, 1, 1))
    # parser.add_argument('--end-date', type=command.parse_datetime, default=datetime.datetime(2019, 5, 1))
    # parser.add_argument('--redshift-slots', type=int, default=2)
    # parser.add_argument('--schema', type=str, default=sqlalchemy_warehouse.DEFAULT_SCHEMA)
    # args = parser.parse_args()
    #
    # schema = args.schema

    discord_key = os.environ["DISCORD_KEY"]
    client.run(discord_key)