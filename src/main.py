from os.path import exists

from bot import sakaClient
from core.config import get_secrets, set_logging
import logging

"""
Main File, run this to run the bot
"""
# TODO: Runtime parameters

COGS = ["admin", "misc", "info"]


def main():
    if not exists("core/secrets.env"):
        print(
            "Error: Have you placed the discord token inside a secrets.env file in /core ?"
        )
        return
    set_logging(level=logging.WARNING, filename="discord.log")
    secrets = get_secrets()
    client = sakaClient(COGS, secrets)
    client.run(secrets["TOKEN"])


if __name__ == "__main__":
    main()
