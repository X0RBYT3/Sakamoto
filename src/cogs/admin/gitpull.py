import os

import git
import discord
from core.cogmanager import cogs_manager

"""
Command to check for github pulls on main
"""
GIT_PATH = os.path.dirname(os.getcwd())


def check_for_push(msg: discord.Message) -> bool:
    # A fucking awful solution.
    # I hate this code with every part of my essence.
    if len(msg.embeds) < 1 or msg.channel.id != 853358653808836659:
        return False
    # Make sure it's main!
    if "Sakamoto:main" in msg.embeds[0].title and "new commit" in msg.embeds[0].title:
        # We got a pull
        return True
    return False


async def pull_and_reload(client: discord.Client):
    repo = git.Repo(GIT_PATH)
    current = repo.head.commit
    repo.remotes.origin.pull()
    print("Pulling")
    r = await cogs_manager(client, "reload", client.cogs)
    print("Reload complete.")
