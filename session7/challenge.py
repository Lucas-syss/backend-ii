import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logger(name: str, log_file: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt='%(asctime)s.%(msecs)03d | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = TimedRotatingFileHandler(
        filename=log_file,
        when='midnight',
        interval=1,
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger("app", "app.log")

if __name__ == "__main__":
    logger.debug("DB connection pool initialised")
    logger.info("Server started on port 8000")
    logger.warning("Response time exceeded 500ms")
    logger.error("Failed to reach external API")

    try:
        _ = 1 / 0
    except ZeroDivisionError:
        logger.exception("Unexpected error in calculation")