import json
import discord

from discord.ext import commands

from event import Event


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents().all()
        super(Bot, self).__init__(command_prefix='$',
                                  intents=intents)
        with open("settings.json", "r") as f:
            self.configFile = json.load(f)
        self.add_cog(Event(self))

    async def on_ready(self):
        # TODO Nettoyer...
        print("I'm ready !")


bot = Bot()
bot.run(bot.configFile["TOKEN"])
