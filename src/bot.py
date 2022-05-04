from datetime import datetime

import discord
from discord.ext import commands

from core.config import PREFIX, VERSION
from core.cogmanager import cogs_manager

"""
The main Client file.
bot 'globals' go into Client.__init__() if they need to be used across commands.
TODO: Logging
"""


class MyHelpCommand(commands.MinimalHelpCommand):
    """Help Command courtesy of Flobot"""

    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description="")
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)


class sakaClient(commands.Bot):
    def __init__(self, cogs: list, secrets: dict):
        super().__init__(
            command_prefix=PREFIX, case_insensitive=True, intents=discord.Intents.all()
        )
        self.help_command = MyHelpCommand()
        self.secrets = secrets
        self.uptime = datetime.now()
        self._version = VERSION
        self._cogs = cogs

    async def on_ready(self):
        print(
            f"Logged as: {self.user} | discord.py: {discord.__version__}\nGuilds: {len(self.guilds)} Users: {len(self.users)}"
        )

    async def startup(self):
        """Sync application commands"""
        await self.wait_until_ready()
        await self.tree.sync()
        print("Synced.")

    async def setup_hook(self):
        """Initialize cogs"""

        # Cogs loader
        await cogs_manager(self, "load", self._cogs)
        print("Cogs all loaded")
        # Sync application commands & show logging informations
        self.loop.create_task(self.startup())
