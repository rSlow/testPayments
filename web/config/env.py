from os import PathLike

from environs import Env


def get_env(env_file: PathLike | None = None) -> Env:
    env = Env()
    if env_file is not None:
        env.read_env(str(env_file))
    return env


ENV = get_env()
