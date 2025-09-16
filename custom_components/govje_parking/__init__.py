"""The GOVJE Parking integration."""
from __future__ import annotations

import logging
import aiohttp
import json
from datetime import timedelta, datetime
from typing import Any, Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    DEFAULT_SCAN_INTERVAL,
    GOVJE_COORDINATOR,
    GOVJE_NAME,
    REMOTE_URL,
    CONF_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BUTTON]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up GOVJE Parking from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Get scan interval from options or use default
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL.total_seconds() // 60)
    scan_interval_timedelta = timedelta(minutes=scan_interval)
    
    # Create data coordinator
    coordinator = JerseyParkingDataCoordinator(
        hass=hass,
        update_interval=scan_interval_timedelta
    )
    
    # Initial data fetch
    await coordinator.async_config_entry_first_refresh()
    
    # Store coordinator reference
    hass.data[DOMAIN][entry.entry_id] = {
        GOVJE_COORDINATOR: coordinator,
        GOVJE_NAME: entry.title,
    }
    
    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Add update listener for options
    entry.async_on_unload(entry.add_update_listener(update_listener))
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener for options."""
    # Get the coordinator
    coordinator = hass.data[DOMAIN][entry.entry_id][GOVJE_COORDINATOR]
    
    # Get new scan interval from options
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL.total_seconds() // 60)
    scan_interval_timedelta = timedelta(minutes=scan_interval)
    
    # Update coordinator's update interval
    coordinator.update_interval = scan_interval_timedelta
    
    # Schedule next update with new interval
    coordinator.async_schedule_refresh()
    
    _LOGGER.debug("Updated scan interval to %s minutes", scan_interval)


class JerseyParkingDataCoordinator(DataUpdateCoordinator):
    """Class to manage fetching GOVJE parking data."""

    def __init__(self, hass: HomeAssistant, update_interval: timedelta = DEFAULT_SCAN_INTERVAL) -> None:
        """Initialize the data coordinator."""
        self.hass = hass
        self.session = async_get_clientsession(hass)
        self.latest_timestamp = None
        self.latest_data = None
        self.last_scrape_time = None
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from GOVJE Parking website."""
        try:
            # Update the last scrape time (format as readable time without milliseconds)
            self.last_scrape_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return await self._fetch_remote_data()
        except Exception as err:
            raise UpdateFailed(f"Error updating Jersey parking data: {err}") from err

    async def _fetch_remote_data(self) -> dict[str, Any]:
        """Fetch data from remote URL."""
        try:
            # Add a user agent to avoid being blocked by the website
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "application/json"
            }
            
            async with self.session.get(REMOTE_URL, headers=headers) as resp:
                if resp.status != 200:
                    _LOGGER.error(
                        "Error fetching Jersey parking data: %s", resp.status
                    )
                    raise UpdateFailed(f"Error fetching data: {resp.status}")
                
                json_content = await resp.text()
                _LOGGER.debug("Successfully fetched data from %s", REMOTE_URL)
                _LOGGER.debug("JSON content length: %d", len(json_content))
                _LOGGER.debug("JSON content preview: %s", json_content[:200])
                return self._parse_parking_data(json_content)
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching Jersey parking data: %s", err)
            raise

    def _parse_parking_data(self, json_content: str) -> dict[str, Any]:
        """Parse the JSON content to extract car park data."""
        # Initialize an empty result dictionary
        result = {}
        
        # If we have previous data, use it as a starting point
        if self.latest_data:
            result = self.latest_data.copy()
        
        try:
            # Parse the JSON content
            try:
                data = json.loads(json_content)
            except json.JSONDecodeError as e:
                _LOGGER.error("Error parsing JSON: %s", e)
                return result
            
            # Extract the timestamp from the JSON data
            if 'carparkData' in data and 'Timestamp' in data['carparkData']:
                self.latest_timestamp = data['carparkData']['Timestamp']
                _LOGGER.debug("Timestamp from data: %s", self.latest_timestamp)
            else:
                _LOGGER.warning("No timestamp found in JSON data")
                # If no timestamp, still proceed with the update
            
            # Process car park data
            if 'carparkData' in data and 'Jersey' in data['carparkData'] and 'carpark' in data['carparkData']['Jersey']:
                carparks = data['carparkData']['Jersey']['carpark']
                _LOGGER.debug("Found %d car parks in the JSON data", len(carparks))
                
                # Process each car park
                for carpark in carparks:
                    if 'name' in carpark and 'spaces' in carpark and 'carparkOpen' in carpark:
                        car_park_name = carpark['name']
                        
                        # Only add car parks that are open
                        if carpark['carparkOpen']:
                            # Try to parse spaces as an integer
                            try:
                                spaces = int(carpark['spaces'])
                                # Create entry for new car parks or update existing ones
                                if car_park_name not in result:
                                    result[car_park_name] = {"free_spaces": spaces}
                                    _LOGGER.info("Added new car park: %s with %d spaces", car_park_name, spaces)
                                else:
                                    result[car_park_name]["free_spaces"] = spaces
                                    _LOGGER.debug("Updated car park %s with %d spaces", car_park_name, spaces)
                                    
                                # Add all extra fields from the JSON data as attributes
                                for field, value in carpark.items():
                                    if field != 'spaces':  # We already handle spaces as free_spaces
                                        result[car_park_name][field] = value
                                _LOGGER.debug("Added extra fields for %s: %s", car_park_name, 
                                             {k: v for k, v in carpark.items() if k != 'spaces'})
                            except (ValueError, TypeError):
                                _LOGGER.debug("Could not parse spaces for %s: %s", car_park_name, carpark['spaces'])
                        else:
                            _LOGGER.debug("Car park %s is closed", car_park_name)
                
                # Add the timestamp to each car park's data
                if self.latest_timestamp:
                    for car_park in result:
                        result[car_park]["last_updated"] = self.latest_timestamp
                    _LOGGER.debug("Added last updated timestamp: %s", self.latest_timestamp)
            
            # Log the result
            if not result:
                _LOGGER.warning("Could not find any car parks in the JSON data")
            else:
                _LOGGER.info("Successfully parsed %d car parks from JSON data", len(result))
                
        except Exception as e:
            _LOGGER.error("Error parsing car park data: %s", e)
            # Return empty dict if parsing fails
            return {}
        
        # Store the latest data
        self.latest_data = result
        return result
        
    # Timestamp parsing methods removed as they are no longer needed
