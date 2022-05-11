import time
import re
import typing
import requests
from random import randint, choice
from datetime import datetime, timedelta

import asyncio
import discord
from discord.app_commands import Choice
from discord.ext import commands
from discord import app_commands

from core.utils.chat_formatter import escape
from cogs.misc.views import PollView


async def setup(client):
    await client.add_cog(Misc(client))


class Misc(commands.Cog):
    """
    Here  be cursed shit
    """

    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name="poll", aliases=["ynpoll", "pollstart"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    @app_commands.choices(
        time=[Choice(name=str(i), value=i) for i in range(10, 120, 10)]
    )
    async def _ynpoll(
        self, ctx: commands.Context, time: typing.Optional[int] = 30, *, question: str
    ):
        """
        Asks question & then adds checkmark & "x" as reactions.
        Thanks to Spoon for original idea

        Make embed -> Add buttons, when buttons are clicked, add them to list and grey out
        after 30 secs announce result

        """
        if time > 120 and not await self.client.is_owner(ctx.author):
            await ctx.send(
                "ERROR: Only the Owner can set the time to more than 2 minutes",
                delete_after=5,
            )
            return
        if time < 5:
            await ctx.send("Bit short don't you think? 🤏")
            return
        ynpoll_embed = discord.Embed(
            title=f"Poll by {ctx.author}. Ends in {time} seconds.",
            description=f"**Question**: {question}",
            timestamp=ctx.message.created_at,
            color=discord.Color.blurple(),
        )
        poll = PollView()
        message = await ctx.send(embed=ynpoll_embed, view=poll)
        await asyncio.sleep(time)

        ynpoll_embed.title = f"Poll by {ctx.author}. Poll Ended"
        # Send forth the greyed out bits.
        await poll.disable_view()
        await message.edit(embed=ynpoll_embed, view=poll)
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
        result_em.title = f"{ctx.author} asked '{question}' {randint(4,9)*'a'}nd the result is: **{result}**"
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
        await message.reply(embed=result_em)

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
            await ctx.send("Not enough options to pick from.")
        else:
            await ctx.send(f"I ch{randint(2,9)*'o'}se: {choice(choices)}")

    @commands.command(usage="flip <user>")
    async def flip(self, ctx, user: discord.Member = None):
        # TODO: Make into Interaction
        """Flip a coin... or a user.
        Defaults to a coin.
        Needs rewriting
        """
        if user is not None:
            msg = ""
            if user.id == ctx.bot.user.id:
                user = ctx.author
                msg = (
                    "Nice try. You think this is funny?\n How about *this* instead:\n\n"
                )
            if user.id == 242398251855249428:  # Me
                user = ctx.author
                msg = "Haha that's cute. \n\n"
            elif user.id == 277272009824665600:  ## Milk
                msg = "Hey! Don't touch Milk!\nThat's *my* job 😎."
            elif user.id == 280780450610544650:  # Antoine
                msg = "Yeah, she deserves this.\n"
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
                ("*flips a coin and... ") + choice([("HEADS!*"), ("TAILS!*")])
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

        await asyncio.sleep(seconds + minutes * 60 + hours * (60**2))
        await interaction.channel.send(
            f":bell: <@{interaction.user.id}> Reminder (<t:{remind_in}:R>): {message}"
        )
