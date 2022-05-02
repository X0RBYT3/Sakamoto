from datetime import datetime

import discord
from discord.ext import commands

from core.config import PREFIX

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
        super().__init__(command_prefix=PREFIX, case_insensitive=True)
        self.help_command = MyHelpCommand()
        self.secrets = secrets
        self.uptime = datetime.now()
        self._version = "0.0.1"  # Make this Magic
        for cog in cogs:
            try:
                self.load_extension(f"cogs.{cog}.main")
            except Exception as e:
                exc = f"{type(e).__name__}: {e}"
                print(f"Cog Loading Failed: {cog}\n{exc}")
            else:
                print(f"Cog Loading Successful: {cog}")
        print(f"{len(self.cogs)} Out of {len(cogs)}) Cogs Loaded")
