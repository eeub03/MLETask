import logging


class Logger(logging.Logger):
    def __init__(self, name: str) -> None:
        super().__init__(name, level=logging.INFO)
        self.handler = logging.StreamHandler()
        self.handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter(
            f"%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.handler.setFormatter(self.formatter)
        self.addHandler(self.handler)
