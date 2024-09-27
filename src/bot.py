from datetime import datetime

import discord
from discord.ext import commands

from core.ansihelp import AnsiHelp
from core.config import VERSION
from core.cogmanager import cogs_manager

"""
The main Client file.
bot 'globals' go into Client.__init__() if they need to be used across commands.
"""

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True


class sakaClient(commands.Bot):
    def __init__(self, cogs: list, secrets: dict, prefix: str):
        super().__init__(
            command_prefix=prefix,
            case_insensitive=True,
            intents=intents,
            help_command=AnsiHelp(),
        )
        self.secrets = secrets
        self.uptime = datetime.now()
        self._version = VERSION
        self._cogs = cogs

    async def on_ready(self):
        # This could probably be prettied up with some f string formatting
        print(
            f"Username: {self.user} | {discord.__version__=}\nGuilds: {len(self.guilds)} | Users: {len(self.users)}|Prefix: {self.command_prefix}"
        )
        # What an invite link holy
        # Authorises both the bot AND the slash commands
        # Note that this prints AFTER cogs get loaded.
        print(
            f"Invite Link: https://discord.com/api/oauth2/authorize?client_id={self.user.id}&permissions=52288&scope=bot%20applications.commands"
        )

    async def startup(self):
        """Sync application commands"""
        await self.wait_until_ready()
        await self.tree.sync()
        print("Ready and Tree Synced")

    async def setup_hook(self):
        """Initialize cogs"""

        # Cogs loader
        await cogs_manager(self, "load", self._cogs)
        print("Cogs all loaded")
        # Sync application commands & show logging informations
        self.loop.create_task(self.startup())
