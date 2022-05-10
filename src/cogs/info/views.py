from datetime import datetime
from random import choice
import platform
from distutils.util import strtobool  # I fucking love this command
from typing import Optional
import discord
from discord.ext import commands

import traceback

# Ew american spelling
from core.utils.chat_formatter import humanize_timedelta

joke_suggestions = ["Get more cat litter", "Treat Sakamoto better!", "*jazz hands*"]


def get_client_uptime(uptime, brief=False):
    # Works well enough for what it does
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


# Could include some more stats. Will revisit
def gen_about_embed(client: discord.Client) -> discord.Embed:
    embed = discord.Embed(
        title="About Me!",
        description="Hi, I'm **Sakamoto**, a Discord Bot by ``Florence#5005``,I'm still in my early stages so be sure to check back often for updates.\n\nAlternatively, if you have any suggestions for me, use `/suggest` to pass forward a suggestion.",
        url="https://github.com/Nekurone/Sakamoto/",
        color=0xC55050,  # Nice light red
    )
    embed.set_image(url="https://c.tenor.com/3qDw5i6bwGUAAAAM/dm4uz3-nichijou.gif")
    # Wag gif
    voice_channels = []
    text_channels = []
    for guild in client.guilds:
        voice_channels.extend(guild.voice_channels)
        text_channels.extend(guild.text_channels)

    embed.add_field(name="Guilds", value=len(client.guilds), inline=True)
    embed.add_field(name="Version", value=client._version, inline=True)
    embed.add_field(name="Python Version", value=platform.python_version(), inline=True)
    embed.add_field(name="Uptime", value=get_client_uptime(client.uptime, brief=True))
    embed.set_footer(
        text="Made with 💖 by Florence",
        icon_url="https://c.tenor.com/Gxa1JfN3334AAAAC/dm4uz3-sakamoto.gif",  # Spin gif
    )
    return embed


class SuggestionModal(discord.ui.Modal, title="Sakamoto Suggestion"):

    suggestion = discord.ui.TextInput(
        label="Suggestion:",
        style=discord.TextStyle.long,
        placeholder=f"Suggestion: {choice(joke_suggestions)}.",
        required=True,
        max_length=200,
    )
    consent = discord.ui.TextInput(
        label="Do you consent to being contacted? (Y/N)",
        style=discord.TextStyle.short,
        placeholder="Yes/No",
        required=True,
        max_length=5,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        """
        This would be a FANTASTIC use of either
        - a simple Flask POST server
        - Google sheets
        Alternatively, could use Git and use it on a private repo
        """
        time_str = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        suggest_str = f"{time_str} -- {self.suggestion.value}"
        if strtobool(self.consent.value):
            suggest_str = f"{interaction.user} -- {suggest_str}"
        with open("suggestions.txt", "a+") as sug:
            sug.write("\n")
            sug.write(suggest_str)
        await interaction.response.send_message(
            f"Thanks for suggesting: {self.suggestion.value}", ephemeral=True
        )

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        await interaction.response.send_message(
            "Oops! Something went wrong.", ephemeral=True
        )

        # Make sure we know what the error actually is
        traceback.print_tb(error.__traceback__)


class GithubView(discord.ui.View):
    # Very very basic, could have a modal in future for adding issues??
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


class AboutView(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__()
        self.add_item(
            discord.ui.Button(
                label="🤖 Check out my Code!", url="https://github.com/Nekurone/Sakamoto"
            )
        )

    @discord.ui.button(
        label="Suggest a Feature", style=discord.ButtonStyle.success, emoji="📄"
    )
    async def sugg_button(
        self, interaction: discord.Integration, button: discord.ui.Button
    ):
        await interaction.response.send_modal(SuggestionModal())
