import subprocess

import asyncio
from discord.ext import commands
import discord

from cogs.admin.gitpull import check_for_push, pull_and_reload


def setup(client):
    client.add_cog(AdminCog(client))


def mod_check(ctx: commands.Context) -> bool:
    """
    We can assume anyone with manage_messages is a mod.

    # TODO: Change this for when bot goes public
    """
    if ctx.author.guild_permissions.manage_messages:
        return True
    return False


class AdminCog(commands.Cog):
    """
    Handles Cog Control / Shutting Down / Git Pulling

    """

    def __init__(self, client: discord.Client):
        self.client = client
        self.last_cog = ""

    @commands.command(
        name="shutdown", help="Shuts down Sakamoto. Used only for emergencies"
    )
    @commands.check(mod_check)
    async def _shutdown(self, ctx: commands.Context):
        """
        Emergency usage only.
        """
        await ctx.send("Shutting down, I love you.")
        await self.client.close()

    @commands.command(name="load")
    @commands.check(mod_check)
    async def _load(self, ctx, *, cog: str):
        """Command which loads a Module.
        eg: !reload admin"""
        try:
            if cog.lower() == "last":
                if self.last_cog != "":
                    cog = self.last_cog
                else:
                    await ctx.send(f"**`ERROR:`** No Last Cog")
            self.client.load_extension(f"Cogs.{cog}.main")
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("**`SUCCESS`**\N{PISTOL}")
        self.last_cog = cog

    @commands.command(name="unload")
    @commands.check(mod_check)
    async def _unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            self.client.unload_extension(f"cogs.{cog}.main")
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("**`SUCCESS`**\N{PISTOL}")
            # this is inside the try:except loop
            # because 9/10 the cog will unload fine
            self.last_cog = cog

    @commands.command(name="reload")
    @commands.check(mod_check)
    async def _reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            if cog.lower() == "last":
                if self.last_cog != "":
                    cog = self.last_cog
                else:
                    await ctx.send(f"**`ERROR:`** No Last Cog")
            self.client.unload_extension(f"cogs.{cog}.main")
            self.client.load_extension(f"cogs.{cog}.main")
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("**`SUCCESS`**\N{PISTOL}")
        self.last_cog = cog

    @commands.command(name="test")
    async def _test(self, ctx):
        await pull_and_reload(self.client)

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if check_for_push(msg):
            # We think there's a Push to main
            await pull_and_reload(self.client)
