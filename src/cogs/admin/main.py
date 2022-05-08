import subprocess
from pathlib import Path

import asyncio
from discord.ext import commands
import discord
import aiohttp

from core.cogmanager import cogs_manager
from cogs.admin.gitpull import check_for_push, pull_and_reload


async def setup(client):
    await client.add_cog(Admin(client))


class Admin(commands.Cog):
    """
    Handles Cog Control / Shutting Down / Git Pulling

    """

    def __init__(self, client: discord.Client):
        self.client = client
        self.last_cog = ""

    @commands.command(name="eb", help="Backs up emojis to local storage")
    @commands.is_owner()
    async def emojiback(self, ctx: commands.Context):
        """
        This is NOT for every day use, it's something I use for my personal server
        And figured it may be handy for someone who stumbles upon this code
        Use with caution homie
        """
        backup = Path("backup/emojis")
        async with aiohttp.ClientSession() as session:
            for e in ctx.guild.emojis:
                url = e.url
                name = url[url.rfind("/") + 1 :]
                async with session.get(url) as resp:
                    if resp.status == 200:
                        with open(backup / name, "wb+") as file:
                            file.write(await resp.read())

    @commands.command(
        name="shutdown", help="Shuts down Sakamoto. Used only for emergencies"
    )
    @commands.bot_has_permissions(send_messages=True)
    @commands.is_owner()
    async def _shutdown(self, ctx: commands.Context):
        """
        Emergency usage only.
        """
        await ctx.send("Shutting down.")
        await self.client.close()

    @commands.command(name="load")
    @commands.bot_has_permissions(send_messages=True)
    @commands.is_owner()
    async def _load(self, ctx, *, cog: str):
        """Command which loads a Module.
        eg: !load admin"""
        if cog.lower() == "last" or cog == "~":
            if self.last_cog != "":
                cog = self.last_cog
            else:
                await ctx.send(f"**`ERROR:`** No Last Cog")
        r = await cogs_manager(self.client, "load", [cog])
        await ctx.send(r)
        self.last_cog = cog

    @commands.command(name="unload")
    @commands.bot_has_permissions(send_messages=True)
    @commands.is_owner()
    async def _unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        r = await cogs_manager(self.client, "unload", [cog])
        await ctx.send(r)
        self.last_cog = cog

    @commands.command(name="reload")
    @commands.bot_has_permissions(send_messages=True)
    @commands.is_owner()
    async def _reload_cog(self, ctx: commands.Context, cog: str):
        """Unload a cog."""
        if cog.lower() == "last" or cog == "~":
            if self.last_cog != "":
                cog = self.last_cog
            else:
                await ctx.send(f"**`ERROR:`** No Last Cog")
        r = await cogs_manager(self.client, "reload", [cog])
        await ctx.send(r)
        self.last_cog = cog

    @commands.command(name="synctree", aliases=["st"])
    @commands.bot_has_permissions(send_messages=True)
    @commands.is_owner()
    async def _reload_tree(self, ctx: commands.Context, guild_id: str = None):
        """Sync application commands."""
        if guild_id:
            if guild_id == "guild" or guild_id == "~":
                guild_id = ctx.guild.id
            sync_tree = await self.client.tree.sync(guild=discord.Object(id=guild_id))
        else:
            sync_tree = await self.client.tree.sync()
        await ctx.send(f":pinched_fingers: `{len(sync_tree)}` synced!")

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if check_for_push(msg):
            # We think there's a Push to main
            await pull_and_reload(self.client)
