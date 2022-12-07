import logging.handlers
from dotenv import load_dotenv
import os

load_dotenv()

logger = logging.getLogger(os.getenv("LOG_NAME"))
logger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

fileHandler = logging.handlers.RotatingFileHandler(os.getenv("PATH_LOGS"), maxBytes=75000,  backupCount=6)
fileHandler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

consoleHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)

logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)

logger.info("Logger is ready")
