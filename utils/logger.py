import logging

class Logger:
    def __init__(self, level) -> None:
        levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR
        }

        # Set logging level.
        self.level = levels.get(level, logging.INFO)

        # Configure logging.
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=self.level
        )
        self.logger = logging.getLogger(__name__)

    def debug(self, message:str) -> None:
        """Log a debug message."""
        self.logger.debug(f"{message}")

    def info(self, message:str,) -> None:
        """Log an info message."""
        self.logger.info(f"{message}")

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(f"{message}")

    def error(self, message: str) -> None:
        """Log an error message."""
        self.logger.error(f"{message}")


log = Logger("DEBUG")
