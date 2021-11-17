import datetime

from discord import utils,Embed,File
from discord.ext import commands
from discord.ext.tasks import loop

from scraping import Scraping


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scraping = Scraping(bot.configFile["USERNAME"], bot.configFile["PASSWORD"])
        self.hour = 0
        self.minute = 0

    @commands.Cog.listener()
    async def on_ready(self):
        self.updateClock.start()
        self.sendEDT.start()

    @loop(seconds=30)
    async def updateClock(self):
        self.hour = int(datetime.datetime.now().hour)
        self.minute = int(datetime.datetime.now().minute)

        if self.hour == 0 and self.minute == 0:
            self.scraping.getEDT()

    @loop(seconds=30)
    async def sendEDT(self):
        channel = utils.get(self.bot.guilds[0].channels, id=909506071905857597)
        hour = self.hour
        minute = self.minute+30

        if minute >= 60:
            hour += 1
            minute -= 60
        time = float(f"{hour}.{minute}")
        print(time)

        moreInfo = f"📆 On est le {datetime.date.today().day}/{datetime.date.today().month}/{datetime.date.today().year}\n🕔 Il est {int(time)}h{int(time-int(time))}"
        infoSection = ["👨‍🏫👩‍🏫 Prof: ","📖 Cours: ","🚪 Salle: "]
        days = {0: "Lundi",1: "Mardi",2: "Mercredi",3: "Jeudi",4: "Vendredi"}

        try:
            self.scraping.edt[time]
        except KeyError: pass
        else:
            dayWeek = self.scraping.getWhatDayWeek()
            embed = Embed(title=f"📅 {days[dayWeek if dayWeek not in [5,6] else 0]}",
                          description=moreInfo)
            # TODO Mettre les noms des enseignant(e)s au complet au lieux des aliases
            embed.add_field(name="⌚ Heure:",
                            value=f"{time}h", inline=True)
            for n, subtitle in enumerate(["👨‍🏫👩‍🏫 Prof: ", "📖 Cours: ", "🚪 Salle: "]):
                embed.add_field(name=subtitle,
                                value=self.scraping.edt[time][n], inline=False)
            await channel.send(content="@everyone",embed=embed)
