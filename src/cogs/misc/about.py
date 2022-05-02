from datetime import datetime
import platform

import discord
from discord.ext import commands

# Ew american spelling
from core.utils.chat_formatter import humanize_timedelta


def get_client_uptime(uptime, brief=False):
    """
    works well enough for what it does
    have a feeling it could be better
    """
    now = datetime.now()
    delta = now - uptime
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    if brief:
        fmt = "{h}h {m}m {s}s"
        if days:
            fmt = "{d}d " + fmt
        return fmt.format(d=days, h=hours, m=minutes, s=seconds)
    return humanize_timedelta(delta)


class AboutView(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__()
        self.add_item(
            discord.ui.Button(
                label="🤖 Check out my Code!", url="https://github.com/Nekurone/Sakamoto"
            )
        )
        self.add_item(
            discord.ui.Button(
                disabled=True,
                label="📄 Check out my site! (WIP)",
                url="https://www.google.com",
            )
        )


def gen_about_embed(client: discord.Client) -> discord.Embed:
    embed = discord.Embed(
        title="Hi, I'm Sakamoto",
        description="I'm a Discord Bot by `Florence#5005`. I'm in very early stages so be sure to check out my code and contribute. See my Github below! ",
    )
    embed.colour = 0x738BD7
    embed.set_author(name="About Me!", icon_url="https://i.imgur.com/3VPTx2K.gif")

    total_members = sum(1 for _ in client.get_all_members())
    total_online = len(
        {m.id for m in client.get_all_members() if m.status is discord.Status.online}
    )
    total_unique = len(client.users)

    voice_channels = []
    text_channels = []
    for guild in client.guilds:
        voice_channels.extend(guild.voice_channels)
        text_channels.extend(guild.text_channels)

    embed.add_field(
        name="Members",
        value=f"{total_members} total\n{total_unique} unique\n{total_online} unique online",
    )
    # embed.add_field(
    # name='Channels', value=f'{text + voice} total\n{text} text\n{voice}
    # voice')
    embed.add_field(name="Guilds", value=len(client.guilds))
    embed.add_field(name="Version", value=client._version)
    embed.add_field(name="Python Version", value=platform.python_version(), inline=True)
    embed.add_field(name="Uptime", value=get_client_uptime(client.uptime, brief=True))
    embed.set_footer(
        text="Made with 💖 by Florence",
        icon_url="https://media.giphy.com/media/qjPD3Me0OCvFC/giphy.gif",
    )
    return embed
