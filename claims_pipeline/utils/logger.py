import logging
from enum import Enum


class ColourEnum(Enum):
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'

    def __str__(self):
        return self.value


class CustomLogger(logging.Logger):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.setLevel(logging.INFO)
        self.propagate = False
        self.handler = logging.StreamHandler()
        self.formatter = logging.Formatter(
            f'%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

logging.setLoggerClass(CustomLogger)