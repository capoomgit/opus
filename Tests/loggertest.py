
import sys
sys.path.insert(0, "P:/pipeline/standalone_dev/libs")
sys.path.insert(1, "P:/pipeline/standalone_dev/libs/site-packages")

from logger import setup_logger
logger = setup_logger(f"test.log")
logger.opus("test opus")
logger.spaces("test spaces")
logger.critical("test critical")