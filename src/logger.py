import logging


class Logger:
    def add_logger(self, name: str, log_filename: str, level: int, formatter: str = "%(asctime)s %(levelname)s %(message)s") -> None:
        handler = logging.FileHandler(log_filename)
        handler.setFormatter(logging.Formatter(formatter))

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        setattr(self, name, logger)
