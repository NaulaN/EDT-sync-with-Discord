import json

from discord.ext import commands
import discord

from event import Event


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents().all()
        super(Bot, self).__init__(command_prefix='$',
                                  intents=intents)
        with open("settings.json", "r") as f:
            self.configFile = json.load(f)

    async def on_ready(self):
        # TODO Nettoyer...
        event = Event(self)
        self.add_cog(event)
        event.updateEDT.start()
        event.sendEDT.start()
        event.updateClock.start()
        print("I'm ready !")


bot = Bot()
bot.run(bot.configFile["TOKEN"])
