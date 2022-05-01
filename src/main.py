from os.path import exists

from bot import shinobuClient
from core.config import get_secrets
"""
Main File, run this to run the bot
"""
# TODO: Logging, Runtime parameters

COGS = []

def main():
    if not exists('core/secrets.env'):
        print('Error: Have you placed the discord token inside a secrets.env file in /core ?')
        return
    secrets = get_secrets()
    client = shinobuClient(COGS,secrets)
    print(f'Booting Shinobu with {len(COGS)} Cogs')
    client.run(secrets['TOKEN'])

main()
