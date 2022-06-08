from typing import Sequence, Optional

import discord
from discord.ext import commands


class AnsiHelp(commands.DefaultHelpCommand):
    """An override of DefaultHelpCommand that provides a colorful help message by using
    Discord's ANSI syntax highlighting."""

    def __init__(self):
        super().__init__(paginator=commands.Paginator(prefix="```ansi"))

    # NOTE(Shad):
    #   May not paginate properly if command descriptions are too long!
    #   Could be worth some further scrutiny once we add more commands.
    def add_indented_commands(
        self,
        commands: Sequence[commands.Command],
        *,
        heading: str,
        max_size: Optional[int] = None,
    ) -> None:
        if not commands:
            return

        self.paginator.add_line("[1;37m" + heading)
        max_size = max_size or self.get_max_size(commands)

        get_width = discord.utils._string_width
        for command in commands:
            name = command.name
            width = max_size - (get_width(name) - len(name))
            entry = (
                f'{self.indent * " "}[1;32m{name:<{width}} [1;34m{command.short_doc}'
            )
            self.paginator.add_line(entry)

    def get_ending_note(self) -> str:
        return "[1;33m" + super().get_ending_note()
