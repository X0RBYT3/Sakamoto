import discord
from discord.ext import commands
from cogs.info.views import get_client_uptime, gen_about_embed, AboutView, GithubView
import requests
import time
from datetime import datetime


async def setup(client):
    await client.add_cog(Info(client))


class Info(commands.Cog):
    """
    Provides some neat stats on the Bot.

    PING: Measures ping
    UPTIME: Measures uptime
    ABOUT: Gives nice data on memory usage and the such.

    """

    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(
        name="about", usage="!about", aliases=["info", "sakamoto", "author"]
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True)
    async def _about(self, ctx: commands.Context):
        """
        Gives you info about Sakamoto
        """
        e = gen_about_embed(self.client)
        await ctx.send(embed=e, view=AboutView(ctx))

    @commands.hybrid_command(name="git", usage="!github", aliases=["source", "github"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True)
    async def _git(self, ctx: commands.Context):
        """
        Links to the Github repo.
        """
        # Really should be moved to another file.
        url = "https://api.github.com/repos/Nekurone/Sakamoto?page=$i&per_page=100"
        r = requests.get(url).json()
        stargazers = r["stargazers_count"]
        issues = r["open_issues"]
        desc = r["description"]
        embed = discord.Embed(
            title="Sakamoto Github!",
            url="https://github.com/Nekurone/Sakamoto",
            description=desc,
            color=0xB81E61,
        )
        embed.add_field(name="⭐ Stargazers", value=stargazers, inline=True)
        embed.add_field(name="😰 Issues", value=issues, inline=True)
        await ctx.send(embed=embed, view=GithubView())

    @commands.hybrid_command(name="ping", description="Ping the bot.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True)
    async def ping(self, ctx: commands.Context):
        """Show latency in seconds & milliseconds"""
        before = time.monotonic()
        message = await ctx.send(":ping_pong: Pong !")
        ping = (time.monotonic() - before) * 1000
        await message.edit(
            content=f":ping_pong: Pong ! in `{float(round(ping/1000.0,3))}s` ||{int(ping)}ms||"
        )

    @commands.hybrid_command(name="uptime", usage="!uptime")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True)
    async def _uptime(self, ctx: commands.Context):
        """
        Gets the time since the bot first connected to Discord
        """
        em = discord.Embed(
            title="Local time",
            description=str(datetime.now())[:-7],
            colour=0x14E818,
        )
        em.set_author(
            name=self.client.user.name, icon_url="https://i.imgur.com/3VPTx2K.gif"
        )
        em.add_field(
            name="Current uptime",
            value=get_client_uptime(self.client.uptime, brief=True),
            inline=True,
        )
        em.add_field(name="Start time", value=str(self.client.uptime)[:-7], inline=True)
        em.set_footer(
            text="Made with 💖 by Florence",
            icon_url="https://media.giphy.com/media/qjPD3Me0OCvFC/giphy.gif",
        )
        await ctx.send(embed=em)
