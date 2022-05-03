import datetime
import time
import re
from random import randint, choice

import discord
from discord.ext import commands

from core.utils.chat_formatter import escape
from cogs.misc.about import AboutView, get_client_uptime, gen_about_embed


async def setup(client):
    await client.add_cog(Misc(client))


class Misc(commands.Cog):
    """
    Provides some neat stats on the Bot.

    PING: Measures ping
    UPTIME: Measures uptime
    ABOUT: Gives nice data on memory usage and the such.

    """

    def __init__(self, client):
        self.client = client

    @commands.command(
        name="about", usage="!about", aliases=["info", "sakamoto", "author"]
    )
    async def _about(self, ctx: commands.Context):
        e = gen_about_embed(self.client)
        await ctx.send(embed=e, view=AboutView(ctx))

    @commands.command(name="git", usage="!github", aliases=["source", "github"])
    async def _git(self, ctx: commands.Context):
        """
        Links to the Github repo
        """
        ## TODO: Expand Command to include subcommands such as !git issue
        await ctx.send(
            "See my code and give me a star at: https://github.com/Nekurone/Sakamoto"
        )

    @commands.command(name="ping", usage="!ping", aliases=["pong"])
    async def _ping(self, ctx: commands.Context):
        """
        Measures how long until a message is sent to Discord and detected.
        """
        ping = ctx.message
        pong = await ctx.send("**:ping_pong:** Pong!")
        delta = pong.created_at - ping.created_at
        delta = int(delta.total_seconds() * 1000)
        await pong.edit(
            content=f":ping_pong: Pong! ({delta} ms)\n*Discord WebSocket Latency: {round(self.client.latency, 5)} ms*"
        )
        return

    @commands.command(name="uptime", usage="!uptime")
    async def _uptime(self, ctx: commands.Context):
        """
        Gets the time since the bot first connected to Discord
        """
        em = discord.Embed(
            title="Local time",
            description=str(datetime.datetime.now())[:-7],
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

    @commands.command(name="poll", aliases=["ynpoll", "pollstart"])
    async def _ynpoll(self, ctx: commands.Context, *, question: str):
        """
        Asks question & then adds checkmark & "x" as reactions.
        Thanks to Spoon for this code
        """
        ynpoll_embed = discord.Embed(
            title="Yes/No Poll",
            description="This is a yes/no poll. Please react with ✅ if yes and ❌ if no.",
            timestamp=ctx.message.created_at,
        )
        ynpoll_embed.add_field(name="Poll Question", value=f"{question}", inline=False)
        ynpoll_embed.set_footer(
            text=f"Poll By {ctx.author}", icon_url="https://i.imgur.com/3VPTx2K.gif"
        )
        await ctx.message.delete()
        message = await ctx.send(embed=ynpoll_embed)
        emoji_1 = "✅"
        emoji_2 = "❌"
        await message.add_reaction(emoji_1)
        await message.add_reaction(emoji_2)

    @commands.command(usage="<first> <second> [others...]")
    async def choose(self, ctx, *choices) -> None:
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
