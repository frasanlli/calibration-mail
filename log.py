import logging

class Log():
    def __init__(self) -> None:
        # Set up logger
        self.logger: logging.getLogger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s - %(message)s")

        file_handler = logging.FileHandler(f"{__file__}.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)