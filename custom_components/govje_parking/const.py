"""Constants for GOVJE Parking Integration."""
from datetime import timedelta

DOMAIN = "govje_parking"

DEFAULT_NAME = "GOVJE Parking"
ATTRIBUTION = "Data provided by Government of Jersey"

DEFAULT_SCAN_INTERVAL = timedelta(minutes=5)
MIN_SCAN_INTERVAL = 2  # minutes
MAX_SCAN_INTERVAL = 120  # minutes (2 hours)

# Configuration and options
CONF_SCAN_INTERVAL = "scan_interval"

# Coordinator names
GOVJE_COORDINATOR = "govje_coordinator"
GOVJE_NAME = "govje_name"

# Data source
REMOTE_URL = "https://sojpublicdata.blob.core.windows.net/sojpublicdata/carpark-data.json"

# Platform
PLATFORM_SENSOR = "sensor"

# Entity attributes
ATTR_LAST_UPDATED = "last_updated"
