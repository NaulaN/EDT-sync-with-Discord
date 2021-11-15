import datetime

from discord import utils,Embed
from discord.ext import commands
from discord.ext.tasks import loop

from scraping import Scraping


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scraping = Scraping(bot.configFile["USERNAME"], bot.configFile["PASSWORD"])
        self.time = .0

    @loop(seconds=30)
    async def updateClock(self):
        self.time = float(f"{datetime.datetime.now().hour}.{datetime.datetime.now().minute}")

    @loop(hours=24)
    async def updateEDT(self):
        self.scraping.getEDT()

    @loop(minutes=1)
    async def sendEDT(self):
        channel = utils.get(self.bot.guilds[0].channels, id=909506071905857597)
        try:
            self.scraping.edt[self.time-.30]
        except KeyError:
            pass
        else:
            # TODO Faire les titres pour chaque jours de la semaine
            days = {0: "Lundi",1: "Mardi",2: "Mercredi"}
            embed = Embed(title=days[0])
            # TODO Mettre au propre les messages dans le Embed
            embed.add_field(name="Heure:",value=f"{self.time}h")
            embed.add_field(name="Prof:",value=self.scraping.edt[self.time - .30][0])
            embed.add_field(name="Cours:",value=self.scraping.edt[self.time - .30][1])
            embed.add_field(name="Salle:",value=self.scraping.edt[self.time - .30][2])
            await channel.send(embed=embed)

