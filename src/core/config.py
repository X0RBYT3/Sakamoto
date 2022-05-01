import os

"""
Yes, this is awful, Yes I'm too stubborn to use dotenv, I may open it as an
issue if people complain
"""


def get_secrets():
    secrets = {}
    env_file = "core/secrets.env"
    with open(env_file) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            if "export" not in line:
                continue
            key, value = line.replace("export ", "", 1).strip().split("=", 1)
            secrets[key] = value
        return secrets


VERSION = "0.1.0"
PREFIX = "!"
