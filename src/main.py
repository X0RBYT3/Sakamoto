import sys
import logging
import argparse, textwrap
from pathlib import Path
from bot import sakaClient
from core.config import get_secrets, set_logging, VERSION, PREFIX

"""
Main File, run this to run the bot
"""
# COGS TO LOAD
# Uses /cogs/{cog_name}/main to load them
# All CogNames are the same as their folder names
COGS = ["admin", "misc", "info"]

# Change this as you want
bannerstr = f"""
            SAKAMOTO
        VERSION: {VERSION}
    MADE WITH <3 by Nekurone.
    """

# Could add more to these
parser = argparse.ArgumentParser(
    add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(bannerstr),
)
parser.add_argument(
    "-l",
    "--logging",
    help="Level at which to set logging module.\nOptions are: CRITICAL, ERROR, WARNING, INFO, and DEBUG\n DEFAULT: WARNING",
    action="store",
    default="WARNING",
)
parser.add_argument(
    "-p",
    "--prefix",
    help="|| PREFIX Sets a temporary prefix different to the one in core/config.py || NOT CURRENTLY WORKING",
    action="store",
    default="",
)
parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS)

SECRETS_PATH = Path("core/secrets.env")


def main():
    if not SECRETS_PATH.exists():
        print(
            "Error: Have you placed the discord token inside a secrets.env file in /core ?"
        )
        return

    parser.print_help()
    args = parser.parse_args()
    v = vars(args)
    set_logging(level=v["logging"], filename="discord.log")
    secrets = get_secrets()
    prefix = v["prefix"]
    if len(prefix) > 0 and len(prefix) < 2 and not prefix.isalnum() and prefix != " ":
        g_PREFIX = prefix
    else:
        g_PREFIX = PREFIX
    client = sakaClient(COGS, secrets, g_PREFIX)
    client.run(secrets["TOKEN"])


if __name__ == "__main__":
    main()
