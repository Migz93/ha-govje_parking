"""Constants for govje_parking."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "govje_parking"
ATTRIBUTION = "Data provided by Government of Jersey"
PARALLEL_UPDATES = 1

REMOTE_URL = "https://sojpublicdata.blob.core.windows.net/sojpublicdata/carpark-data.json"

CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_SCAN_INTERVAL_MINUTES = 5
MIN_SCAN_INTERVAL_MINUTES = 2
MAX_SCAN_INTERVAL_MINUTES = 120
