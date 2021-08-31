from twitchio.ext import commands
import discordbot
import asyncio
import tokens
import csv

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=tokens.oauth,prefix='!', initial_channels=['channel'])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')

    #using csv file to count messages
    async def event_message(self,message):
        list = []
        is_found = False
        try:
            with open('baza.csv', 'r',newline='') as readFile:
                reader = csv.reader(readFile)
                for row in reader:
                    list.append(row)
                    for field in row:
                        if field == message.author.name:
                            is_found = True
                            list.remove(row)
                            item = row[1]
        except:
            f = open('baza.csv','w')
            f.close()

        if is_found == False:
            list.append([message.author.name,1])
        else:
            list.append([message.author.name,int(item)+1])
                        
        with open('baza.csv','w',newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(list)

        if message.echo:
            return

        await discordbot.linkimaster(message)
        await self.handle_commands(message)   
        

bot = Bot()
loop = asyncio.get_event_loop()
loop.create_task(discordbot.client.start(tokens.discordtoken))
loop.create_task(bot.run())
loop.run_forever()
