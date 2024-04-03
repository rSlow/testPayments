import os.path
from pathlib import Path
from typing import Optional

from environs import Env


def get_env(base_dir: Optional[Path] = None):
    env = Env()
    if base_dir is not None:
        ENV_FILE = base_dir.parent / ".env"
        if os.path.isfile(ENV_FILE):
            env.read_env(str(ENV_FILE))
    return env
