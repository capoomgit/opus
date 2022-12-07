from logger import setup_logger

logger = setup_logger(f"test.log")
logger.spaces("test spaces")
logger.critical("test critical")