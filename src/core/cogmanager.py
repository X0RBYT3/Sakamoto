import sys, os

import discord


async def cogs_manager(client: discord.Client, mode: str, cogs: list[str]) -> None:
    """This breaks more than ANYTHING else.
    Could probably do with recursively reloading all modules on a load.

    Args:
        client (discord.Client): the discord Client
        mode (str): "unload", "reload" or "load"
        cogs (list[str]): a list of cogs to perform functions on

    Raises:
        ValueError: Bad mode

    Returns:
        _type_: Success or Error code.
    """
    for cog in cogs:
        try:
            cog_path = f"cogs.{cog.lower()}.main"
            if mode == "unload":
                await client.unload_extension(cog_path)
            elif mode == "load":
                await client.load_extension(cog_path)

            elif mode == "reload":
                await client.reload_extension(cog_path)
            else:
                raise ValueError("Invalid mode.")
            if len(cogs) == 1:
                return f"**`SUCCESS`** - {cog} {mode}ed! \N{PISTOL}"
        except Exception as e:
            exc = f"{type(e).__name__}: {e}"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, exc)

            if len(cogs) == 1:
                return f"**`ERROR:`** Cog Loading Failed: {cog}\n{exc}\n{exc_type} {fname} {exc_tb.tb_lineno}"
        else:
            print(f"**`SUCCESS`** - {cog} {mode}ed! \N{PISTOL}")
        # Since we only need this for sending to discord
