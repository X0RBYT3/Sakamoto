import string
from typing import List, Literal, Optional
import time

import discord
from discord.ext import commands
from discord import app_commands

from cogs.fun import minesweeper

# from cogs.fun import views
MINESWEEPER_HELP = """
Minesweeper is a game where mines are hidden in a grid of squares. Safe squares have numbers telling you how many mines touch the square. You can use the number clues to solve the game by opening all of the safe squares. If you click on a mine you lose the game!


`/minesweeper` has several options,
`/minesweeper random` -> A random board
`/minesweeper daily` -> Today's game
`/minesweeper my daily` -> Your game of the day!
`/minesweeper mysweep` -> A game tied to your user ID.

Each game can be customised with `width` and `height` to your liking.

Once you're in a game, use `/ms [column] [row]` to pick your cell to uncover use `/ms [column] [row] True` to place a flag !
You win the game once you've opened every safe square without blowing up!

Good luck! 💣"""


def gen_mine_help() -> discord.Embed:
    em = discord.Embed(
        title="💣 Minesweeper Help 💣",
        description=MINESWEEPER_HELP,
        color=discord.Color.blurple(),
    )
    em.set_image(url="https://i.imgur.com/xXR4rwn.gif")
    em.set_footer(
        text="Made with 💖 by Xorhash",
        icon_url="https://c.tenor.com/Gxa1JfN3334AAAAC/dm4uz3-sakamoto.gif",  # Spin gif
    )
    return em


async def setup(client):
    await client.add_cog(Fun(client))


class Fun(commands.Cog):
    """
    Commands Designed for Fun!!
    """

    def __init__(self, client):
        self.wordle_games = {}
        self.minesweeper_games = {}
        self.client = client

    # WIP

    # @app_commands.command(name="wordle", description="Play Wordle!")
    # @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    # async def _wordle(self, interaction: discord.Interaction):
    #     V = views.WordleView()

    #     u = interaction.user
    #     m = None
    #     e = None
    #     while V.finished is not True:

    #         def check(i):
    #             return i.data["name"] == "guess" and i.user == u

    #         print(interaction.data)
    #         await interaction.response.send_message("Hello, I am under the water.")

    async def minesweep_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        choices = ["Random", "Daily", "My Daily", "MySweep", "Help"]
        return [
            app_commands.Choice(name=choices, value=choices)
            for choices in choices
            if current.lower() in choices.lower()
        ]

    @app_commands.command(
        name="roll",
        description="Rolls",
        aliases=["checkem", "check", "riggity", "dubs"],
    )
    async def num_roll(self, ctx: commands.Context):
        # I used to use the last 8 digits of the message ID,
        # but since this is a Hybrid, it won't always have a message ID, so we're using Epoch Time.
        epoch_time = int(time.time())
        await ctx.send(f"Your roll: {epoch_time}.")

    @app_commands.command(name="minesweeper", description="Plays minesweeper")
    @app_commands.autocomplete(choices=minesweep_autocomplete)
    async def minesweeper(
        self,
        interaction: discord.Interaction,
        choices: str,
        width: Optional[int] = 10,
        height: Optional[int] = 10,
    ):
        """The handler for Minesweeper games
        Also handles timeouts for the embed

        Args:
            interaction (discord.Interaction): _description_
            choices (str): _description_
        """
        if interaction.user.id in self.minesweeper_games:
            await interaction.response.send_message(
                "You already have a minesweeper game!", ephemeral=True
            )
            return

        if choices == "Help":
            return await interaction.response.send_message(embed=gen_mine_help())

        # Check width and height are normal numbers
        if min(width, height) < 3 or max(width, height) > 20:
            return await interaction.response.send_message(
                "Bit off on the dimensions there", ephemeral=True
            )
        c = minesweeper.MineSweeperGames(
            choices, interaction, height=height, width=width
        )
        x = c.make_message()
        msg = f"Welcome to Minesweeper. This is a `{choices} Game`, use `/ms [COL][ROW]` to Uncover a square. \nEG: /ms A 1` for the top left square.\nType quit into column in /ms to quit"

        c.mine_message = await interaction.response.send_message(msg, embed=x)
        self.minesweeper_games[interaction.user.id] = c

    @app_commands.command(name="ms", description="Uncover a minesweeper tile")
    async def ms(
        self,
        interaction: discord.Interaction,
        column: str,
        row: int,
        is_flag: Optional[bool] = False,
    ):
        if not interaction.user.id in self.minesweeper_games:
            return await interaction.response.send_message(
                "You don't appear to have a minesweeper game Active, use //minesweeper to start one :)"
            )

        if column.lower() == "quit":
            self.minesweeper_games.pop(interaction.user.id, None)
            return await interaction.response.send_message(
                "Okay, thanks for playing!", ephemeral=True
            )

        if (
            column.upper() not in self.minesweeper_games[interaction.user.id].cols
            or row not in self.minesweeper_games[interaction.user.id].rows
        ):
            await interaction.response.send_message(
                "Sorry, I couldn't find those Coords, try again?", ephemeral=True
            )

        col = self.minesweeper_games[interaction.user.id].cols.index(column.upper())
        if (
            self.minesweeper_games[interaction.user.id].user_board[row - 1][col] != "#"
            and self.minesweeper_games[interaction.user.id].user_board[row - 1][col]
            != "f"
        ):
            return await interaction.response.send_message(
                "You've already uncovered this!", ephemeral=True
            )

        # NOTE !! This will NOT stop a user from "clicking" on a flag
        if (
            is_flag
            and self.minesweeper_games[interaction.user.id].user_board[row - 1][col]
            == "f"
        ):
            return await interaction.response.send_message(
                "This is already a flag !", ephemeral=True
            )

        # Finally checks are over
        if is_flag:
            msg = self.minesweeper_games[interaction.user.id].make_flag(col, row)
            if msg is not None:
                await interaction.response.send_message(msg, ephemeral=True)
        else:
            self.minesweeper_games[interaction.user.id].make_guess(col, row)
        if not self.minesweeper_games[interaction.user.id].finished:
            msg = self.minesweeper_games[interaction.user.id].make_message()
            await interaction.response.send_message(
                embed=msg, ephemeral=True
            )  # Not lost
        else:
            if self.minesweeper_games[interaction.user.id].won:  # woot woot
                msg = discord.Embed(
                    title=f"{interaction.user} WON!",
                    description="Congrats on winning minesweeper, Have a cookie.",
                )
                msg.set_image(
                    url="https://data.whicdn.com/images/234478539/original.jpg"
                )
                msg.set_footer(
                    text="Made with 💖 by Xorhash",
                    icon_url="https://c.tenor.com/Gxa1JfN3334AAAAC/dm4uz3-sakamoto.gif",  # Spin gif
                )
                await interaction.response.send_message(embed=msg)
            else:
                msg = self.minesweeper_games[interaction.user.id].gen_game_over()
                await interaction.response.send_message(msg, ephemeral=True)
            self.minesweeper_games.pop(interaction.user.id, None)
