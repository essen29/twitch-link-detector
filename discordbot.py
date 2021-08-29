import discord
import szukaczurl
import twitchrequest
import csv

client = discord.Client()

discord_channel_id = 1234567890 #insert discord channel id here (int)
bot_id = 1234567890 #insert bot discord id (int)

@client.event
async def on_ready():
    print('Discord bot is ready')

#sending a discord private message to the user who reacted to a message
@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(discord_channel_id) 
    message = await channel.fetch_message(payload.message_id)
    if message.author.id == bot_id and payload.user_id != bot_id and payload.emoji.name == '\N{THUMBS UP SIGN}':
        user = await client.fetch_user(payload.user_id)
        split = message.content.split()
        sender = split[5]
        streamer = split[1]
        since_when = twitchrequest.since_when_follow(twitchrequest.get_user_id(sender),twitchrequest.get_user_id(streamer))
        created = twitchrequest.when_created(sender)
        with open('baza.csv', 'r',newline='') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                if row[0] == sender:
                    number = row[1]
        await user.send(f'---------------------------------------------\nInformacje o {sender}:\nKonto utworzone: {created}\nFollowuje {streamer} od: {since_when}\nWysłał na kanale wiadomości: {number}\n---------------------------------------------')

#sending a message to a discord channel and reacting to it
async def linkimaster(message):
    channel = client.get_channel(discord_channel_id)
    emoji = '\N{THUMBS UP SIGN}'
    if message.echo:
        return
    try:
        msg = await channel.send(f'Channel: {message.channel.name}\n{szukaczurl.Find(message.content)[0]} wyslane przez {message.author.name}')
        await msg.add_reaction(emoji)
    except:
        pass