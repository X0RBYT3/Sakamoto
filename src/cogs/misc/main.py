from datetime import datetime, timedelta
import dateutil.parser
import time
import re
import asyncio
from random import randint, choice

import requests

import discord
from discord.app_commands import Choice
from discord.ext import commands
from discord import app_commands
from core.utils.chat_formatter import escape
from cogs.misc.about import (
    AboutView,
    get_client_uptime,
    gen_about_embed,
    PollView,
    ExpiredPoll,
)


async def setup(client):
    await client.add_cog(Misc(client))


class Github(discord.ui.View):
    # Could be moved into another file.
    def __init__(self):
        super().__init__()

        self.add_item(
            discord.ui.Button(
                label="📄 Source code on Github.",
                url="https://github.com/Nekurone/Sakamoto",
            )
        )
        self.add_item(
            discord.ui.Button(
                label="🌟 Become a stargazer! 🌟",
                url="https://github.com/nekurone/Sakamoto/stargazers",
            )
        )


class Misc(commands.Cog):
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
        await ctx.send(embed=embed, view=Github())

    @commands.hybrid_command(name="ping", description="Ping the bot.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True)
    async def ping(self, ctx: commands.Context):
        """Show latency in seconds & milliseconds"""
        before = time.monotonic()
        message = await ctx.send(":ping_pong: Pong !")
        ping = (time.monotonic() - before) * 1000
        await message.edit(
            content=f":ping_pong: Pong ! in `{float(round(ping / 1000.0, 3))}s` ||{int(ping)}ms||"
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

    @commands.hybrid_command(name="poll", aliases=["ynpoll", "pollstart"])
    async def _ynpoll(self, ctx: commands.Context, *, args: str):
        """
        Asks question & then adds checkmark & "x" as reactions.
        Thanks to Spoon for original idea

        Make embed -> Add buttons, when buttons are clicked, add them to list and grey out
        after some user defined time in secs announce result

        """
        to_wait = 30
        question = args
        if args.startswith("-t "):
            try:
                s = args.split(" ")[1]
                to_wait = int(s)    # behaviour note, passing as the only arg `-t 100` will have that be both the time
                question = " ".join(args.split(" ")[2:])  # and the question
            except ValueError or IndexError:
                pass
        to_wait = max(1, min(to_wait, 3600))
        ynpoll_embed = discord.Embed(
            title=f"Poll by {ctx.author}. Expires in {to_wait} seconds.",
            description=f"**Question**: {question}",
            timestamp=ctx.message.created_at,
            color=discord.Color.blurple(),
        )
        poll = PollView()
        message = await ctx.send(embed=ynpoll_embed, view=poll)
        await asyncio.sleep(to_wait)
        ynpoll_embed.title = f"Poll by {ctx.author}. Poll Ended"
        # Send forth the greyed out bits.
        await message.edit(embed=ynpoll_embed, view=ExpiredPoll())
        poll.stop()

        # Generate Score.
        # Easier to write this then copy paste len each time
        yes_l = len(poll.users_yes)
        no_l = len(poll.users_no)

        result_em = discord.Embed(
            title="Placeholder",
            description="Placeholder",
        )
        # There's probably an easier way to write this.
        if yes_l > no_l:
            result = "Yes"
            result_em.color = discord.Color.green()
        elif yes_l < no_l:
            result = "No"
            result_em.color = discord.Color.red()
        else:
            result = "Draw"
            result_em.color = discord.Color.yellow()
        # Emoji time?
        result_em.title = f"And the result is: **{result}**"
        result_em.description = f"{yes_l + no_l} Voted and they voted: {result}"

        # There's defo an easier way to write this in like 2 lines.
        if yes_l == 0:
            yes_s = "Nobody!"
        else:
            yes_s = ", ".join(poll.users_yes)
        if no_l == 0:
            no_s = "Nobody!"
        else:
            no_s = ", ".join(poll.users_no)

        # Emojis in the fields?
        result_em.add_field(name="People who voted Yes", value=yes_s, inline=True)
        result_em.add_field(name="People who voted No", value=no_s, inline=True)
        await ctx.send(embed=result_em)

    @commands.command(usage="<first> <second> [others...]")
    async def choose(self, ctx, *choices) -> None:
        # TODO: Make into Interaction
        """Choose between multiple options.
        There must be at least 2 options to pick from.
        Options are separated by spaces.
        To denote options which include whitespace, you should enclose the options in double quotes.
        """
        choices = [escape(c, mass_mentions=True) for c in choices if c]
        if len(choices) < 2:
            await ctx.send(_("Not enough options to pick from."))
        else:
            await ctx.send("I ch{0}se: ".format("o" * randint(2, 5)) + choice(choices))

    @commands.command()
    async def flip(self, ctx, user: discord.Member = None):
        # TODO: Make into Interaction
        """Flip a coin... or a user.
        Defaults to a coin.
        """
        _ = lambda a: a
        if user is not None:
            msg = ""
            if user.id == ctx.bot.user.id:
                user = ctx.author
                msg = _(
                    "Nice try. You think this is funny?\n How about *this* instead:\n\n"
                )
            if user.id == 242398251855249428:  # Me
                user = ctx.author
                msg = _("Haha that's cute. \n\n")
            elif user.id == 277272009824665600:  ## Milk
                msg = _("Hey! Don't touch Milk!\nThat's *my* job 😎.")
            elif user.id == 280780450610544650:  # Antoine
                msg = _("Yeah, she deserves this.\n")
            # Lower case
            char = "abcdefghijklmnopqrstuvwxyz"
            tran = "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz"
            table = str.maketrans(char, tran)
            name = user.display_name.translate(table)
            # Upper Case
            char = char.upper()
            tran = "∀𐐒ƆᗡƎℲפHIſʞ˥WNOԀQᴚS┴∩ΛMX⅄Z"
            table = str.maketrans(char, tran)
            name = name.translate(table)
            # Symbols
            char = '(){}[]!"&.346789;<>?‿_'
            tran = ")(}{][¡„⅋˙Ɛᔭ9Ɫ89؛><¿⁀‾"
            table = str.maketrans(char, tran)
            name = name.translate(table)
            # Accents
            # char = "ÀÈÌÒÙàèìòùÁÉÍÓÚÝáéíóúýÂÊÎÔÛâêîôûÃÑÕãñõÄËÏÖÜŸäëïöüÿ"
            # tran = "∀Ǝ̖I̖O̖∩ɐ̖ǝ̖ı̖o̖n̖∀Ǝ̗I̗O̗∩⅄̗ɐ̗ǝ̗ᴉ̗o̗n̗ʎ̗∀Ǝ̬I̬O̬∩ɐ̬ǝ̬ᴉ̬o̬n̬∀N̰O̰ɐ̰ṵo̰∀̤Ǝ̤I̤O̤∩⅄̤ɐ̤ǝ̤ᴉ̤o̤n̤ʎ̤"
            # print('{0}-{1}'.format(len(char),len(tran)))
            # table = str.maketrans(char, tran)
            # name = name.translate(table)
            if user.id == 315229592837160962:
                await ctx.send(
                    "Do a barrel roll!\n{0} {1}\n{0} {2}\n{0} {1}\n{0} {2}\n{0} KERSPLAT.".format(
                        "(╯°□°）╯︵ ", name[::-1], user.display_name
                    )
                )
                return
            await ctx.send(msg + "(╯°□°）╯︵ " + name[::-1])
        else:
            await ctx.send(
                _("*flips a coin and... ") + choice([_("HEADS!*"), _("TAILS!*")])
            )

    @app_commands.command(name="reminder", description="Reminds you of something.")
    @app_commands.describe(
        hours="Hours.",
        minutes="Minutes.",
        seconds="Seconds.",
        message="Your reminder message.",
    )
    @app_commands.choices(
        hours=[Choice(name=str(i), value=i) for i in range(0, 25)],
        minutes=[Choice(name=str(i), value=i) for i in range(0, 56, 5)],
        seconds=[Choice(name=str(i), value=i) for i in range(5, 56, 5)],
    )
    @app_commands.checks.bot_has_permissions(send_messages=True)
    async def reminder(
            self,
            interaction: discord.Interaction,
            hours: int,
            minutes: int,
            seconds: int,
            message: str,
    ) -> None:
        """Reminds you of something."""
        remind_in = round(
            datetime.timestamp(
                datetime.now()
                + timedelta(hours=hours, minutes=minutes, seconds=seconds)
            )
        )
        await interaction.response.send_message(
            f"Your message will be sent <t:{remind_in}:R>."
        )

        await asyncio.sleep(seconds + minutes * 60 + hours * (60 ** 2))
        await interaction.channel.send(
            f":bell: <@{interaction.user.id}> Reminder (<t:{remind_in}:R>): {message}"
        )
