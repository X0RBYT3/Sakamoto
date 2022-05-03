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
            print(f"Cog Loading Failed: {cog}\n{exc}")
            raise e
        else:
            print(f"{cog} {mode} Successful.")
