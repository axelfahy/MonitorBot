"""Monitoring module."""
import logging
import os
import uuid
from pathlib import Path
from dotenv import load_dotenv

from ._version import get_versions

# Load the .env file containing the keys.
load_dotenv()

# Timeout for requests.
SLEEP_TIME = 30
SLEEP_BETWEEN_MSG = 60 * 10

# Default command and its threshold.
DEFAULT_CMD = "free | grep Mem | awk '{print $3/$2 * 100.0}'"
DEFAULT_THRESHOLD = 30
DEFAULT_METRIC = 'RAM'

# Server hostname, either pass to the docker container or set in the .env file.
HOSTNAME = os.getenv('HOSTNAME')
if not HOSTNAME:
    HOSTNAME = os.uname()[1]
assert HOSTNAME, 'Error when retrieving the hostname of the server.'

# Telegram information.
HOOKURL = os.getenv('HOOKURL')

# Logging configuration.
# Log the DEBUG inside a file and the INFO to stderr.
FORMATTER = logging.Formatter('%(asctime)s [%(levelname)-7s] %(name)s: %(message)s')

# File logger.
LOGFILE = Path('logs').joinpath(f'monitorbot_{uuid.uuid4()}.log')
LOGFILE.parent.mkdir(exist_ok=True)
file_handler = logging.FileHandler(LOGFILE)  # pylint: disable=invalid-name
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(FORMATTER)

# Stream logger.
stream_handler = logging.StreamHandler(None)  # pylint: disable=invalid-name
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(FORMATTER)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)-7s] %(name)s: %(message)s',
    handlers=[file_handler, stream_handler]
)

__version__ = get_versions()['version']
del get_versions
