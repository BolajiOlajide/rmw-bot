from os import environ, path

from dotenv import load_dotenv

env_path = path.join(path.dirname(__file__), path.pardir, ".env")
load_dotenv(env_path, override=True)


def get_env(key):
    return environ.get(key)
