import os

import git
import discord

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
    for cog in client.cogs:
        try:
            client.unload_extension(f"cogs.{cog.lower()}.main")
            client.load_extension(f"cogs.{cog.lower()}.main")
        except Exception as e:
            print(f"Error with {cog}: {type(e).__name__} - {e}")
        else:
            print(f"Successfully reload {cog}")
