import sys, os

import discord


async def cogs_manager(client: discord.Client, mode: str, cogs: list[str]) -> None:
    for cog in cogs:
        try:
            cog_path = f"cogs.{cog}.main"
            if mode == "unload":
                await client.unload_extension(cog_path)
            elif mode == "load":
                await client.load_extension(cog_path)

            elif mode == "reload":
                await client.reload_extension(cog_path)
            else:
                raise ValueError("Invalid mode.")
        except Exception as e:
            exc = f"{type(e).__name__}: {e}"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, exc)
            print(f"**`ERROR:`** Cog Loading Failed: {cog}\n{exc}")
        else:
            print(f"**`SUCCESS`** - {cog} {mode}ed! \N{PISTOL}")
    return f"**`SUCCESS`** - {cog} {mode}ed! \N{PISTOL}"  # Since we only need this for sending to discord
